import requests
import json

# Test getting players for a format first
print("=== Testing Players by Format ===")
response = requests.get('http://localhost:8001/players/test')
if response.status_code == 200:
    players = response.json()
    print(f"Found {len(players)} players for Test format")
    
    # Show first 3 and one from beyond 8
    for idx, player in enumerate(players):
        if idx < 3 or idx == 9:  # First 3 and the 10th player
            print(f"\nPlayer {idx}: {player.get('player_name')}")
            print(f"  ID: {player.get('id')}")
            print(f"  Has batting_stats: {bool(player.get('batting_stats'))}")
            print(f"  Has bowling_stats: {bool(player.get('bowling_stats'))}")
            
            # Try to fetch individual profile
            player_name = player.get('player_name')
            print(f"\n  === Testing individual profile fetch for {player_name} ===")
            profile_response = requests.get(f'http://localhost:8001/player-profile/{player_name}')
            if profile_response.status_code == 200:
                profile = profile_response.json()
                print(f"  Profile Status: 200")
                print(f"  Profile has batting_stats: {bool(profile.get('batting_stats'))}")
                print(f"  Profile has bowling_stats: {bool(profile.get('bowling_stats'))}")
                
                # Try parsing stats
                if profile.get('batting_stats'):
                    try:
                        batting = json.loads(profile.get('batting_stats')) if isinstance(profile.get('batting_stats'), str) else profile.get('batting_stats')
                        print(f"  Batting stats parsed: {type(batting)}, count={len(batting) if isinstance(batting, list) else 'N/A'}")
                    except Exception as e:
                        print(f"  Error parsing batting stats: {e}")
            else:
                print(f"  Profile Status: {profile_response.status_code}")
else:
    print(f"Error fetching players: {response.status_code}")
