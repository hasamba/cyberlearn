#!/bin/bash
# CyberLearn Setup Script
# Run this script after cloning the repository to set up the application

set -e  # Exit on error

echo "========================================="
echo "  CyberLearn Installation Setup"
echo "========================================="
echo ""

# Check Python version
echo "[1/5] Checking Python version..."
python3 --version || { echo "Error: Python 3.8+ required"; exit 1; }
echo "✓ Python found"
echo ""

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "[4/5] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Load lessons into database
echo "[5/5] Loading lessons into database..."
python load_all_lessons.py
echo "✓ Lessons loaded successfully"
echo ""

echo "========================================="
echo "  Installation Complete!"
echo "========================================="
echo ""
echo "To start the application, run:"
echo ""
echo "  source venv/bin/activate  # Activate virtual environment"
echo "  streamlit run app.py      # Start the application"
echo ""
echo "The application will open in your browser at:"
echo "  http://localhost:8501"
echo ""
echo "========================================="
