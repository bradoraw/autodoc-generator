#!/bin/bash

# Create a virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    shot-scraper install # install browser
else
    source venv/bin/activate
fi

python3 autodoc.py 