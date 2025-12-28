import requests
import json

# Test getting the 10th player (index 9) from Test format
print("=== Testing 10th Player (Index 9) ===")
response = requests.get('http://localhost:8001/players/test')

if response.status_code == 200:
    players = response.json()
    if len(players) > 9:
        player_9 = players[9]
        player_name = player_9.get('player_name')
        print(f"Player 9: {player_name}")
        print(f"Has batting_stats in list: {bool(player_9.get('batting_stats'))}")
        print(f"Has bowling_stats in list: {bool(player_9.get('bowling_stats'))}")
        
        # Now fetch the individual profile (as the frontend would)
        print(f"\n=== Fetching Individual Profile ===")
        profile_url = f'http://localhost:8001/player-profile/{player_name}'
        print(f"URL: {profile_url}")
        
        profile_response = requests.get(profile_url)
        print(f"Status: {profile_response.status_code}")
        
        if profile_response.status_code == 200:
            profile = profile_response.json()
            print(f"Profile Name: {profile.get('player_name')}")
            print(f"Image URL: {profile.get('image_url')}")
            print(f"Has batting_stats: {bool(profile.get('batting_stats'))}")
            print(f"Has bowling_stats: {bool(profile.get('bowling_stats'))}")
            
            # Try parsing batting stats
            if profile.get('batting_stats'):
                try:
                    batting = json.loads(profile.get('batting_stats')) if isinstance(profile.get('batting_stats'), str) else profile.get('batting_stats')
                    if isinstance(batting, list) and len(batting) > 0:
                        first_stat = batting[0]
                        print(f"\nFirst batting stat entry:")
                        print(f"  Game Type: {first_stat.get('Game Type')}")
                        print(f"  Matches: {first_stat.get('Mat')}")
                        print(f"  Runs: {first_stat.get('R')}")
                        print(f"  Average: {first_stat.get('Avg')}")
                except Exception as e:
                    print(f"Error parsing batting stats: {e}")
        else:
            print(f"Error fetching profile: {profile_response.status_code}")
    else:
        print(f"Not enough players. Found {len(players)}")
else:
    print(f"Error fetching players: {response.status_code}")
