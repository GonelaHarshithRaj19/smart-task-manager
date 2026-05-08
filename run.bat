@echo off
REM Smart Task Manager - Run Script for Windows
REM This script sets up the environment and runs the Flask application

echo ========================================
echo Smart Task Manager - Flask Application
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/Update requirements
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)

REM Run the Flask app
echo.
echo Starting Smart Task Manager...
echo.
echo Application will be available at http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
