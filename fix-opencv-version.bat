@echo off
echo Fixing OpenCV version for compatibility...

echo Activating virtual environment...
call venv\Scripts\activate

echo Uninstalling current OpenCV...
pip uninstall opencv-python opencv-python-headless -y

echo Installing compatible OpenCV version...
pip install opencv-python==4.5.5.64

echo Verifying installation...
python -c "import cv2; print('OpenCV version:', cv2.__version__)"

echo Done! Try running the API again with: python api.py
pause