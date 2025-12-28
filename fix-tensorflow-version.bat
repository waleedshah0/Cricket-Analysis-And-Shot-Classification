@echo off
echo Fixing TensorFlow version for Python 3.9 compatibility...

echo Activating virtual environment...
call venv\Scripts\activate

echo Uninstalling current TensorFlow...
pip uninstall tensorflow -y

echo Installing compatible TensorFlow version...
pip install tensorflow==2.12.0 --use-deprecated=legacy-resolver

echo Verifying installation...
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"

echo Done! Try running the API again with: python api.py
pause