#!/bin/bash

# Set the path to the folder containing the WAV files
folder_path="output/"

# Set the target volume level in dB (decibels)
target_volume="-10"

# Iterate over the WAV files in the folder
for file in "$folder_path"/*.wav; do
    # Check if the file exists
    if [ -e "$file" ]; then
        # Get the base filename without the extension
        filename=$(basename "$file" .wav)
        
        # Normalize the volume using ffmpeg
        ffmpeg -i "$file" -filter:a "volume=${target_volume}dB" "normalized_${filename}.wav"
        
        echo "Normalized $file"
    fi
done
