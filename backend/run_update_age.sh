#!/bin/bash

# Path to your virtual environment
VENV="/Users/tamasgavlider/Desktop/CivilAI/CivilAI/backend/venv"

# Activate the virtual environment
source "$VENV/bin/activate"

# Navigate to your Django project directory
cd /Users/tamasgavlider/Desktop/CivilAI/CivilAI/backend

# Run the management command
python manage.py update_age >> /tmp/update_age.log 2>&1