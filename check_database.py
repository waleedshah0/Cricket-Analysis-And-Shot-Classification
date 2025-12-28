import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'database': 'cricket_db',
    'user': 'postgres',
    'password': 'admin123',
    'port': 5432
}

def check_tables():
    """Check what tables exist in the database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check for tables
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        tables = cursor.fetchall()
        print("Tables in cricket_db:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Check team_squad_players table
        print("\n" + "="*60)
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = 'team_squad_players'
            )
        """)
        exists = cursor.fetchone()[0]
        print(f"team_squad_players table exists: {exists}")
        
        if exists:
            cursor.execute("SELECT COUNT(*) FROM team_squad_players")
            count = cursor.fetchone()[0]
            print(f"Number of records: {count}")
            
            if count > 0:
                cursor.execute("SELECT DISTINCT format FROM team_squad_players")
                formats = cursor.fetchall()
                print(f"Formats available: {[f[0] for f in formats]}")
                
                # Get sample data
                cursor.execute("""
                    SELECT id, team_name, format, player_name, image_url 
                    FROM team_squad_players 
                    LIMIT 5
                """)
                samples = cursor.fetchall()
                print("\nSample data:")
                for sample in samples:
                    print(f"  {sample}")
        
        # Check player_profiles table
        print("\n" + "="*60)
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = 'player_profiles'
            )
        """)
        exists = cursor.fetchone()[0]
        print(f"player_profiles table exists: {exists}")
        
        if exists:
            cursor.execute("SELECT COUNT(*) FROM player_profiles")
            count = cursor.fetchone()[0]
            print(f"Number of records: {count}")
            
            if count > 0:
                cursor.execute("""
                    SELECT id, player_name, profile_url, personal_info, batting_stats, bowling_stats
                    FROM player_profiles 
                    LIMIT 5
                """)
                samples = cursor.fetchall()
                print("\nSample data:")
                for sample in samples:
                    print(f"  ID: {sample[0]}, Player: {sample[1]}, Profile URL: {sample[2]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Checking Cricket Database Structure")
    print("="*60)
    check_tables()
