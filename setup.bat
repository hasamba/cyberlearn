@echo off
REM CyberLearn Setup Script for Windows
REM Run this script after cloning the repository to set up the application

echo =========================================
echo   CyberLearn Installation Setup
echo =========================================
echo.

REM Check Python version
echo [1/5] Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3.8+ required
    pause
    exit /b 1
)
echo OK Python found
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo OK Virtual environment created
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo OK Virtual environment activated
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo OK Dependencies installed
echo.

REM Load lessons into database
echo [5/5] Loading lessons into database...
python load_all_lessons.py
echo OK Lessons loaded successfully
echo.

echo =========================================
echo   Installation Complete!
echo =========================================
echo.
echo To start the application, run:
echo.
echo   venv\Scripts\activate.bat  REM Activate virtual environment
echo   streamlit run app.py       REM Start the application
echo.
echo The application will open in your browser at:
echo   http://localhost:8501
echo.
echo =========================================
pause
