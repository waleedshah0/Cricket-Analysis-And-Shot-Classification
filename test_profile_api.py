import requests
import json

# Test with players from database
test_names = ['Babar Azam', 'Shaheen Afridi', 'Hasan Ali', 'Mohammad Rizwan']

for name in test_names:
    try:
        url = f'http://localhost:8001/player-profile/{name}'
        response = requests.get(url)
        print(f'\n{name}:')
        print(f'Status: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'Found: {data.get("player_name")}')
            print(f'Has batting_stats: {bool(data.get("batting_stats"))}')
            print(f'Has bowling_stats: {bool(data.get("bowling_stats"))}')
            if data.get('batting_stats'):
                try:
                    batting = json.loads(data.get('batting_stats')) if isinstance(data.get('batting_stats'), str) else data.get('batting_stats')
                    print(f'Batting stats items: {len(batting) if isinstance(batting, list) else 1}')
                except:
                    print('Could not parse batting stats')
        else:
            print(f'Error: {response.text[:200]}')
    except Exception as e:
        print(f'Error: {e}')
