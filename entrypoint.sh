#!/bin/bash
set -e

echo ">>> Running DB migrations..."
flask db upgrade

echo ">>> Starting gunicorn..."
exec gunicorn --workers 3 --bind 0.0.0.0:5000 run:app
