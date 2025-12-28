import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Create the cricket_db database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (not to a specific database)
        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='admin123',
            port=5432
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        with conn.cursor() as cursor:
            # Check if database exists
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'cricket_db'")
            exists = cursor.fetchone()
            
            if not exists:
                cursor.execute("CREATE DATABASE cricket_db")
                print("[OK] Database 'cricket_db' created successfully")
            else:
                print("[OK] Database 'cricket_db' already exists")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"[ERROR] Error creating database: {e}")
        return False

def create_table():
    """Create the stadiums table"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='cricket_db',
            user='postgres',
            password='admin123',
            port=5432
        )
        
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stadiums (
                    id SERIAL PRIMARY KEY,
                    ground_name VARCHAR(255) NOT NULL,
                    pitch_type VARCHAR(50),
                    pitch_description TEXT,
                    url VARCHAR(500),
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("[OK] Table 'stadiums' created successfully")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"[ERROR] Error creating table: {e}")
        return False

if __name__ == "__main__":
    print("Setting up Cricket Stadium Database...")
    print("=" * 40)
    
    if create_database():
        if create_table():
            print("\n[OK] Database setup completed successfully!")
            print("You can now run the scraper with: python cricket_scraper.py")
        else:
            print("\n[ERROR] Failed to create table")
    else:
        print("\n[ERROR] Failed to create database")
        print("Please ensure PostgreSQL is running and accessible")
