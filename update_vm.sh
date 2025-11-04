#!/bin/bash
# Complete VM update script - pulls latest code and resets database

echo "============================================================"
echo "CYBERLEARN VM UPDATE SCRIPT"
echo "============================================================"

echo ""
echo "Step 1: Pulling latest changes (discarding local changes)..."
git fetch origin
git reset --hard origin/main
git clean -fd

echo ""
echo "✓ Code updated to match remote"
echo ""
echo "Current commit:"
git log -1 --oneline

echo ""
echo "============================================================"

# Check if database exists
if [ -f "cyberlearn.db" ]; then
    echo "Step 2: Found existing database"

    # Loop until valid input (y or n)
    while true; do
        read -p "Delete and recreate database? This will remove all user data (y/n): " -n 1 -r
        echo ""

        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Deleting old database..."
            rm cyberlearn.db
            echo "✓ Old database deleted"

            echo ""
            echo "Creating fresh database from template..."
            python setup_database.py

            echo ""
            echo "============================================================"
            echo "✅ VM FULLY UPDATED - Ready to use!"
            echo "============================================================"
            echo ""
            echo "Run the app: streamlit run app.py"
            break
        elif [[ $REPLY =~ ^[Nn]$ ]]; then
            echo "Keeping existing database"
            echo ""

            # Ask about updating outdated lessons
            while true; do
                read -p "Check for lesson content updates? This preserves user data (y/n): " -n 1 -r
                echo ""

                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    echo ""
                    echo "Checking for outdated lessons..."
                    python scripts/update_outdated_lessons.py

                    echo ""
                    echo "============================================================"
                    echo "✅ VM UPDATED - Lessons synced, user data preserved!"
                    echo "============================================================"
                    echo ""
                    echo "Run the app: streamlit run app.py"
                    break 2
                elif [[ $REPLY =~ ^[Nn]$ ]]; then
                    echo "Skipping lesson updates"
                    echo ""
                    echo "To update lessons later, run:"
                    echo "  python scripts/update_outdated_lessons.py"
                    echo ""
                    echo "To recreate database from scratch, run:"
                    echo "  rm cyberlearn.db"
                    echo "  python setup_database.py"
                    break 2
                else
                    echo "Invalid input. Please enter 'y' or 'n'."
                fi
            done
        else
            echo "Invalid input. Please enter 'y' or 'n'."
        fi
    done
else
    echo "Step 2: No database found, creating from template..."
    python setup_database.py

    echo ""
    echo "============================================================"
    echo "✅ VM FULLY UPDATED - Ready to use!"
    echo "============================================================"
    echo ""
    echo "Run the app: streamlit run app.py"
fi
