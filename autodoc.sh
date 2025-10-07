#!/bin/bash

# 0. Create a virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    shot-scraper install # install browser
else
    source venv/bin/activate
fi

# Create screenshots and chapters directories if they don't exist
mkdir -p screenshots
mkdir -p chapters

python3 capture_screenshots.py
python3 analyze_and_document.py 