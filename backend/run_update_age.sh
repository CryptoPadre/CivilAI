#!/bin/bash

# Activate virtual environment
source /Users/tamasgavlider/Desktop/CivilAI/CivilAI/backend/venv/bin/activate

# Navigate to Django project
cd /Users/tamasgavlider/Desktop/CivilAI/CivilAI/backend

# Set Django settings module explicitly
export DJANGO_SETTINGS_MODULE="backend.settings"

# Run management command and log output
python manage.py update_age >> /tmp/update_age.log 2>&1