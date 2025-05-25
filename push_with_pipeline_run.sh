#!/bin/bash

PROJECT_PATH=~/KState/Prokope
RUNNER_PATH=~/Development/actions-runner

cd "$RUNNER_PATH" || {
    echo "Runner directory not found: $RUNNER_PATH"
    exit 1
}

echo "Starting GitHub Actions runner..."
./svc.sh start --once

echo "Pushing update to remote repo..."
cd "$PROJECT_PATH"
git push
cd "$RUNNER_PATH"

# Wait for the runner to finish
while ./svc.sh status | grep -q "active"; do
    sleep 1
done

echo "GitHub Actions - Runner completed job."
