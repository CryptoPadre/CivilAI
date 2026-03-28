#!/bin/bash

# go to script directory (optional if already running from backend)
cd "$(dirname "$0")"

# correct DATABASE_URL with quotes
export DATABASE_URL="postgresql://neondb_owner:npg_DCmdoQ8PO0pL@ep-crimson-resonance-amjq27sj-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Django settings module
export DJANGO_SETTINGS_MODULE=civilAI.settings

# activate virtual environment
source venv/bin/activate

# run the command and log output
python manage.py update_age >> /tmp/update_age.log 2>&1