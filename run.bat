@echo off
SETLOCAL

REM Check if venv directory exists
IF NOT EXIST "venv" (
    python -m venv venv
    echo Virtual environment created.
) ELSE (
    echo Virtual environment already exists.
)

REM Start Docker containers in detached mode (non-blocking)
echo Starting Docker containers with docker compose in detached mode...
docker compose up -d

REM Activate virtual environment
CALL venv\Scripts\activate.bat
echo Activated virtual environment.

echo Installing dependencies
pip install -r requirements.txt

echo Running program
python -m app.main

ENDLOCAL