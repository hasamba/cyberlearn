@echo off
REM CyberLearn Start Script for Windows
REM Quick start script for running the application after initial setup

echo =========================================
echo   Starting CyberLearn
echo =========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Error: Virtual environment not found!
    echo Please run setup.bat first to install the application.
    echo.
    echo   setup.bat
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Start Streamlit
echo Starting application...
echo.
echo Opening in browser: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo =========================================
echo.

streamlit run app.py
