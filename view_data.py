import psycopg2
from psycopg2.extras import RealDictCursor

def view_scraped_data():
    """View the scraped stadium data"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='cricket_db',
            user='postgres',
            password='admin123',
            port=5432
        )
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Get total count
            cursor.execute("SELECT COUNT(*) as total FROM stadiums")
            total = cursor.fetchone()['total']
            print(f"Total stadiums scraped: {total}")
            print("=" * 80)
            
            # Get pitch type distribution
            cursor.execute("""
                SELECT pitch_type, COUNT(*) as count 
                FROM stadiums 
                WHERE pitch_type IS NOT NULL 
                GROUP BY pitch_type 
                ORDER BY count DESC
            """)
            print("Pitch Type Distribution:")
            for row in cursor.fetchall():
                print(f"  {row['pitch_type']}: {row['count']} stadiums")
            print()
            
            # Show sample data
            cursor.execute("""
                SELECT ground_name, pitch_type, pitch_description, url 
                FROM stadiums 
                ORDER BY scraped_at DESC 
                LIMIT 10
            """)
            
            print("Sample Data (Latest 10 entries):")
            print("-" * 80)
            
            for row in cursor.fetchall():
                print(f"Ground: {row['ground_name']}")
                print(f"Pitch Type: {row['pitch_type']}")
                print(f"Description: {row['pitch_description'][:100]}...")
                print(f"URL: {row['url']}")
                print("-" * 80)
        
        conn.close()
        
    except Exception as e:
        print(f"Error viewing data: {e}")

if __name__ == "__main__":
    view_scraped_data()
