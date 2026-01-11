#!/bin/bash

# Script to create company portal directories
# Usage: ./create-company-portal.sh <company-slug>

if [ -z "$1" ]; then
    echo "Usage: ./create-company-portal.sh <company-slug>"
    echo "Example: ./create-company-portal.sh elitetilingsolutions"
    exit 1
fi

COMPANY_SLUG=$1
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
COMPANY_DIR="$REPO_ROOT/$COMPANY_SLUG"

echo "Creating company portal for: $COMPANY_SLUG"

# Create company directory if it doesn't exist
if [ -d "$COMPANY_DIR" ]; then
    echo "Warning: Directory $COMPANY_DIR already exists"
    read -p "Do you want to overwrite? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

mkdir -p "$COMPANY_DIR"

# Copy company portal templates
echo "Copying company portal templates..."
cp "$REPO_ROOT/frontend/company/index.html" "$COMPANY_DIR/"
cp "$REPO_ROOT/frontend/company/projects.html" "$COMPANY_DIR/"
cp "$REPO_ROOT/frontend/company/calculator.html" "$COMPANY_DIR/"
cp "$REPO_ROOT/frontend/company/quotes.html" "$COMPANY_DIR/"
cp "$REPO_ROOT/frontend/company/profile.html" "$COMPANY_DIR/"

echo "✓ Company portal created successfully!"
echo ""
echo "Access the company portal at:"
echo "  http://localhost:8080/$COMPANY_SLUG/index.html"
echo ""
echo "Make sure to:"
echo "  1. Create the company in the admin portal"
echo "  2. Use the exact slug: $COMPANY_SLUG"
echo "  3. Create users for this company"
