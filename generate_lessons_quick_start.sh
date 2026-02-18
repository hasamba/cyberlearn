#!/bin/bash
# Quick Start Script for Batch Lesson Generation
# Linux/Mac Shell Script

echo "================================================================================"
echo "CyberLearn Batch Lesson Generator - Quick Start"
echo "================================================================================"
echo ""

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "ERROR: ANTHROPIC_API_KEY environment variable not set!"
    echo ""
    echo "Please set your Anthropic API key:"
    echo "  export ANTHROPIC_API_KEY='your-api-key-here'"
    echo ""
    echo "Get your API key from: https://console.anthropic.com/"
    echo ""
    exit 1
fi

echo "API Key: Set"
echo ""

# Check if anthropic module is installed
python3 -c "import anthropic" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing Anthropic SDK..."
    pip3 install anthropic
    echo ""
fi

echo "Starting batch generation..."
echo ""
python3 batch_generate_lessons.py

echo ""
echo "================================================================================"
echo "Batch generation complete!"
echo ""
echo "Next steps:"
echo "  1. Review generated lessons in content/ directory"
echo "  2. Validate: python3 scripts/validate_lesson_compliance.py"
echo "  3. Load to DB: python3 scripts/sync_lessons.py"
echo "  4. Test: streamlit run app.py"
echo "================================================================================"
