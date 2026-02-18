@echo off
REM Quick Start Script for Batch Lesson Generation
REM Windows Batch File

echo ================================================================================
echo CyberLearn Batch Lesson Generator - Quick Start
echo ================================================================================
echo.

REM Check if API key is set
if "%ANTHROPIC_API_KEY%"=="" (
    echo ERROR: ANTHROPIC_API_KEY environment variable not set!
    echo.
    echo Please set your Anthropic API key:
    echo   set ANTHROPIC_API_KEY=your-api-key-here
    echo.
    echo Get your API key from: https://console.anthropic.com/
    echo.
    pause
    exit /b 1
)

echo API Key: Set
echo.

REM Check if anthropic module is installed
python -c "import anthropic" 2>nul
if errorlevel 1 (
    echo Installing Anthropic SDK...
    pip install anthropic
    echo.
)

echo Starting batch generation...
echo.
python batch_generate_lessons.py

echo.
echo ================================================================================
echo Batch generation complete!
echo.
echo Next steps:
echo   1. Review generated lessons in content/ directory
echo   2. Validate: python scripts/validate_lesson_compliance.py
echo   3. Load to DB: python scripts/sync_lessons.py
echo   4. Test: streamlit run app.py
echo ================================================================================
pause
