#!/bin/bash

RUNNER_PATH=~/Development/actions-runner

cd "$RUNNER_PATH" || {
    echo "Runner directory not found: $RUNNER_PATH"
    exit 1
}

echo "Starting GitHub Actions runner..."
./svc.sh start --once

# Wait for the runner to finish
while ./svc.sh status | grep -q "active"; do
    sleep 1
done

echo "GitHub Actions runner job."
