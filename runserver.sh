#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PROJECT_DIR="$SCRIPT_DIR/prokope"
SETTINGS_FILE="$PROJECT_DIR/settings.py"

function testMode() {
  echo "Setting DEBUG and PRODUCTION to false for testing..."
  
  sed -i '' 's/^DEBUG *= *.*/DEBUG = False/' "$SETTINGS_FILE"
  if [ $? -eq 0 ]; then
    echo "Successfully updated DEBUG to False in $SETTINGS_FILE."
  else
    echo "Error: Failed to update DEBUG setting. Please check file permissions."
    exit 1
  fi

  sed -i '' 's/^PRODUCTION *= *.*/PRODUCTION = False/' "$SETTINGS_FILE"
  if [ $? -eq 0 ]; then
    echo "Successfully updated PRODUCTION to False in $SETTINGS_FILE."
  else
    echo "Error: Failed to update PRODUCTION setting. Please check file permissions."
    exit 1
  fi
}

function debugMode() {
  if grep -q "DEBUG = False" "$SETTINGS_FILE"; then
    echo "Django DEBUG mode is disabled. Changing DEBUG to True..."
    
    # Replace DEBUG = False with DEBUG = True
    # NOTE: MacOS sed differs from GNU sed in that it requires an argument for backup extension.
    sed -i '' 's/DEBUG = False/DEBUG = True/' "$SETTINGS_FILE"

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
}

function usage() {
  cat <<USAGE

  Usage: $0 [-d debug] [-t test]

  Options:
    -d, --debug:          Run server in debug mode.
    -t, --test:           Run server in test mode (with DEBUG off).
USAGE
    exit 1
}

if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Project directory '$PROJECT_DIR' does not exist."
    exit 1
fi

# Check if the virtual environment is active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Virtual environment is not active. Please activate it and try again."
    exit 1
else
    echo -e "Virtual environment is active.\n"
fi

echo "🧪 Running tests..."
coverage run --source=apps.common,apps.index --omit=*/migrations/* manage.py test apps.common apps.index

# Check if tests failed
if [ $? -ne 0 ]; then
echo "❌ Tests failed. Please fix the errors before running the server again."
    exit 1
else
    echo "✅ All tests passed."
fi

# Enforce minimum of 80% coverage
MIN_COVERAGE=80
COVERAGE_RESULT=$(coverage report | grep 'TOTAL' | awk '{print $4}' | sed 's/%//')

if [ "$COVERAGE_RESULT" -lt "$MIN_COVERAGE" ]; then
    echo "❌ Code coverage is below ${MIN_COVERAGE}%. Current: ${COVERAGE_RESULT}%"
    coverage report -m
    exit 1
fi
echo "✅ Coverage at: ${COVERAGE_RESULT}%"
coverage html -d docs/coverage
echo -e "\n"

if [ $# -eq 0 ]; then
  debugMode
else
  while [ "$1" != "" ]; do
    case $1 in
    -d | --debug)
      debugMode
      break
      ;;
    -t | --test)
      testMode
      break
      ;;
    -h | --help)
      usage
      ;;
    *)
      debugMode
      break
      ;;
    esac
  done
fi


# Navigate to the project directory and run the server
cd "$SCRIPT_DIR" || { echo "Error: Failed to navigate to project directory."; exit 1; }

./apply_migrations.sh

# Run the Django development server
echo "Starting the Django development server..."
cat << "EOF"
 ____                 __                                  
/\  _`\              /\ \                                 
\ \ \L\ \ _ __   ___ \ \ \/'\      ___    _____      __   
 \ \ ,__//\`'__\/ __`\\ \ , <     / __`\ /\ '__`\  /'__`\ 
  \ \ \/ \ \ \//\ \L\ \\ \ \\`\  /\ \L\ \\ \ \L\ \/\  __/ 
   \ \_\  \ \_\\ \____/ \ \_\ \_\\ \____/ \ \ ,__/\ \____\
    \/_/   \/_/ \/___/   \/_/\/_/ \/___/   \ \ \/  \/____/
                                            \ \_\         
                                             \/_/         
EOF

python3 ./manage.py runserver