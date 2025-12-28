# Troubleshooting Guide for Cricket AI Squad

## Python Version Compatibility Issues

### Problem
You're encountering errors related to TensorFlow installation:
```
ERROR: Ignored the following versions that require a different python version
ERROR: Could not find a version that satisfies the requirement wrapt>=1.11.0
```

### Root Cause
Your system is running Python 3.9.0, but newer versions of TensorFlow require Python 3.10 or higher.

### Solutions

#### Option 1: Downgrade TensorFlow (Recommended for Python 3.9)
We've already updated the requirements files to use TensorFlow 2.12.0 which is compatible with Python 3.9:

1. Update your `requirements.txt`:
   ```
   tensorflow == 2.12.0
   ```

2. Use compatible numpy versions:
   ```
   numpy >= 1.22, < 1.24
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Option 2: Upgrade Python (Long-term Solution)
1. Download and install Python 3.10 or higher from [python.org](https://www.python.org/downloads/)
2. Create a new virtual environment with the newer Python version:
   ```bash
   python -m venv venv-new
   source venv-new/bin/activate  # On Windows: venv-new\Scripts\activate
   ```
3. Install the latest TensorFlow:
   ```bash
   pip install tensorflow==2.13.0
   ```

## Virtual Environment Issues

### Problem
Dependencies conflict with system packages

### Solution
Use the provided setup scripts which automatically create and configure a virtual environment:

1. For a fresh installation, run the clean install script:
   ```
   clean-install.bat
   ```

2. For a regular setup, run the setup script:
   ```
   setup-environment.bat
   ```

Or manually create a virtual environment:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate it:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt --use-deprecated=legacy-resolver
   ```

## Model Weights File Missing

### Problem
The API fails to start because `model_weights.h5` is missing

### Solution
Ensure the `model_weights.h5` file is in the project root directory (`d:\cricket\`).

If you don't have this file, you'll need to either:
1. Obtain it from the project source
2. Train your own model and save the weights

## Port Conflicts

### Problem
The API or frontend fails to start due to port conflicts

### Solution
Change the ports in the respective configuration files:

1. For the API (`api.py`):
   ```python
   if __name__ == "__main__":
       uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed from 8000
   ```

2. For the frontend (`vite.config.ts` in the frontend directory):
   ```javascript
   export default defineConfig({
     server: {
       port: 5174  // Changed from 5173
     }
   })
   ```

## CORS Issues

### Problem
Frontend cannot communicate with the backend API

### Solution
Ensure the backend API has CORS enabled (already implemented):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing the API

### Verify the API is Running
1. Start the API:
   ```bash
   python api.py
   ```

2. Test with the provided script:
   ```bash
   python test_api.py
   ```

3. Or manually check:
   ```bash
   curl http://localhost:8000/
   ```

Expected response:
```json
{"message": "Cricket Shot Classification API"}
```

## Common Windows Issues

### PowerShell Execution Policy
If you encounter script execution issues:

1. Open PowerShell as Administrator
2. Run:
   ```powershell
   Set-ExecutionPolicy RemoteSigned
   ```

### Path Issues
Use forward slashes or escaped backslashes in paths:
- Correct: `d:/cricket/model_weights.h5`
- Correct: `d:\\cricket\\model_weights.h5`
- Incorrect: `d:\cricket\model_weights.h5`

## Performance Optimization

### Slow Video Processing
For faster processing during development:

1. Reduce the number of frames processed in `api.py`:
   ```python
   # Change from 30 frames to 15 frames
   class_name, confidence = classify_video(tmp_path, model, 15, classes)
   ```

2. Use smaller video files for testing (under 10MB)

## Debugging Tips

### Enable Detailed Logging
Add logging to the API to debug issues:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Check Dependencies
Verify installed packages:
```bash
pip list | grep tensorflow
pip list | grep opencv
```

### Run Verification Script
Use the provided verification script to check if all dependencies are correctly installed:
```bash
python verify-installation.py
```

This script will check:
- Python version compatibility
- Required package installations
- Model weights file presence

### TensorFlow Installation Issues

If you encounter issues with TensorFlow installation:

1. Use the `fix-installation.bat` script which installs compatible versions:
   ```
   fix-installation.bat
   ```

2. Or manually install the CPU version which avoids Intel-specific package conflicts:
   ```bash
   pip install tensorflow-cpu==2.12.0
   ```

3. If you still encounter issues, try installing packages individually:
   ```bash
   pip install numpy==1.23.5
   pip install tensorflow-cpu==2.12.0
   pip install opencv-python==4.5.5.64
   ```

### OpenCV Compatibility Issues

If you encounter OpenCV errors like `module 'cv2.dnn' has no attribute 'DictValue'`:

1. Use the `fix-opencv-version.bat` script:
   ```
   fix-opencv-version.bat
   ```

2. Or manually fix the OpenCV version:
   ```bash
   pip uninstall opencv-python opencv-python-headless -y
   pip install opencv-python==4.5.5.64
   ```

### Video File Upload Issues

If you're having trouble uploading AVI or other video files:

1. Check that the file extension is correct (.mp4, .avi, or .mov)
2. Try using the test script to verify file upload:
   ```bash
   python test-video-upload.py your_video_file.avi
   ```
3. Check the API logs for detailed error information
4. Ensure the video file is not corrupted
5. Try with a smaller video file (under 50MB) for testing

## Additional Resources

1. TensorFlow installation guide: https://www.tensorflow.org/install
2. FastAPI documentation: https://fastapi.tiangolo.com/
3. OpenCV documentation: https://docs.opencv.org/