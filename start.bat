@echo off
REM CyberLearn Start Script for Windows
REM Quick start script for running the application after initial setup
REM
REM Usage:
REM   start.bat        - Normal mode
REM   start.bat -v     - Verbose/Debug mode
REM   start.bat --debug - Debug mode

REM Check for debug flag
set DEBUG_FLAG=
if "%1"=="-v" set DEBUG_FLAG=-- -v
if "%1"=="--verbose" set DEBUG_FLAG=-- --verbose
if "%1"=="--debug" set DEBUG_FLAG=-- --debug

if defined DEBUG_FLAG (
    echo =========================================
    echo   Starting CyberLearn (DEBUG MODE^)
    echo =========================================
) else (
    echo =========================================
    echo   Starting CyberLearn
    echo =========================================
)
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
if defined DEBUG_FLAG (
    echo Debug mode enabled - check terminal for debug output
)
echo.
echo Opening in browser: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo =========================================
echo.

streamlit run app.py %DEBUG_FLAG%
