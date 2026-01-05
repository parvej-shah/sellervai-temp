#!/bin/sh

# Activate virtual environment
source /app/.venv/bin/activate

# Run the application
alembic upgrade head

python app/main.py