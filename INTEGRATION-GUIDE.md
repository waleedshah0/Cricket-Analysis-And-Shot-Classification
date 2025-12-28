# Cricket AI Squad - Video Classification Integration Guide

## Overview

This guide explains how the video classification functionality has been integrated into the BattingAnalysis page of the Cricket AI Squad application.

## Architecture

The application now consists of two main components:

1. **Frontend** (React/Vite application in `cricket-ai-squad-main/`)
2. **Backend** (FastAPI server in `api.py`)

## How It Works

1. **Video Upload**: When a user selects a video file in the BattingAnalysis page, it's stored in the component's state.

2. **Analysis Request**: When the user clicks "Start AI Analysis", the frontend sends the video file to the backend API endpoint `http://localhost:8000/classify-video/` using a POST request with FormData.

3. **Video Processing**: The backend API:
   - Receives the video file
   - Processes it using OpenCV to extract frames
   - Uses the TensorFlow model to classify the cricket shot
   - Returns the classification results

4. **Results Display**: The frontend receives the classification results and displays them in the UI.

## Files Modified

### Frontend Changes

- **`cricket-ai-squad-main/src/pages/BattingAnalysis.tsx`**:
  - Replaced the mock analysis function with a real API call
  - Added error handling for API requests
  - Updated the success message to include classification details

### Backend Files

- **`api.py`**: New file containing the FastAPI server with video classification functionality
- **`requirements-api.txt`**: Dependencies needed for the backend API
- **`README-API.md`**: Documentation for the backend API
- **`start-dev.bat`**: Windows batch script to start both frontend and backend servers

## Running the Application

### Method 1: Using the Batch Script (Windows)

Double-click `start-dev.bat` to automatically:
1. Install backend dependencies
2. Start the backend API server
3. Start the frontend development server

### Method 2: Manual Start

1. **Start the Backend API**:
   ```bash
   cd d:\cricket
   pip install -r requirements-api.txt
   python api.py
   ```

2. **Start the Frontend**:
   ```bash
   cd d:\cricket\cricket-ai-squad-main
   npm run dev
   ```

## API Endpoints

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000

The frontend makes requests to the backend at `http://localhost:8000/classify-video/`.

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the backend API is running and accessible.

2. **Model Loading Errors**: Make sure `model_weights.h5` is in the `d:\cricket` directory.

3. **Port Conflicts**: If ports 5173 or 8000 are in use, modify the startup scripts accordingly.

### Verifying the Setup

1. Check that `http://localhost:8000` loads the API documentation
2. Check that `http://localhost:5173/batting-analysis` loads the batting analysis page
3. Try uploading a small video file to test the classification

## Future Improvements

1. Add authentication to API endpoints
2. Implement proper error handling for different video formats
3. Add progress tracking for video processing
4. Implement caching for processed videos
5. Add more detailed analysis metrics from the TensorFlow model

## Troubleshooting

If you encounter any issues with the integration, please refer to `TROUBLESHOOTING.md` for detailed solutions to common problems including Python version compatibility, dependency installation issues, and runtime errors.