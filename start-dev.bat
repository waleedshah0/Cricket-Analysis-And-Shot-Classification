@echo off
echo Starting Cricket AI Squad Development Environment...

rem Check if virtual environment exists, if not create it
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing backend dependencies...
pip install -r requirements-api.txt --use-deprecated=legacy-resolver

echo Starting backend API server...
start "Backend API" /D "d:\cricket" cmd /c "venv\Scripts\activate && python api.py"

echo Starting stadiums API server...
start "Stadiums API" /D "d:\cricket" cmd /c "venv\Scripts\activate && python stadiums_api.py"

echo Starting frontend development server...
cd cricket-ai-squad-main
npm run dev

echo Servers started:
echo Frontend: http://localhost:5173
echo Backend API: http://localhost:8000
echo.
echo If you encounter any issues, please refer to TROUBLESHOOTING.md
pause