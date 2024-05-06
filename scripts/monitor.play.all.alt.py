import os
import random
import time
from pydub import AudioSegment

# Set the path to the "output" folder
output_folder = "output"

# Function to generate silent audio
def generate_silence(duration_ms):
    return AudioSegment.silent(duration=duration_ms)

# Function to play the shuffled .wav files
def play_shuffled_files():
    # Get a list of all the .wav files in the "output" folder
    wav_files = [file for file in os.listdir(output_folder) if file.endswith(".wav")]

    # Shuffle the list randomly
    random.shuffle(wav_files)

    # Play the shuffled .wav files using aplay
    for file in wav_files:
        # Set the volume to 50%
        os.system("amixer sset 'Master' 75%")
        
        # Load the audio file
        audio = AudioSegment.from_wav(os.path.join(output_folder, file))

        # Apply a low-pass filter at 200Hz
        low_pass_audio = audio.low_pass_filter(200)

        # Export the filtered audio to a temporary file
        temp_file = "temp.wav"
        low_pass_audio.export(temp_file, format="wav")

        # Play the filtered audio using aplay
        print(f"Playing: {file}")
        os.system(f"aplay {temp_file}")

        # Remove the temporary file
        os.remove(temp_file)

        # Generate 30 seconds of silent audio
        silent_audio = generate_silence(30000)  # 30 seconds in milliseconds
        silent_audio.export("silent.wav", format="wav")
        os.system("aplay silent.wav")
        os.remove("silent.wav")

        # Generate a random sleep duration between 30 and 90 seconds
        sleep_duration = random.randint(30, 90)
        print(f"Sleeping for {sleep_duration} seconds...")
        time.sleep(sleep_duration)

# Function to check if the current time is within the specified ranges
def is_within_time_range():
    current_hour = int(time.strftime("%H"))
    current_day = int(time.strftime("%w"))  # 0 for Sunday, 6 for Saturday

    # Check if it's not a weekend and the time is within the specified ranges
    if current_day != 0 and current_day != 6:
        return (6 <= current_hour < 9) or (12 <= current_hour < 14) or (18 <= current_hour < 23)
    else:
        return (12 <= current_hour < 14) or (18 <= current_hour < 23)

# Continuously monitor the "output" folder and play new files within the specified time ranges
while True:
    if is_within_time_range():
        print("Monitoring the 'output' folder for new .wav files...")
        play_shuffled_files()
        print("All files have been played. Restarting the playlist...")
    else:
        print("Current time is outside the specified ranges. Waiting...")

    # Wait for 60 seconds before checking again
    time.sleep(60)
