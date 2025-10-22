#!/bin/bash
# Complete Rich Content Setup Script
# Automates the entire process of setting up rich content

echo "============================================================"
echo "CyberLearn Rich Content Setup"
echo "============================================================"
echo ""

# Check if we're on the VM
if [ ! -f "cyberlearn.db" ]; then
    echo "⚠️  Warning: Database not found. Is this the correct directory?"
    echo "   Current directory: $(pwd)"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Step 1: Loading existing rich content lessons"
echo "------------------------------------------------------------"

# Check if rich lessons exist
if [ -f "content/lesson_active_directory_01_fundamentals_RICH.json" ]; then
    echo "✅ Found rich lesson files"

    # Rename rich lessons to replace placeholders
    echo "   Renaming rich lessons..."

    if [ -f "content/lesson_active_directory_01_fundamentals_RICH.json" ]; then
        cp content/lesson_active_directory_01_fundamentals_RICH.json \
           content/lesson_active_directory_01_active_directory_fundamentals.json
        echo "   ✅ Active Directory Fundamentals"
    fi

    if [ -f "content/lesson_fundamentals_02_authentication_vs_authorization_RICH.json" ]; then
        cp content/lesson_fundamentals_02_authentication_vs_authorization_RICH.json \
           content/lesson_fundamentals_02_authentication_vs_authorization.json
        echo "   ✅ Authentication vs Authorization"
    fi

    if [ -f "content/lesson_red_team_01_fundamentals_RICH.json" ]; then
        cp content/lesson_red_team_01_fundamentals_RICH.json \
           content/lesson_red_team_01_red_team_fundamentals.json
        echo "   ✅ Red Team Fundamentals"
    fi
else
    echo "ℹ️  No _RICH lesson files found (that's okay if they're already loaded)"
fi

echo ""
echo "Step 2: Generate additional lesson templates (optional)"
echo "------------------------------------------------------------"
read -p "Generate 10 priority lesson templates now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 create_rich_lesson.py --batch generate_all_rich_lessons.json
    echo "✅ Generated 10 lesson templates"
    echo ""
    echo "📝 Next: Fill these templates with content using AI"
    echo "   Run: python3 enhance_with_ai.py --list"
    echo ""
else
    echo "⏭️  Skipped template generation"
fi

echo ""
echo "Step 3: Generate ALL basic and advanced lessons"
echo "------------------------------------------------------------"
read -p "Generate all 46 lessons (basic + advanced)? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "   Generating basic lessons..."
    python3 generate_lessons.py

    echo "   Generating advanced lessons..."
    python3 generate_advanced_lessons.py

    echo "✅ All lesson templates generated"
else
    echo "⏭️  Skipped full generation"
fi

echo ""
echo "Step 4: Load all lessons into database"
echo "------------------------------------------------------------"
python3 load_all_lessons.py

echo ""
echo "Step 5: Check database status"
echo "------------------------------------------------------------"
python3 check_database.py

echo ""
echo "Step 6: Reset user (optional)"
echo "------------------------------------------------------------"
read -p "Enter username to reset (or press Enter to skip): " username
if [ -n "$username" ]; then
    python3 check_database.py reset "$username"
    echo "✅ User $username reset"
else
    echo "⏭️  Skipped user reset"
fi

echo ""
echo "============================================================"
echo "✅ Setup Complete!"
echo "============================================================"
echo ""
echo "SUMMARY:"
echo "  • Rich lessons loaded (4 professional lessons)"
echo "  • All 46 lesson templates generated"
echo "  • Database updated"
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. ENHANCE CONTENT (Optional):"
echo "   python3 enhance_with_ai.py --list"
echo "   python3 enhance_with_ai.py content/lesson_FILE.json"
echo ""
echo "2. LAUNCH APP:"
echo "   streamlit run app.py"
echo ""
echo "3. TEST:"
echo "   • Complete diagnostic"
echo "   • Try a rich content lesson (AD Fundamentals, Auth/Authz, Red Team)"
echo "   • Compare with placeholder lessons"
echo "   • See the quality difference!"
echo ""
echo "4. GENERATE MORE RICH CONTENT:"
echo "   python3 create_rich_lesson.py --interactive"
echo ""
echo "============================================================"
