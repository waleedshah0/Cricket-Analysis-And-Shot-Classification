import requests
import json

BASE_URL = "http://localhost:8001"

def test_player_profile_fetch():
    """Test fetching individual player profiles"""
    print("Testing Player Profile Fetch\n")
    print("="*80)
    
    # Test with different player names from the database
    test_players = ["Babar Azam", "Abrar Ahmed", "Abdullah Shafique"]
    
    for player_name in test_players:
        try:
            url = f"{BASE_URL}/player-profile/{player_name}"
            print(f"\nFetching: {player_name}")
            print("-" * 80)
            
            response = requests.get(url, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Player Found: {data.get('player_name', 'N/A')}")
                print(f"Profile URL: {data.get('profile_url', 'N/A')}")
                
                # Parse batting stats
                if data.get('batting_stats'):
                    try:
                        batting_stats = json.loads(data['batting_stats']) if isinstance(data['batting_stats'], str) else data['batting_stats']
                        if isinstance(batting_stats, list) and len(batting_stats) > 0:
                            print(f"\nBatting Stats (Total Entries: {len(batting_stats)}):")
                            for i, stat in enumerate(batting_stats[:2], 1):  # Show first 2
                                print(f"  {i}. {stat.get('Game Type', 'N/A')}: {stat.get('Mat', 0)} matches, {stat.get('R', 0)} runs, Avg: {stat.get('Avg', 0)}")
                    except Exception as e:
                        print(f"Error parsing batting stats: {e}")
                
                # Parse bowling stats
                if data.get('bowling_stats'):
                    try:
                        bowling_stats = json.loads(data['bowling_stats']) if isinstance(data['bowling_stats'], str) else data['bowling_stats']
                        if isinstance(bowling_stats, list) and len(bowling_stats) > 0:
                            print(f"\nBowling Stats (Total Entries: {len(bowling_stats)}):")
                            for i, stat in enumerate(bowling_stats[:2], 1):  # Show first 2
                                print(f"  {i}. {stat.get('Game Type', 'N/A')}: {stat.get('W', 0)} wickets, Avg: {stat.get('Avg', 0)}, Economy: {stat.get('E/R', 0)}")
                    except Exception as e:
                        print(f"Error parsing bowling stats: {e}")
                
                # Parse personal info
                if data.get('personal_info'):
                    try:
                        personal_info = json.loads(data['personal_info']) if isinstance(data['personal_info'], str) else data['personal_info']
                        if isinstance(personal_info, dict):
                            print(f"\nPersonal Info:")
                            print(f"  Full Name: {personal_info.get('Full Name', 'N/A')}")
                            print(f"  Age: {personal_info.get('Age', 'N/A')}")
                            print(f"  Nationality: {personal_info.get('Nationality', 'N/A')}")
                            print(f"  Batting Style: {personal_info.get('Batting Style', 'N/A')}")
                            print(f"  Bowling Style: {personal_info.get('Bowling Style', 'N/A')}")
                    except Exception as e:
                        print(f"Error parsing personal info: {e}")
            else:
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"Exception: {e}")

    print(f"\n{'='*80}")
    print("Testing complete!")
    print(f"{'='*80}")

if __name__ == "__main__":
    test_player_profile_fetch()
