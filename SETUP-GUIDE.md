# Cricket AI Squad - Complete Setup Guide

## Overview

This guide provides step-by-step instructions for setting up the Cricket AI Squad application with video classification functionality.

## Prerequisites

1. **Python 3.9 or higher** (Python 3.9.0 is confirmed to work)
2. **Node.js and npm** (for the frontend)
3. **Git** (optional, for version control)

## Quick Start

For the fastest setup, you have two options:

1. **Regular setup** (if you already have a working environment):
   ```cmd
   setup-environment.bat
   ```

2. **Clean installation** (recommended if you're having issues):
   ```cmd
   clean-install.bat
   ```

Both scripts will:
- Create a virtual environment
- Install all required dependencies
- Prepare your system for running the application

## Manual Setup

If you prefer to set up manually, follow these steps:

### 1. Create and Activate Virtual Environment

```cmd
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```cmd
pip install -r requirements.txt
pip install -r requirements-api.txt
```

If you encounter dependency conflicts, try these approaches:

1. Use the `--use-deprecated=legacy-resolver` flag:
   ```cmd
   pip install -r requirements.txt --use-deprecated=legacy-resolver
   pip install -r requirements-api.txt --use-deprecated=legacy-resolver
   ```

2. Use the fix script for TensorFlow issues:
   ```cmd
   fix-installation.bat
   ```

3. Install packages individually if needed:
   ```cmd
   pip install numpy==1.23.5
   pip install tensorflow-cpu==2.12.0
   pip install opencv-python==4.5.5.64
   pip install fastapi==0.68.0 uvicorn[standard]==0.15.0
   ```

4. If you encounter OpenCV errors, use the dedicated fix script:
   ```cmd
   fix-opencv-version.bat
   ```

### 3. Verify Installation

```cmd
python verify-installation.py
```

## Running the Application

### Method 1: Using the Batch Script (Windows)

Double-click `start-dev.bat` to automatically:
1. Activate the virtual environment
2. Install backend dependencies
3. Start the backend API server
4. Start the frontend development server

### Method 2: Manual Start

1. **Start the Backend API**:
   ```cmd
   venv\Scripts\activate
   python api.py
   ```

2. **Start the Frontend** (in a new terminal):
   ```cmd
   cd cricket-ai-squad-main
   npm install  # Only needed the first time
   npm run dev
   ```

## Accessing the Application

Once both servers are running:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

Navigate to the Batting Analysis page to test the video classification functionality.

## File Structure

```
d:\cricket\
├── api.py                 # Backend API server
├── requirements.txt       # Main project dependencies
├── requirements-api.txt   # API-specific dependencies
├── model_weights.h5      # TensorFlow model weights (required)
├── setup-environment.bat # Automated setup script
├── start-dev.bat         # Development startup script
├── verify-installation.py # Dependency verification script
├── TROUBLESHOOTING.md    # Solutions to common issues
├── SETUP-GUIDE.md        # This file
└── cricket-ai-squad-main\ # Frontend application
    ├── package.json
    ├── src\
    │   └── pages\
    │       └── BattingAnalysis.tsx  # Modified for API integration
    └── ...
```

## Testing the Integration

1. Open your browser and go to http://localhost:5173/batting-analysis
2. Click "Choose File" or drag and drop a cricket video
3. Click "Start AI Analysis"
4. Wait for the analysis to complete
5. View the classification results

## Troubleshooting

If you encounter any issues:

1. **Check the verification script output**:
   ```cmd
   python verify-installation.py
   ```

2. **Refer to the detailed troubleshooting guide**:
   ```cmd
   notepad TROUBLESHOOTING.md
   ```

3. **Common issues and solutions**:
   - Python version incompatibility → Use Python 3.9
   - Missing dependencies → Run setup script
   - Model weights missing → Obtain `model_weights.h5` file
   - Port conflicts → Change ports in configuration

## Updating Dependencies

To update dependencies after changes:

```cmd
venv\Scripts\activate
pip install -r requirements.txt --upgrade
pip install -r requirements-api.txt --upgrade
```

## Stopping the Application

To stop the servers:

1. **Frontend**: Press `Ctrl+C` in the terminal
2. **Backend**: Press `Ctrl+C` in the terminal

To deactivate the virtual environment:
```cmd
deactivate
```

## Next Steps

After successful setup:

1. Test with sample cricket videos
2. Explore the API documentation at http://localhost:8000/docs
3. Review the integration guide in `INTEGRATION-GUIDE.md`
4. Customize the analysis parameters in `api.py`

## Support

If you continue to experience issues:

1. Check that all prerequisites are met
2. Ensure you're using the correct Python version
3. Verify all required files are present
4. Consult `TROUBLESHOOTING.md` for specific error solutions