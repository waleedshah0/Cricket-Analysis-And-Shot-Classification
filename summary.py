import psycopg2
from psycopg2.extras import RealDictCursor

def show_final_summary():
    """Show final summary of the scraping results"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='cricket_db',
            user='postgres',
            password='admin123',
            port=5432
        )
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            print("CRICKET STADIUM PITCH SCRAPING SUMMARY")
            print("=" * 50)
            
            # Total count
            cursor.execute("SELECT COUNT(*) as total FROM stadiums")
            total = cursor.fetchone()['total']
            print(f"Total Stadiums Scraped: {total}")
            
            # Pitch type breakdown
            cursor.execute("""
                SELECT 
                    pitch_type,
                    COUNT(*) as count,
                    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM stadiums), 2) as percentage
                FROM stadiums 
                WHERE pitch_type IS NOT NULL 
                GROUP BY pitch_type 
                ORDER BY count DESC
            """)
            
            print("\nPitch Type Distribution:")
            print("-" * 30)
            for row in cursor.fetchall():
                print(f"{row['pitch_type']:12} | {row['count']:3} stadiums ({row['percentage']:5}%)")
            
            # Countries/Regions represented
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN ground_name ILIKE '%india%' OR ground_name ILIKE '%mumbai%' OR ground_name ILIKE '%delhi%' OR ground_name ILIKE '%bangalore%' OR ground_name ILIKE '%hyderabad%' OR ground_name ILIKE '%kolkata%' OR ground_name ILIKE '%chennai%' OR ground_name ILIKE '%rajasthan%' OR ground_name ILIKE '%punjab%' OR ground_name ILIKE '%gujarat%' OR ground_name ILIKE '%uttar pradesh%' OR ground_name ILIKE '%madhya pradesh%' OR ground_name ILIKE '%maharashtra%' OR ground_name ILIKE '%karnataka%' OR ground_name ILIKE '%tamil nadu%' OR ground_name ILIKE '%west bengal%' OR ground_name ILIKE '%rajasthan%' OR ground_name ILIKE '%punjab%' OR ground_name ILIKE '%gujarat%' OR ground_name ILIKE '%uttar pradesh%' OR ground_name ILIKE '%madhya pradesh%' OR ground_name ILIKE '%maharashtra%' OR ground_name ILIKE '%karnataka%' OR ground_name ILIKE '%tamil nadu%' OR ground_name ILIKE '%west bengal%' THEN 'India'
                        WHEN ground_name ILIKE '%australia%' OR ground_name ILIKE '%melbourne%' OR ground_name ILIKE '%sydney%' OR ground_name ILIKE '%perth%' OR ground_name ILIKE '%adelaide%' OR ground_name ILIKE '%brisbane%' THEN 'Australia'
                        WHEN ground_name ILIKE '%england%' OR ground_name ILIKE '%london%' OR ground_name ILIKE '%manchester%' OR ground_name ILIKE '%birmingham%' OR ground_name ILIKE '%nottingham%' OR ground_name ILIKE '%leeds%' OR ground_name ILIKE '%southampton%' OR ground_name ILIKE '%lords%' OR ground_name ILIKE '%edgbaston%' OR ground_name ILIKE '%old trafford%' OR ground_name ILIKE '%trent bridge%' OR ground_name ILIKE '%headingley%' OR ground_name ILIKE '%rose bowl%' THEN 'England'
                        WHEN ground_name ILIKE '%pakistan%' OR ground_name ILIKE '%karachi%' OR ground_name ILIKE '%lahore%' OR ground_name ILIKE '%islamabad%' OR ground_name ILIKE '%rawalpindi%' OR ground_name ILIKE '%multan%' OR ground_name ILIKE '%gaddafi%' THEN 'Pakistan'
                        WHEN ground_name ILIKE '%sri lanka%' OR ground_name ILIKE '%colombo%' OR ground_name ILIKE '%galle%' OR ground_name ILIKE '%kandy%' OR ground_name ILIKE '%pallekele%' OR ground_name ILIKE '%premadasa%' THEN 'Sri Lanka'
                        WHEN ground_name ILIKE '%new zealand%' OR ground_name ILIKE '%auckland%' OR ground_name ILIKE '%wellington%' OR ground_name ILIKE '%christchurch%' OR ground_name ILIKE '%nelson%' OR ground_name ILIKE '%mount maunganui%' THEN 'New Zealand'
                        WHEN ground_name ILIKE '%south africa%' OR ground_name ILIKE '%cape town%' OR ground_name ILIKE '%johannesburg%' OR ground_name ILIKE '%durban%' OR ground_name ILIKE '%pretoria%' OR ground_name ILIKE '%newlands%' OR ground_name ILIKE '%wanderers%' OR ground_name ILIKE '%supersport%' THEN 'South Africa'
                        WHEN ground_name ILIKE '%bangladesh%' OR ground_name ILIKE '%dhaka%' OR ground_name ILIKE '%chittagong%' OR ground_name ILIKE '%chowdhury%' THEN 'Bangladesh'
                        WHEN ground_name ILIKE '%uae%' OR ground_name ILIKE '%dubai%' OR ground_name ILIKE '%abu dhabi%' OR ground_name ILIKE '%zayed%' THEN 'UAE'
                        WHEN ground_name ILIKE '%usa%' OR ground_name ILIKE '%america%' OR ground_name ILIKE '%texas%' OR ground_name ILIKE '%nassau%' THEN 'USA'
                        WHEN ground_name ILIKE '%west indies%' OR ground_name ILIKE '%trinidad%' OR ground_name ILIKE '%barbados%' OR ground_name ILIKE '%jamaica%' OR ground_name ILIKE '%queens park%' THEN 'West Indies'
                        ELSE 'Other'
                    END as country,
                    COUNT(*) as count
                FROM stadiums 
                GROUP BY 
                    CASE 
                        WHEN ground_name ILIKE '%india%' OR ground_name ILIKE '%mumbai%' OR ground_name ILIKE '%delhi%' OR ground_name ILIKE '%bangalore%' OR ground_name ILIKE '%hyderabad%' OR ground_name ILIKE '%kolkata%' OR ground_name ILIKE '%chennai%' OR ground_name ILIKE '%rajasthan%' OR ground_name ILIKE '%punjab%' OR ground_name ILIKE '%gujarat%' OR ground_name ILIKE '%uttar pradesh%' OR ground_name ILIKE '%madhya pradesh%' OR ground_name ILIKE '%maharashtra%' OR ground_name ILIKE '%karnataka%' OR ground_name ILIKE '%tamil nadu%' OR ground_name ILIKE '%west bengal%' OR ground_name ILIKE '%rajasthan%' OR ground_name ILIKE '%punjab%' OR ground_name ILIKE '%gujarat%' OR ground_name ILIKE '%uttar pradesh%' OR ground_name ILIKE '%madhya pradesh%' OR ground_name ILIKE '%maharashtra%' OR ground_name ILIKE '%karnataka%' OR ground_name ILIKE '%tamil nadu%' OR ground_name ILIKE '%west bengal%' THEN 'India'
                        WHEN ground_name ILIKE '%australia%' OR ground_name ILIKE '%melbourne%' OR ground_name ILIKE '%sydney%' OR ground_name ILIKE '%perth%' OR ground_name ILIKE '%adelaide%' OR ground_name ILIKE '%brisbane%' THEN 'Australia'
                        WHEN ground_name ILIKE '%england%' OR ground_name ILIKE '%london%' OR ground_name ILIKE '%manchester%' OR ground_name ILIKE '%birmingham%' OR ground_name ILIKE '%nottingham%' OR ground_name ILIKE '%leeds%' OR ground_name ILIKE '%southampton%' OR ground_name ILIKE '%lords%' OR ground_name ILIKE '%edgbaston%' OR ground_name ILIKE '%old trafford%' OR ground_name ILIKE '%trent bridge%' OR ground_name ILIKE '%headingley%' OR ground_name ILIKE '%rose bowl%' THEN 'England'
                        WHEN ground_name ILIKE '%pakistan%' OR ground_name ILIKE '%karachi%' OR ground_name ILIKE '%lahore%' OR ground_name ILIKE '%islamabad%' OR ground_name ILIKE '%rawalpindi%' OR ground_name ILIKE '%multan%' OR ground_name ILIKE '%gaddafi%' THEN 'Pakistan'
                        WHEN ground_name ILIKE '%sri lanka%' OR ground_name ILIKE '%colombo%' OR ground_name ILIKE '%galle%' OR ground_name ILIKE '%kandy%' OR ground_name ILIKE '%pallekele%' OR ground_name ILIKE '%premadasa%' THEN 'Sri Lanka'
                        WHEN ground_name ILIKE '%new zealand%' OR ground_name ILIKE '%auckland%' OR ground_name ILIKE '%wellington%' OR ground_name ILIKE '%christchurch%' OR ground_name ILIKE '%nelson%' OR ground_name ILIKE '%mount maunganui%' THEN 'New Zealand'
                        WHEN ground_name ILIKE '%south africa%' OR ground_name ILIKE '%cape town%' OR ground_name ILIKE '%johannesburg%' OR ground_name ILIKE '%durban%' OR ground_name ILIKE '%pretoria%' OR ground_name ILIKE '%newlands%' OR ground_name ILIKE '%wanderers%' OR ground_name ILIKE '%supersport%' THEN 'South Africa'
                        WHEN ground_name ILIKE '%bangladesh%' OR ground_name ILIKE '%dhaka%' OR ground_name ILIKE '%chittagong%' OR ground_name ILIKE '%chowdhury%' THEN 'Bangladesh'
                        WHEN ground_name ILIKE '%uae%' OR ground_name ILIKE '%dubai%' OR ground_name ILIKE '%abu dhabi%' OR ground_name ILIKE '%zayed%' THEN 'UAE'
                        WHEN ground_name ILIKE '%usa%' OR ground_name ILIKE '%america%' OR ground_name ILIKE '%texas%' OR ground_name ILIKE '%nassau%' THEN 'USA'
                        WHEN ground_name ILIKE '%west indies%' OR ground_name ILIKE '%trinidad%' OR ground_name ILIKE '%barbados%' OR ground_name ILIKE '%jamaica%' OR ground_name ILIKE '%queens park%' THEN 'West Indies'
                        ELSE 'Other'
                    END
                ORDER BY count DESC
            """)
            
            print("\nStadiums by Country/Region:")
            print("-" * 30)
            for row in cursor.fetchall():
                print(f"{row['country']:15} | {row['count']:3} stadiums")
            
            # Most common pitch types by country
            print("\nTop Batting-Friendly Countries:")
            print("-" * 30)
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN ground_name ILIKE '%india%' OR ground_name ILIKE '%mumbai%' OR ground_name ILIKE '%delhi%' OR ground_name ILIKE '%bangalore%' OR ground_name ILIKE '%hyderabad%' OR ground_name ILIKE '%kolkata%' OR ground_name ILIKE '%chennai%' OR ground_name ILIKE '%rajasthan%' OR ground_name ILIKE '%punjab%' OR ground_name ILIKE '%gujarat%' OR ground_name ILIKE '%uttar pradesh%' OR ground_name ILIKE '%madhya pradesh%' OR ground_name ILIKE '%maharashtra%' OR ground_name ILIKE '%karnataka%' OR ground_name ILIKE '%tamil nadu%' OR ground_name ILIKE '%west bengal%' THEN 'India'
                        WHEN ground_name ILIKE '%australia%' OR ground_name ILIKE '%melbourne%' OR ground_name ILIKE '%sydney%' OR ground_name ILIKE '%perth%' OR ground_name ILIKE '%adelaide%' OR ground_name ILIKE '%brisbane%' THEN 'Australia'
                        WHEN ground_name ILIKE '%england%' OR ground_name ILIKE '%london%' OR ground_name ILIKE '%manchester%' OR ground_name ILIKE '%birmingham%' OR ground_name ILIKE '%nottingham%' OR ground_name ILIKE '%leeds%' OR ground_name ILIKE '%southampton%' OR ground_name ILIKE '%lords%' OR ground_name ILIKE '%edgbaston%' OR ground_name ILIKE '%old trafford%' OR ground_name ILIKE '%trent bridge%' OR ground_name ILIKE '%headingley%' OR ground_name ILIKE '%rose bowl%' THEN 'England'
                        WHEN ground_name ILIKE '%pakistan%' OR ground_name ILIKE '%karachi%' OR ground_name ILIKE '%lahore%' OR ground_name ILIKE '%islamabad%' OR ground_name ILIKE '%rawalpindi%' OR ground_name ILIKE '%multan%' OR ground_name ILIKE '%gaddafi%' THEN 'Pakistan'
                        WHEN ground_name ILIKE '%sri lanka%' OR ground_name ILIKE '%colombo%' OR ground_name ILIKE '%galle%' OR ground_name ILIKE '%kandy%' OR ground_name ILIKE '%pallekele%' OR ground_name ILIKE '%premadasa%' THEN 'Sri Lanka'
                        WHEN ground_name ILIKE '%new zealand%' OR ground_name ILIKE '%auckland%' OR ground_name ILIKE '%wellington%' OR ground_name ILIKE '%christchurch%' OR ground_name ILIKE '%nelson%' OR ground_name ILIKE '%mount maunganui%' THEN 'New Zealand'
                        WHEN ground_name ILIKE '%south africa%' OR ground_name ILIKE '%cape town%' OR ground_name ILIKE '%johannesburg%' OR ground_name ILIKE '%durban%' OR ground_name ILIKE '%pretoria%' OR ground_name ILIKE '%newlands%' OR ground_name ILIKE '%wanderers%' OR ground_name ILIKE '%supersport%' THEN 'South Africa'
                        WHEN ground_name ILIKE '%bangladesh%' OR ground_name ILIKE '%dhaka%' OR ground_name ILIKE '%chittagong%' OR ground_name ILIKE '%chowdhury%' THEN 'Bangladesh'
                        WHEN ground_name ILIKE '%uae%' OR ground_name ILIKE '%dubai%' OR ground_name ILIKE '%abu dhabi%' OR ground_name ILIKE '%zayed%' THEN 'UAE'
                        WHEN ground_name ILIKE '%usa%' OR ground_name ILIKE '%america%' OR ground_name ILIKE '%texas%' OR ground_name ILIKE '%nassau%' THEN 'USA'
                        WHEN ground_name ILIKE '%west indies%' OR ground_name ILIKE '%trinidad%' OR ground_name ILIKE '%barbados%' OR ground_name ILIKE '%jamaica%' OR ground_name ILIKE '%queens park%' THEN 'West Indies'
                        ELSE 'Other'
                    END as country,
                    COUNT(*) as batting_count
                FROM stadiums 
                WHERE pitch_type = 'Batting'
                GROUP BY 
                    CASE 
                        WHEN ground_name ILIKE '%india%' OR ground_name ILIKE '%mumbai%' OR ground_name ILIKE '%delhi%' OR ground_name ILIKE '%bangalore%' OR ground_name ILIKE '%hyderabad%' OR ground_name ILIKE '%kolkata%' OR ground_name ILIKE '%chennai%' OR ground_name ILIKE '%rajasthan%' OR ground_name ILIKE '%punjab%' OR ground_name ILIKE '%gujarat%' OR ground_name ILIKE '%uttar pradesh%' OR ground_name ILIKE '%madhya pradesh%' OR ground_name ILIKE '%maharashtra%' OR ground_name ILIKE '%karnataka%' OR ground_name ILIKE '%tamil nadu%' OR ground_name ILIKE '%west bengal%' THEN 'India'
                        WHEN ground_name ILIKE '%australia%' OR ground_name ILIKE '%melbourne%' OR ground_name ILIKE '%sydney%' OR ground_name ILIKE '%perth%' OR ground_name ILIKE '%adelaide%' OR ground_name ILIKE '%brisbane%' THEN 'Australia'
                        WHEN ground_name ILIKE '%england%' OR ground_name ILIKE '%london%' OR ground_name ILIKE '%manchester%' OR ground_name ILIKE '%birmingham%' OR ground_name ILIKE '%nottingham%' OR ground_name ILIKE '%leeds%' OR ground_name ILIKE '%southampton%' OR ground_name ILIKE '%lords%' OR ground_name ILIKE '%edgbaston%' OR ground_name ILIKE '%old trafford%' OR ground_name ILIKE '%trent bridge%' OR ground_name ILIKE '%headingley%' OR ground_name ILIKE '%rose bowl%' THEN 'England'
                        WHEN ground_name ILIKE '%pakistan%' OR ground_name ILIKE '%karachi%' OR ground_name ILIKE '%lahore%' OR ground_name ILIKE '%islamabad%' OR ground_name ILIKE '%rawalpindi%' OR ground_name ILIKE '%multan%' OR ground_name ILIKE '%gaddafi%' THEN 'Pakistan'
                        WHEN ground_name ILIKE '%sri lanka%' OR ground_name ILIKE '%colombo%' OR ground_name ILIKE '%galle%' OR ground_name ILIKE '%kandy%' OR ground_name ILIKE '%pallekele%' OR ground_name ILIKE '%premadasa%' THEN 'Sri Lanka'
                        WHEN ground_name ILIKE '%new zealand%' OR ground_name ILIKE '%auckland%' OR ground_name ILIKE '%wellington%' OR ground_name ILIKE '%christchurch%' OR ground_name ILIKE '%nelson%' OR ground_name ILIKE '%mount maunganui%' THEN 'New Zealand'
                        WHEN ground_name ILIKE '%south africa%' OR ground_name ILIKE '%cape town%' OR ground_name ILIKE '%johannesburg%' OR ground_name ILIKE '%durban%' OR ground_name ILIKE '%pretoria%' OR ground_name ILIKE '%newlands%' OR ground_name ILIKE '%wanderers%' OR ground_name ILIKE '%supersport%' THEN 'South Africa'
                        WHEN ground_name ILIKE '%bangladesh%' OR ground_name ILIKE '%dhaka%' OR ground_name ILIKE '%chittagong%' OR ground_name ILIKE '%chowdhury%' THEN 'Bangladesh'
                        WHEN ground_name ILIKE '%uae%' OR ground_name ILIKE '%dubai%' OR ground_name ILIKE '%abu dhabi%' OR ground_name ILIKE '%zayed%' THEN 'UAE'
                        WHEN ground_name ILIKE '%usa%' OR ground_name ILIKE '%america%' OR ground_name ILIKE '%texas%' OR ground_name ILIKE '%nassau%' THEN 'USA'
                        WHEN ground_name ILIKE '%west indies%' OR ground_name ILIKE '%trinidad%' OR ground_name ILIKE '%barbados%' OR ground_name ILIKE '%jamaica%' OR ground_name ILIKE '%queens park%' THEN 'West Indies'
                        ELSE 'Other'
                    END
                ORDER BY batting_count DESC
                LIMIT 5
            """)
            
            for row in cursor.fetchall():
                print(f"{row['country']:15} | {row['batting_count']:3} batting-friendly stadiums")
        
        conn.close()
        print("\n" + "=" * 50)
        print("Scraping completed successfully!")
        print("Data is now available in the 'cricket_db' database.")
        
    except Exception as e:
        print(f"Error showing summary: {e}")

if __name__ == "__main__":
    show_final_summary()
