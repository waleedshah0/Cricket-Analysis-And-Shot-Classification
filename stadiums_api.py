from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from typing import List, Dict, Any

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'cricket_db',
    'user': 'postgres',
    'password': 'admin123',
    'port': 5432
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

@app.get("/")
async def root():
    return {"message": "Cricket Stadiums API"}

@app.get("/stadiums")
async def get_stadiums() -> List[Dict[str, Any]]:
    """Fetch all stadiums from the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute query to fetch stadiums
        cursor.execute("""
            SELECT id, ground_name, pitch_type, pitch_description, url, scraped_at 
            FROM stadiums 
            ORDER BY ground_name
        """)
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Get column names
        columns = [desc[0] for desc in cursor.description]
        
        # Convert rows to list of dictionaries
        stadiums = []
        for row in rows:
            stadium = dict(zip(columns, row))
            stadiums.append(stadium)
        
        # Close connections
        cursor.close()
        conn.close()
        
        return stadiums
        
    except Exception as e:
        print(f"Error fetching stadiums: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching stadiums: {str(e)}")

@app.get("/stadiums/{stadium_id}")
async def get_stadium(stadium_id: int) -> Dict[str, Any]:
    """Fetch a specific stadium by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute query to fetch specific stadium
        cursor.execute("""
            SELECT id, ground_name, pitch_type, pitch_description, url, scraped_at 
            FROM stadiums 
            WHERE id = %s
        """, (stadium_id,))
        
        # Fetch the row
        row = cursor.fetchone()
        
        # Close connections
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Stadium not found")
        
        # Get column names
        columns = [desc[0] for desc in cursor.description]
        
        # Convert row to dictionary
        stadium = dict(zip(columns, row))
        
        return stadium
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching stadium: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching stadium: {str(e)}")

@app.get("/players/{format}")
async def get_players_by_format(format: str) -> List[Dict[str, Any]]:
    """Fetch players by match format from team_squad_players and player_profiles"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Normalize format to match database (TEST, ODI, T20I)
        format_map = {
            'test': 'TEST',
            'odi': 'ODI',
            't20i': 'T20I',
            'Test': 'TEST',
            'ODI': 'ODI',
            'T20I': 'T20I',
            'TEST': 'TEST'
        }
        db_format = format_map.get(format, format.upper())
        
        # Execute query to fetch players by format and their profiles
        cursor.execute("""
            SELECT 
                pp.id,
                tsp.player_name,
                tsp.player_info,
                tsp.player_link,
                tsp.image_url,
                pp.personal_info,
                pp.batting_stats,
                pp.bowling_stats,
                pp.profile_url,
                pp.scraped_at
            FROM team_squad_players tsp
            LEFT JOIN player_profiles pp ON tsp.player_name = pp.player_name
            WHERE tsp.format = %s
            ORDER BY tsp.player_name
            LIMIT 15
        """, (db_format,))
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Get column names
        columns = [desc[0] for desc in cursor.description]
        
        # Convert rows to list of dictionaries
        players = []
        for idx, row in enumerate(rows):
            player = dict(zip(columns, row))
            # Add an id if not present
            if not player.get('id'):
                player['id'] = idx + 1
            players.append(player)
        
        # Close connections
        cursor.close()
        conn.close()
        
        return players
        
    except Exception as e:
        print(f"Error fetching players by format: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching players: {str(e)}")

@app.get("/player-profile/{player_name}")
async def get_player_profile(player_name: str) -> Dict[str, Any]:
    """Fetch complete player profile data"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute query to fetch player profile
        cursor.execute("""
            SELECT id, player_name, profile_url, personal_info, batting_stats, bowling_stats, scraped_at
            FROM player_profiles
            WHERE player_name = %s
        """, (player_name,))
        
        # Fetch the row
        row = cursor.fetchone()
        
        # Close connections
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Player profile not found")
        
        # Get column names
        columns = [desc[0] for desc in cursor.description]
        
        # Convert row to dictionary
        player_profile = dict(zip(columns, row))
        
        return player_profile
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching player profile: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching player profile: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)