#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# For Vercel, we'll load data in the view since database is in-memory
