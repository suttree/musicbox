#!/bin/bash

# Set the path to the "output" folder
output_folder="output"

# Get an array of all the .wav files in the "output" folder
wav_files=("$output_folder"/*.wav)

# Get the total number of .wav files
num_files=${#wav_files[@]}

# Shuffle the array randomly
shuffled_files=( $(shuf -e "${wav_files[@]}") )

# Play the shuffled .wav files using aplay
for file in "${shuffled_files[@]}"
do
  echo "Playing: $file"
  aplay "$file"
done

echo "All files have been played."
