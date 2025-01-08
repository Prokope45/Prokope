#!/bin/bash

# Function to generate a random SECRET_KEY
generate_secret_key() {
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
}

# Check if .env file exists; if not, create it
if [ ! -f .env ]; then
    echo ".env file not found, creating it..."
    touch .env
fi

# Generate a new SECRET_KEY and add it to .env
SECRET_KEY=$(generate_secret_key)

# Write the SECRET_KEY to .env file
echo "SECRET_KEY='$SECRET_KEY'" > .env

# Confirm the action
echo "Generated and stored new SECRET_KEY in .env"

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PROJECT_DIR="$SCRIPT_DIR/mysite"
SETTINGS_FILE="$PROJECT_DIR/settings.py"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Project directory '$PROJECT_DIR' does not exist."
    exit 1
fi

# Check if the virtual environment is active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Virtual environment is not active. Please activate it and try again."
    exit 1
else
    echo "Virtual environment is active."
fi

if grep -q "DEBUG = False" "$SETTINGS_FILE"; then
    echo "Django DEBUG mode is disabled. Changing DEBUG to True..."
    
    # Replace DEBUG = False with DEBUG = True
    sed -i 's/DEBUG = False/DEBUG = True/' "$SETTINGS_FILE"

    if [ $? -eq 0 ]; then
        echo "Successfully updated DEBUG to True in $SETTINGS_FILE."
    else
        echo "Error: Failed to update DEBUG setting. Please check file permissions."
        exit 1
    fi
elif grep -q "DEBUG = True" "$SETTINGS_FILE"; then
    echo "Django DEBUG mode is already enabled."
else
    echo "Error: DEBUG setting not found in $SETTINGS_FILE. Please ensure it exists."
    exit 1
fi

# Navigate to the project directory and run the server
cd "$SCRIPT_DIR" || { echo "Error: Failed to navigate to project directory."; exit 1; }

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

# Run the Django development server
echo "Starting the Django development server..."
python3 ./manage.py runserver
