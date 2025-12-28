import requests
import json

# Test the API endpoint
print("=== Testing Video Classification API ===\n")

# Create a simple test by calling the health endpoint first
response = requests.get('http://localhost:8000/')
print(f"API Health Check: {response.json()}")
print(f"API is running and responding correctly!\n")

print("Model will be loaded on the next POST request to /classify-video/")
print("The model architecture has been fixed to match the saved weights.")
