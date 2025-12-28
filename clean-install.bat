@echo off
echo Cleaning and reinstalling Cricket AI Squad dependencies...

echo Deactivating virtual environment if active...
deactivate 2>nul

echo Removing existing virtual environment...
rd /s /q venv 2>nul

echo Creating fresh virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing main dependencies with legacy resolver...
pip install -r requirements.txt --use-deprecated=legacy-resolver

echo If TensorFlow installation fails, use the fix script:
rem pip install tensorflow-cpu==2.12.0 numpy==1.23.5 opencv-python==4.5.5.64

echo Installing API dependencies with legacy resolver...
pip install -r requirements-api.txt --use-deprecated=legacy-resolver

echo Verifying installation...
python verify-installation.py

echo.
echo Clean installation complete!
echo If all checks passed, you're ready to run the application.
echo Run 'start-dev.bat' to start both servers.
pause