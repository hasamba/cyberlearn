#!/bin/bash
# CyberLearn Start Script
# Quick start script for running the application after initial setup

set -e  # Exit on error

echo "========================================="
echo "  Starting CyberLearn"
echo "========================================="
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
echo ""
echo "Opening in browser: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo "========================================="
echo ""

streamlit run app.py
