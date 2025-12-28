#!/usr/bin/env python3
"""
Simple script to test video file upload to the API
"""

import requests
import os

def test_video_upload(file_path):
    """Test uploading a video file to the API"""
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found")
        return
    
    # Get file extension
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()
    
    print(f"Testing upload of {file_path}")
    print(f"File extension: {extension}")
    
    # Determine content type based on extension
    content_types = {
        '.mp4': 'video/mp4',
        '.avi': 'video/x-msvideo',
        '.mov': 'video/quicktime'
    }
    
    content_type = content_types.get(extension, 'application/octet-stream')
    print(f"Content type: {content_type}")
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, content_type)}
            response = requests.post('http://localhost:8000/classify-video/', files=files)
            
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("Success! Response:")
            print(response.json())
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python test-video-upload.py <video_file_path>")
        print("Example: python test-video-upload.py sample.avi")
        sys.exit(1)
    
    test_video_upload(sys.argv[1])