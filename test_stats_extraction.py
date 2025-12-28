import psycopg2
import json

DB_CONFIG = {
    'host': 'localhost',
    'database': 'cricket_db',
    'user': 'postgres',
    'password': 'admin123',
    'port': 5432
}

def extract_stats_from_array(stats_array, format_to_match=None):
    """Simulate the TypeScript function in Python"""
    if not isinstance(stats_array, list) or len(stats_array) == 0:
        return None
    
    selected_stats = None
    
    # Try to match the current format
    if format_to_match:
        for s in stats_array:
            game_type = (s.get('Game Type', '') or '').upper()
            if format_to_match.upper() in game_type:
                selected_stats = s
                break
    
    # If no match, use the first comprehensive stats
    if not selected_stats:
        for s in stats_array:
            game_type = (s.get('Game Type', '') or '').upper()
            if game_type in ['FIRSTCLASS', 'TESTS', 'ODIS', 'T20IS']:
                selected_stats = s
                break
        if not selected_stats:
            selected_stats = stats_array[0]
    
    return selected_stats

def test_format(format_name):
    """Test extracting stats for a specific format"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Normalize format
        format_map = {
            'test': 'TEST',
            'odi': 'ODI',
            't20i': 'T20I',
        }
        db_format = format_map.get(format_name.lower(), format_name.upper())
        
        # Fetch players for this format
        cursor.execute("""
            SELECT 
                pp.player_name,
                pp.batting_stats,
                pp.bowling_stats
            FROM team_squad_players tsp
            LEFT JOIN player_profiles pp ON tsp.player_name = pp.player_name
            WHERE tsp.format = %s
            LIMIT 3
        """, (db_format,))
        
        rows = cursor.fetchall()
        
        print(f"\n{'='*80}")
        print(f"FORMAT: {format_name}")
        print(f"{'='*80}")
        print(f"Found {len(rows)} players\n")
        
        for i, row in enumerate(rows, 1):
            player_name = row[0]
            batting_stats_raw = row[1]
            bowling_stats_raw = row[2]
            
            print(f"{i}. {player_name}")
            print("-" * 80)
            
            # Parse and extract batting stats
            if batting_stats_raw:
                try:
                    batting_stats = json.loads(batting_stats_raw) if isinstance(batting_stats_raw, str) else batting_stats_raw
                    extracted = extract_stats_from_array(batting_stats, format_name)
                    if extracted:
                        print(f"   Batting Stats:")
                        print(f"     - Matches: {extracted.get('Mat', '0')}")
                        print(f"     - Runs: {extracted.get('R', '0')}")
                        print(f"     - Average: {extracted.get('Avg', '0')}")
                        print(f"     - Strike Rate: {extracted.get('S/R', '0')}")
                        print(f"     - Game Type: {extracted.get('Game Type', 'N/A')}")
                except Exception as e:
                    print(f"   Error parsing batting stats: {e}")
            
            # Parse and extract bowling stats
            if bowling_stats_raw:
                try:
                    bowling_stats = json.loads(bowling_stats_raw) if isinstance(bowling_stats_raw, str) else bowling_stats_raw
                    extracted = extract_stats_from_array(bowling_stats, format_name)
                    if extracted:
                        print(f"   Bowling Stats:")
                        print(f"     - Matches: {extracted.get('Mat', '0')}")
                        print(f"     - Wickets: {extracted.get('W', '0')}")
                        print(f"     - Average: {extracted.get('Avg', '0')}")
                        print(f"     - Economy: {extracted.get('E/R', '0')}")
                        print(f"     - Game Type: {extracted.get('Game Type', 'N/A')}")
                except Exception as e:
                    print(f"   Error parsing bowling stats: {e}")
            
            print()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing Stats Extraction from Database")
    
    test_format("Test")
    test_format("ODI")
    test_format("T20I")
    
    print(f"\n{'='*80}")
    print("Testing complete!")
    print(f"{'='*80}")
