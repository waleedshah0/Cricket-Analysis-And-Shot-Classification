@echo off
echo Setting up Cricket AI Squad Environment...

rem Check if virtual environment exists, if not create it
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing main dependencies...
pip install -r requirements.txt --use-deprecated=legacy-resolver

echo Installing API dependencies...
pip install -r requirements-api.txt --use-deprecated=legacy-resolver

echo Setup complete!
echo To activate the environment manually, run: venv\Scripts\activate
pause