#!/bin/bash

# Set the path to the "output" folder
output_folder="output"

# Function to play the shuffled .wav files
play_shuffled_files() {
    # Get an array of all the .wav files in the "output" folder
    wav_files=("$output_folder"/*.wav)
    
    # Get the total number of .wav files
    num_files=${#wav_files[@]}
    
    # Shuffle the array randomly
    shuffled_files=( $(shuf -e "${wav_files[@]}") )
    
    # Play the shuffled .wav files using aplay
    for file in "${shuffled_files[@]}"
    do
        source "~/src/pele/.volume.py"
        echo "Playing: $file"
        aplay "$file"
        sleep_duration=$((RANDOM % 61 + 30))
        sleep $sleep_duration
    done
}

# Function to check if the current time is within the specified ranges
is_within_time_range() {
    current_hour=$(date +%H)
    
    if [[ $current_hour -ge 6 && $current_hour -lt 9 ]] || [[ $current_hour -ge 18 && $current_hour -lt 23 ]]; then
        return 0  # Within the specified time range
    else
        return 1  # Outside the specified time range
    fi
}

# Continuously monitor the "output" folder and play new files within the specified time ranges
while true
do
    if is_within_time_range; then
        echo "Monitoring the 'output' folder for new .wav files..."
        # Play the shuffled .wav files
        play_shuffled_files
        echo "All files have been played. Restarting the playlist..."
    else
        echo "Current time is outside the specified ranges. Waiting..."
    fi
    
    sleep 60  # Wait for 60 seconds before checking again
done
