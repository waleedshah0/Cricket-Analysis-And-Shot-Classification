import requests
import json

def test_api():
    """Test the cricket shot classification API"""
    
    # Test the root endpoint
    try:
        response = requests.get('http://localhost:8000/')
        print(f"Root endpoint status: {response.status_code}")
        print(f"Root endpoint response: {response.json()}")
    except Exception as e:
        print(f"Error connecting to root endpoint: {e}")
        return
    
    print("\nAPI is running correctly!")
    print("To test video classification:")
    print("1. Make sure you have a short cricket video file")
    print("2. Use the frontend at http://localhost:5173/batting-analysis")
    print("3. Upload and analyze the video")
    
if __name__ == "__main__":
    test_api()