#!/bin/bash

# Define the virtual environment directory
VENV_DIR="venv"

# Create a Python virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Install required packages from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing packages from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Please ensure it exists in the current directory."
    deactivate
    exit 1
fi

# Check for mysqlclient installation errors
if ! pip install mysqlclient; then
    echo "Failed to install mysqlclient. Checking system package manager..."

    # Determine the package manager (Debian or Fedora based)
    if command -v apt-get > /dev/null; then
        echo "Detected apt package manager. Installing necessary system dependencies..."
        sudo apt-get update
        sudo apt-get install -y pkg-config python3-dev default-libmysqlclient-dev build-essential
    elif command -v dnf > /dev/null; then
        echo "Detected dnf package manager. Installing necessary system dependencies..."
        sudo dnf install -y pkgconf-pkg-config python3-devel Kernel-devel gcc gcc-c++
    else
        echo "Error: Unsupported package manager. Please install the necessary dependencies manually."
        deactivate
        exit 1
    fi

    echo "Retrying installation of mysqlclient..."
    if ! pip install mysqlclient; then
        echo "Error: mysqlclient installation failed again. Please check your system configuration."
        deactivate
        exit 1
    fi
else
    echo "mysqlclient installed successfully."
fi

echo "Creating debug secrets..."

# Function to generate a random SECRET_KEY
generate_secret_key() {
    python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
}

# Check if .env file exists; if not, create it
if [ ! -f .env ]; then
    echo ".env file not found, creating it..."
    touch .env
fi

# Write the SECRET_KEY to .env file
{
    echo "SECRET_KEY=$(generate_secret_key)"
    echo "EMAIL_BACKEND=''"
    echo "EMAIL_HOST=''"
    echo "EMAIL_HOST_USER=''"
    echo "EMAIL_HOST_PASSWORD=''"
    echo "EMAIL_PORT=''"
    echo "EMAIL_USE_SSL=''"
    echo "DEFAULT_FROM_EMAIL=''"
    echo "HCAPTCHA_SITEKEY=''"
    echo "HCAPTCHA_SECRET=''"
    echo "VERIFY_URL=''"
} > .env

# Confirm the action
echo "Generated and stored debug secrets in .env"

echo "Setup completed successfully."
