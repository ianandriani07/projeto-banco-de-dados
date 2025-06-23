@echo off
SETLOCAL

REM Check if venv directory exists
IF NOT EXIST "venv" (
    python -m venv venv
    echo Virtual environment created.
) ELSE (
    echo Virtual environment already exists.
)

REM Activate virtual environment
CALL venv\Scripts\activate.bat
echo Activated virtual environment.

echo Installing dependencies
pip install -r requirements.txt

echo Running program
python -m app.main

ENDLOCAL
