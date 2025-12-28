import requests
import json

# Test the squad API endpoints
BASE_URL = "http://localhost:8001"

def test_players_by_format(format_name):
    """Test fetching players by format"""
    try:
        url = f"{BASE_URL}/players/{format_name}"
        print(f"\n{'='*60}")
        print(f"Testing: GET {url}")
        print(f"{'='*60}")
        
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Number of players returned: {len(data)}")
            
            if data:
                print(f"\nFirst player data:")
                first_player = data[0]
                print(json.dumps(first_player, indent=2, default=str))
                
                print(f"\nSummary of all {len(data)} players:")
                for i, player in enumerate(data[:5], 1):
                    print(f"  {i}. {player.get('player_name', 'N/A')} - ID: {player.get('id', 'N/A')}")
                
                if len(data) > 5:
                    print(f"  ... and {len(data) - 5} more players")
            else:
                print("No players found for this format.")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

def test_stadiums():
    """Test fetching stadiums"""
    try:
        url = f"{BASE_URL}/stadiums"
        print(f"\n{'='*60}")
        print(f"Testing: GET {url}")
        print(f"{'='*60}")
        
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Number of stadiums returned: {len(data)}")
            
            if data:
                print(f"\nFirst stadium data:")
                first_stadium = data[0]
                print(json.dumps(first_stadium, indent=2, default=str))
            else:
                print("No stadiums found.")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

def test_api_health():
    """Test API health"""
    try:
        url = f"{BASE_URL}/"
        print(f"\n{'='*60}")
        print(f"Testing: GET {url}")
        print(f"{'='*60}")
        
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    print("Testing Cricket Squad API")
    
    # Test API health
    test_api_health()
    
    # Test stadiums
    test_stadiums()
    
    # Test players by format
    test_players_by_format("Test")
    test_players_by_format("ODI")
    test_players_by_format("T20I")
    
    print(f"\n{'='*60}")
    print("Testing complete!")
    print(f"{'='*60}")
