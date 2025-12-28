@echo off
echo Fixing TensorFlow and OpenCV installation for Python 3.9...

echo Activating virtual environment...
call venv\Scripts\activate

echo Uninstalling existing OpenCV packages...
pip uninstall opencv-python opencv-python-headless -y

echo Installing TensorFlow CPU version (avoids Intel-specific packages)...
pip install tensorflow-cpu==2.12.0 --use-deprecated=legacy-resolver

echo Installing compatible OpenCV version...
pip install opencv-python==4.5.5.64

echo Installing numpy...
pip install numpy==1.23.5

echo Installing FastAPI and uvicorn...
pip install fastapi==0.68.0 uvicorn[standard]==0.15.0

echo Verifying installation...
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"
python -c "import cv2; print('OpenCV version:', cv2.__version__)"

echo Done! Try running the API again with: python api.py
pause