#!/bin/bash

# Run volume.sh script
./volume.sh

# Directory containing the files
DIR="melodies"

# Check if the directory exists
if [ ! -d "$DIR" ]; then
    echo "Directory $DIR does not exist."
    exit 1
fi

# Infinite loop
while true; do
    # Get a list of .py files in the directory
    FILES=($DIR/*.py)

    # Check if there are any .py files
    if [ ${#FILES[@]} -eq 0 ]; then
        echo "No .py files found in $DIR."
        exit 1
    fi

    # Pick a random file
    RANDOM_FILE=${FILES[RANDOM % ${#FILES[@]}]}

    # Execute the file
    echo "Running: $RANDOM_FILE"
    /usr/bin/env python3 "$RANDOM_FILE"

    # Wait for a moment before running the next file
    echo "Execution finished. Picking another file..."
    sleep 1
done
