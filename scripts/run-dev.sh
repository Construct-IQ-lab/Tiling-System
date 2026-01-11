#!/bin/bash

# Tiling System Development Server

set -e

echo "Starting Tiling System development server..."
echo ""

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run ./scripts/setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Using default configuration."
fi

# Run uvicorn development server
echo "Starting uvicorn server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
