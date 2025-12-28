import requests
import os

# Test video classification with improved preprocessing
print("=== Testing Video Classification API ===\n")

# Find a test video file
test_video_dir = "d:\\cricket"
video_files = [f for f in os.listdir(test_video_dir) if f.endswith(('.avi', '.mp4', '.mov'))]

if video_files:
    test_video = os.path.join(test_video_dir, video_files[0])
    print(f"Testing with video: {test_video}")
    
    # Upload and classify
    with open(test_video, 'rb') as f:
        files = {'file': (video_files[0], f, 'video/avi')}
        response = requests.post('http://localhost:8000/classify-video/', files=files)
    
    print(f"\nResponse Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"\nClassification Results:")
        print(f"  Shot Type: {result.get('shotType')}")
        print(f"  Confidence: {result.get('confidence')}%")
        print(f"\nFull Response:")
        import json
        print(json.dumps(result, indent=2))
    else:
        print(f"Error: {response.text}")
else:
    print("No test video files found in the directory")
    print("\nPlease provide a .avi, .mp4, or .mov file for testing")
