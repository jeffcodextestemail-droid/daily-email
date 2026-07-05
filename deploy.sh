#!/usr/bin/env bash
set -e

cd /home/ubuntu/daily-email

echo "Pulling latest code..."
git pull origin master

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
python -m pip install -r requirements.txt

echo "Checking Python syntax..."
python -m py_compile daily_email.py

echo "Checking import..."
python -c "import daily_email; print('Import successful')"

echo "Deployment complete."
