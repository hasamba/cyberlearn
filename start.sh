#!/bin/bash
# CyberLearn Start Script
# Quick start script for running the application after initial setup
#
# Usage:
#   ./start.sh        # Normal mode
#   ./start.sh -v     # Verbose/Debug mode
#   ./start.sh --debug # Debug mode

set -e  # Exit on error

# Check for debug flag
DEBUG_FLAG=""
if [ "$1" = "-v" ] || [ "$1" = "--verbose" ] || [ "$1" = "--debug" ]; then
    DEBUG_FLAG="-- $1"
    echo "========================================="
    echo "  Starting CyberLearn (DEBUG MODE)"
    echo "========================================="
else
    echo "========================================="
    echo "  Starting CyberLearn"
    echo "========================================="
fi
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run setup.sh first to install the application."
    echo ""
    echo "  ./setup.sh"
    echo ""
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Start Streamlit
echo "Starting application..."
if [ -n "$DEBUG_FLAG" ]; then
    echo "Debug mode enabled - check terminal for debug output"
fi
echo ""
echo "Opening in browser: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo "========================================="
echo ""

streamlit run app.py $DEBUG_FLAG
