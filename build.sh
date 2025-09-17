#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Load initial data
python manage.py loaddata portfolio/fixtures/initial_data.json
