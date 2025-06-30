#!/bin/bash

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Start Docker containers in detached mode (non-blocking)
echo "Starting Docker containers with docker compose in detached mode..."
docker compose up -d

source venv/bin/activate
echo "Activated virtual environment."

echo "Installing dependencies"
pip install -r requirements.txt

echo "Running program"
python -m app.main