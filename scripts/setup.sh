#!/bin/bash

# Tiling System Setup Script

set -e

echo "Setting up Tiling System..."
echo ""

# Backend setup
echo "Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found"
fi

# Copy environment file if it doesn't exist
if [ -f ".env.example" ] && [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please update .env with your configuration"
fi

cd ..

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update backend/.env with your configuration"
echo "2. Run 'docker-compose up -d postgres' to start the database"
echo "3. Run './scripts/run-dev.sh' to start the development server"
echo "   OR run 'docker-compose up' to start all services with Docker"
echo ""
