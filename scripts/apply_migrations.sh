#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
cd $ROOT_DIR

# Check for pending migrations and apply them if necessary
echo "Checking for pending migrations..."
if python3 ./manage.py makemigrations --check --dry-run | grep -q "No changes detected"; then
    echo "No pending migrations detected."
else
    echo "Pending migrations detected. Do you want to apply them? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "Applying migrations..."
        python3 ./manage.py makemigrations
        python3 ./manage.py migrate
        if [ $? -eq 0 ]; then
            echo "Migrations applied successfully."
        else
            echo "Error: Failed to apply migrations."
            exit 1
        fi
    else
        echo "Migration aborted by the user."
        exit 0
    fi
fi