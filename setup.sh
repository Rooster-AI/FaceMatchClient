#!/bin/bash

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python is not installed. Please install Python 3.x and try again."
    exit 1
fi

# Create a virtual environment
python3 -m venv rooster-venv

# Activate the virtual environment
source rooster-venv/bin/activate

# Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Please create the file with your project dependencies."
    deactivate
    exit 1
fi

echo "Virtual environment created and activated. Dependencies installed."
