@echo off
REM Complete Rich Content Setup Script for Windows
REM Automates the entire process of setting up rich content

echo ============================================================
echo CyberLearn Rich Content Setup
echo ============================================================
echo.

echo Step 1: Loading existing rich content lessons
echo ------------------------------------------------------------

if exist "content\lesson_active_directory_01_fundamentals_RICH.json" (
    echo Found rich lesson files
    echo    Renaming rich lessons...

    if exist "content\lesson_active_directory_01_fundamentals_RICH.json" (
        copy /Y "content\lesson_active_directory_01_fundamentals_RICH.json" "content\lesson_active_directory_01_active_directory_fundamentals.json" >nul
        echo    ✅ Active Directory Fundamentals
    )

    if exist "content\lesson_fundamentals_02_authentication_vs_authorization_RICH.json" (
        copy /Y "content\lesson_fundamentals_02_authentication_vs_authorization_RICH.json" "content\lesson_fundamentals_02_authentication_vs_authorization.json" >nul
        echo    ✅ Authentication vs Authorization
    )

    if exist "content\lesson_red_team_01_fundamentals_RICH.json" (
        copy /Y "content\lesson_red_team_01_fundamentals_RICH.json" "content\lesson_red_team_01_red_team_fundamentals.json" >nul
        echo    ✅ Red Team Fundamentals
    )
) else (
    echo No _RICH lesson files found (that's okay if already loaded)
)

echo.
echo Step 2: Generate additional lesson templates (optional)
echo ------------------------------------------------------------
set /p generate_templates="Generate 10 priority lesson templates now? (y/n): "
if /i "%generate_templates%"=="y" (
    python create_rich_lesson.py --batch generate_all_rich_lessons.json
    echo ✅ Generated 10 lesson templates
    echo.
    echo 📝 Next: Fill these templates with content using AI
    echo    Run: python enhance_with_ai.py --list
    echo.
) else (
    echo ⏭️  Skipped template generation
)

echo.
echo Step 3: Generate ALL basic and advanced lessons
echo ------------------------------------------------------------
set /p generate_all="Generate all 46 lessons (basic + advanced)? (y/n): "
if /i "%generate_all%"=="y" (
    echo    Generating basic lessons...
    python generate_lessons.py

    echo    Generating advanced lessons...
    python generate_advanced_lessons.py

    echo ✅ All lesson templates generated
) else (
    echo ⏭️  Skipped full generation
)

echo.
echo Step 4: Load all lessons into database
echo ------------------------------------------------------------
python load_all_lessons.py

echo.
echo Step 5: Check database status
echo ------------------------------------------------------------
python check_database.py

echo.
echo Step 6: Reset user (optional)
echo ------------------------------------------------------------
set /p username="Enter username to reset (or press Enter to skip): "
if not "%username%"=="" (
    python check_database.py reset %username%
    echo ✅ User %username% reset
) else (
    echo ⏭️  Skipped user reset
)

echo.
echo ============================================================
echo ✅ Setup Complete!
echo ============================================================
echo.
echo SUMMARY:
echo   • Rich lessons loaded (4 professional lessons)
echo   • All 46 lesson templates generated
echo   • Database updated
echo.
echo NEXT STEPS:
echo.
echo 1. ENHANCE CONTENT (Optional):
echo    python enhance_with_ai.py --list
echo    python enhance_with_ai.py content\lesson_FILE.json
echo.
echo 2. LAUNCH APP:
echo    streamlit run app.py
echo.
echo 3. TEST:
echo    • Complete diagnostic
echo    • Try a rich content lesson (AD, Auth/Authz, Red Team)
echo    • Compare with placeholder lessons
echo    • See the quality difference!
echo.
echo 4. GENERATE MORE RICH CONTENT:
echo    python create_rich_lesson.py --interactive
echo.
echo ============================================================
pause
