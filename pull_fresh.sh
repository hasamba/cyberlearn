#!/bin/bash
# Pull latest changes from remote, discarding all local changes
# Use this on VM to always get the latest from dev machine

echo "============================================================"
echo "PULLING FRESH FROM REMOTE (DISCARDING LOCAL CHANGES)"
echo "============================================================"

echo ""
echo "1. Fetching latest changes from remote..."
git fetch origin

echo ""
echo "2. Resetting local branch to match remote (discarding local changes)..."
git reset --hard origin/main

echo ""
echo "3. Cleaning untracked files..."
git clean -fd

echo ""
echo "============================================================"
echo "✅ REPOSITORY UPDATED TO MATCH REMOTE"
echo "============================================================"

echo ""
echo "Current commit:"
git log -1 --oneline

echo ""
echo "Next steps:"
echo "  1. Delete old database: rm cyberlearn.db"
echo "  2. Create fresh database: python setup_database.py"
echo "  3. Run app: streamlit run app.py"
