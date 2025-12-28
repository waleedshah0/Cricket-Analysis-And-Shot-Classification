import os
import json
import time
from typing import Dict, List, Any, Tuple

import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from sentence_transformers import SentenceTransformer
import faiss
from tqdm import tqdm


DEFAULT_DB_CONFIG = {
    "host": "localhost",
    "database": "cricket_db",
    "user": "postgres",
    "password": "admin123",
    "port": 5432,
}


# Map requested table names to actual names used in this project
TABLE_ALIASES = {
    "team_squad_player": "team_squad_players",
    "stadium_patch_info": "stadiums",
    "player_profile": "player_profiles",
}


def resolve_table_name(name: str) -> str:
    return TABLE_ALIASES.get(name, name)


def get_connection(db_config: Dict[str, Any]):
    return psycopg2.connect(
        host=db_config["host"],
        database=db_config["database"],
        user=db_config["user"],
        password=db_config["password"],
        port=db_config["port"],
    )


def fetch_rows(conn, table: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        columns = [desc.name for desc in cur.description]
        return rows, columns


def flatten_json(obj: Any) -> str:
    try:
        if isinstance(obj, (dict, list)):
            return json.dumps(obj, ensure_ascii=False)
        return str(obj)
    except Exception:
        return str(obj)


def row_to_text(table: str, row: Dict[str, Any], columns: List[str]) -> str:
    t = table.lower()
    if t == "stadiums":
        parts = []
        ground = row.get("ground_name")
        pitch_type = row.get("pitch_type")
        desc = row.get("pitch_description")
        url = row.get("url")
        if ground:
            parts.append(f"Stadium: {ground}.")
        if pitch_type:
            parts.append(f"Pitch type: {pitch_type}.")
        if desc:
            parts.append(f"Description: {desc}")
        if url:
            parts.append(f"Source: {url}")
        return " ".join(parts).strip()

    if t == "team_squad_players":
        parts = []
        team = row.get("team_name")
        fmt = row.get("format")
        name = row.get("player_name")
        info = row.get("player_info")
        more = row.get("additional_info")
        link = row.get("player_link")
        if team and fmt:
            parts.append(f"Team: {team} ({fmt}).")
        elif team:
            parts.append(f"Team: {team}.")
        if name:
            parts.append(f"Player: {name}.")
        if info:
            parts.append(f"Info: {info}.")
        if more:
            parts.append(f"Additional: {more}.")
        if link:
            parts.append(f"Profile: {link}")
        return " ".join(parts).strip()

    if t == "player_profiles":
        parts = []
        name = row.get("player_name")
        url = row.get("profile_url")
        personal = flatten_json(row.get("personal_info"))
        batting = flatten_json(row.get("batting_stats"))
        bowling = flatten_json(row.get("bowling_stats"))
        if name:
            parts.append(f"Player: {name}.")
        if personal:
            parts.append(f"Personal: {personal}.")
        if batting:
            parts.append(f"Batting stats: {batting}.")
        if bowling:
            parts.append(f"Bowling stats: {bowling}.")
        if url:
            parts.append(f"Profile URL: {url}.")
        return " ".join(parts).strip()

    # Generic fallback: label each column
    labeled = [f"{col}: {flatten_json(row.get(col))}" for col in columns]
    return ", ".join(labeled)


def normalize(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vectors / norms


def ensure_outdir(path: str):
    os.makedirs(path, exist_ok=True)


def build_table_index(
    conn,
    table: str,
    model: SentenceTransformer,
    out_dir: str,
    model_name: str,
) -> Dict[str, Any]:
    rows, columns = fetch_rows(conn, table)
    if not rows:
        return {"table": table, "count": 0, "index_path": None}

    texts: List[str] = []
    ids: List[int] = []
    for row in rows:
        # Prefer primary key column named 'id'
        pk = row.get("id")
        if pk is None:
            # Try to find any column ending with 'id'
            pk_cols = [c for c in columns if c.endswith("id")]
            pk = row.get(pk_cols[0]) if pk_cols else None
        ids.append(int(pk) if pk is not None else -1)
        texts.append(row_to_text(table, row, columns))

    embeddings = model.encode(texts, batch_size=64, show_progress_bar=True)
    embeddings = np.asarray(embeddings, dtype=np.float32)
    embeddings = normalize(embeddings)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    ensure_outdir(out_dir)
    index_path = os.path.join(out_dir, f"{table}.index")
    meta_path = os.path.join(out_dir, f"{table}_meta.jsonl")
    manifest_path = os.path.join(out_dir, f"{table}_manifest.json")

    faiss.write_index(index, index_path)

    with open(meta_path, "w", encoding="utf-8") as f:
        for i, (pk, text) in enumerate(zip(ids, texts)):
            payload = {"vector_id": i, "pk": pk, "table": table, "text": text}
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    manifest = {
        "table": table,
        "count": len(texts),
        "index_path": index_path,
        "meta_path": meta_path,
        "model_name": model_name,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "dimension": int(embeddings.shape[1]),
        "metric": "cosine",
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    return {"table": table, "count": len(texts), "index_path": index_path}


def build_embeddings(
    db_config: Dict[str, Any] = None,
    tables: List[str] = None,
    out_dir: str = "faiss_indexes",
    model_name: str = "all-MiniLM-L6-v2",
) -> List[Dict[str, Any]]:
    db_config = db_config or DEFAULT_DB_CONFIG
    tables = tables or [
        "team_squad_players",
        "stadiums",
        "player_profiles",
    ]

    resolved = [resolve_table_name(t) for t in tables]

    model = SentenceTransformer(model_name)
    conn = get_connection(db_config)
    try:
        results = []
        for t in resolved:
            print(f"Building FAISS index for table: {t}")
            res = build_table_index(conn, t, model, out_dir, model_name)
            print(f"  -> {res['count']} rows embedded; index: {res['index_path']}")
            results.append(res)
        return results
    finally:
        conn.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Create sentence-transformer embeddings per table and store in FAISS"
    )
    parser.add_argument(
        "--tables",
        nargs="*",
        default=["team_squad_player", "stadium_patch_info", "player_profile"],
        help="Table names to process (aliases resolved)",
    )
    parser.add_argument(
        "--model",
        default="all-MiniLM-L6-v2",
        help="SentenceTransformer model name",
    )
    parser.add_argument(
        "--out",
        default="faiss_indexes",
        help="Output directory for FAISS indexes",
    )
    args = parser.parse_args()

    results = build_embeddings(
        db_config=DEFAULT_DB_CONFIG,
        tables=args.tables,
        out_dir=args.out,
        model_name=args.model,
    )

    print("\nSummary:")
    for r in results:
        print(f"- {r['table']}: {r['count']} vectors -> {r['index_path']}")


if __name__ == "__main__":
    main()