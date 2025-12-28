import logging
import time
from typing import Dict, List, Optional
from urllib.parse import urljoin

import psycopg2
from psycopg2.extras import Json, execute_batch
import requests
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class PlayerProfileScraper:
    """Scrape player profile information and stats from Sportskeeda."""

    BASE_URL = "https://www.sportskeeda.com"

    def __init__(self, db_config: Dict[str, str], delay_seconds: float = 1.5):
        self.db_config = db_config
        self.delay_seconds = delay_seconds

        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/123.0 Safari/537.36"
                )
            }
        )

    # ------------------------------------------------------------------
    # Database helpers
    # ------------------------------------------------------------------
    def get_db_connection(self):
        try:
            return psycopg2.connect(
                host=self.db_config["host"],
                database=self.db_config["database"],
                user=self.db_config["user"],
                password=self.db_config["password"],
                port=self.db_config["port"],
            )
        except Exception as exc:
            logger.error("Database connection failed: %s", exc)
            return None

    def create_table(self) -> bool:
        conn = self.get_db_connection()
        if not conn:
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS player_profiles (
                        id SERIAL PRIMARY KEY,
                        player_name VARCHAR(255) NOT NULL,
                        profile_url VARCHAR(500) NOT NULL UNIQUE,
                        personal_info JSONB,
                        batting_stats JSONB,
                        bowling_stats JSONB,
                        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
            conn.commit()
            logger.info("Ensured player_profiles table exists")
            return True
        except Exception as exc:
            conn.rollback()
            logger.error("Error creating player_profiles table: %s", exc)
            return False
        finally:
            conn.close()

    def fetch_player_urls(self) -> List[Dict[str, str]]:
        conn = self.get_db_connection()
        if not conn:
            return []

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT DISTINCT ON (player_link) player_name, player_link
                    FROM team_squad_players
                    WHERE player_link IS NOT NULL
                    ORDER BY player_link, player_name
                    """
                )
                rows = cursor.fetchall()

                players = []
                for name, link in rows:
                    if not link:
                        continue
                    absolute = self.ensure_absolute_url(link)
                    players.append({"player_name": name, "profile_url": absolute})

                logger.info("Loaded %d player profile URLs", len(players))
                return players
        except Exception as exc:
            logger.error("Error fetching player URLs: %s", exc)
            return []
        finally:
            conn.close()

    def ensure_absolute_url(self, link: str) -> str:
        if link.startswith("http://") or link.startswith("https://"):
            return link
        return urljoin(self.BASE_URL, link)

    # ------------------------------------------------------------------
    # Scraping helpers
    # ------------------------------------------------------------------
    def fetch_profile_page(self, url: str) -> Optional[str]:
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as exc:
            logger.error("Failed to fetch %s: %s", url, exc)
            return None

    def parse_personal_info(self, soup: BeautifulSoup) -> Dict[str, str]:
        data: Dict[str, str] = {}
        heading = soup.find(
            lambda tag: tag.name in ("h2", "h3")
            and "personal information" in tag.get_text(strip=True).lower()
        )
        if not heading:
            return data

        table = heading.find_next("table")
        if not table:
            return data

        for row in table.find_all("tr"):
            cells = [cell.get_text(" ", strip=True) for cell in row.find_all("td")]
            if not cells:
                continue

            for idx in range(0, len(cells), 2):
                label = cells[idx].strip()
                value = cells[idx + 1].strip() if idx + 1 < len(cells) else ""
                if label:
                    data[label] = value
        return data

    def parse_stats(self, soup: BeautifulSoup, heading_text: str) -> List[Dict[str, str]]:
        heading = soup.find(
            lambda tag: tag.name in ("h2", "h3")
            and heading_text.lower() in tag.get_text(strip=True).lower()
        )
        if not heading:
            return []

        table = heading.find_next("table", class_="stats-table")
        if not table:
            return []

        headers = [th.get_text(" ", strip=True) for th in table.find_all("th")]
        stats: List[Dict[str, str]] = []
        for row in table.find_all("tr")[1:]:
            cells = [cell.get_text(" ", strip=True) for cell in row.find_all("td")]
            if not cells:
                continue
            row_data = {header: value for header, value in zip(headers, cells)}
            stats.append(row_data)
        return stats

    def scrape_profile(self, player: Dict[str, str]) -> Optional[Dict[str, object]]:
        url = player["profile_url"]
        html = self.fetch_profile_page(url)
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")

        personal_info = self.parse_personal_info(soup)
        batting_stats = self.parse_stats(soup, "Batting Stats")
        bowling_stats = self.parse_stats(soup, "Bowling Stats")

        return {
            "player_name": player["player_name"],
            "profile_url": url,
            "personal_info": personal_info,
            "batting_stats": batting_stats,
            "bowling_stats": bowling_stats,
        }

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def save_profiles(self, profiles: List[Dict[str, object]]) -> bool:
        if not profiles:
            logger.warning("No profiles to save")
            return False

        conn = self.get_db_connection()
        if not conn:
            return False

        try:
            with conn.cursor() as cursor:
                execute_batch(
                    cursor,
                    """
                    INSERT INTO player_profiles (
                        player_name,
                        profile_url,
                        personal_info,
                        batting_stats,
                        bowling_stats
                    ) VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (profile_url) DO UPDATE SET
                        player_name = EXCLUDED.player_name,
                        personal_info = EXCLUDED.personal_info,
                        batting_stats = EXCLUDED.batting_stats,
                        bowling_stats = EXCLUDED.bowling_stats,
                        scraped_at = NOW()
                    """,
                    [
                        (
                            profile["player_name"],
                            profile["profile_url"],
                            Json(profile.get("personal_info") or {}),
                            Json(profile.get("batting_stats") or []),
                            Json(profile.get("bowling_stats") or []),
                        )
                        for profile in profiles
                    ],
                )
            conn.commit()
            logger.info("Saved %d player profiles", len(profiles))
            return True
        except Exception as exc:
            conn.rollback()
            logger.error("Error saving profiles: %s", exc)
            return False
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Orchestration
    # ------------------------------------------------------------------
    def scrape_all(self) -> bool:
        if not self.create_table():
            return False

        players = self.fetch_player_urls()
        if not players:
            logger.error("No player URLs found in database")
            return False

        scraped: List[Dict[str, object]] = []
        for index, player in enumerate(players, start=1):
            logger.info("(%d/%d) Scraping %s", index, len(players), player["player_name"])
            profile = self.scrape_profile(player)
            if profile:
                scraped.append(profile)
            else:
                logger.error("Failed to scrape %s", player["profile_url"])
            time.sleep(self.delay_seconds)

        return self.save_profiles(scraped)


def main():
    db_config = {
        "host": "localhost",
        "database": "cricket_db",
        "user": "postgres",
        "password": "admin123",
        "port": 5432,
    }

    scraper = PlayerProfileScraper(db_config)
    success = scraper.scrape_all()

    if success:
        logger.info("Player profile scraping completed successfully")
    else:
        logger.error("Player profile scraping failed")


if __name__ == "__main__":
    main()

