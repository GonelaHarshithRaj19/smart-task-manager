#!/bin/bash
# Smart Task Manager - Run Script for Linux/macOS
# This script sets up the environment and runs the Flask application

echo "========================================"
echo "Smart Task Manager - Flask Application"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/Update requirements
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install requirements"
    exit 1
fi

# Run the Flask app
echo ""
echo "Starting Smart Task Manager..."
echo ""
echo "Application will be available at http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""
python app.py
