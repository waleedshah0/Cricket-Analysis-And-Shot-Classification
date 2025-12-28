import psycopg2
from cricket_scraper import CricketStadiumScraper

def test_database_connection():
    """Test database connection"""
    db_config = {
        'host': 'localhost',
        'database': 'cricket_db',
        'user': 'postgres',
        'password': 'admin123',
        'port': 5432
    }
    
    try:
        conn = psycopg2.connect(**db_config)
        print("[OK] Database connection successful")
        conn.close()
        return True
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        return False

def test_scraper():
    """Test the scraper with a single stadium"""
    db_config = {
        'host': 'localhost',
        'database': 'cricket_db',
        'user': 'postgres',
        'password': 'admin123',
        'port': 5432
    }
    
    scraper = CricketStadiumScraper(db_config)
    
    # Test with a single stadium URL
    test_url = "https://pitch-report.com/rajiv-gandhi-international-stadium-pitch-report/"
    
    print(f"Testing scraper with URL: {test_url}")
    
    # Extract pitch info
    stadium_data = scraper.extract_pitch_info(test_url)
    
    if stadium_data:
        print("[OK] Successfully extracted stadium data:")
        print(f"  Ground Name: {stadium_data['ground_name']}")
        print(f"  Pitch Type: {stadium_data['pitch_type']}")
        print(f"  Description: {stadium_data['pitch_description'][:100]}...")
        
        # Test database save
        if scraper.save_to_database(stadium_data):
            print("[OK] Successfully saved to database")
        else:
            print("[ERROR] Failed to save to database")
    else:
        print("[ERROR] Failed to extract stadium data")

if __name__ == "__main__":
    print("Testing Cricket Stadium Scraper...")
    print("=" * 50)
    
    # Test database connection
    if test_database_connection():
        # Test scraper
        test_scraper()
    else:
        print("Please ensure PostgreSQL is running and the database 'cricket_db' exists")
        print("You can create the database with: CREATE DATABASE cricket_db;")
