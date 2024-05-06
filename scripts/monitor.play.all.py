import os
import random
import time
from datetime import datetime
from pydub import AudioSegment
from scipy.signal import butter, sosfilt

# Set the path to the "output" folder
output_folder = "output"

def process_audio(file_path):
    # Load the audio file
    audio = AudioSegment.from_wav(file_path)

    # Normalize the audio
    normalized_audio = audio.normalize()

    # Apply dynamic range compression
    compressed_audio = normalized_audio.compress_dynamic_range()

    # Apply a high-pass filter to reduce bass frequencies
    cutoff_freq = 100  # Adjust the cutoff frequency as needed
    sample_rate = compressed_audio.frame_rate
    order = 4

    # Design the high-pass filter
    sos = butter(order, cutoff_freq, 'hp', fs=sample_rate, output='sos')

    # Apply the filter to the audio samples
    filtered_samples = sosfilt(sos, compressed_audio.get_array_of_samples())

    # Create a new audio segment with the filtered samples
    filtered_audio = compressed_audio._spawn(filtered_samples)

    return filtered_audio

def play_shuffled_files():
    # Get a list of all the .wav files in the "output" folder
    wav_files = [file for file in os.listdir(output_folder) if file.endswith(".wav")]

    # Shuffle the list randomly
    random.shuffle(wav_files)

    # Play the shuffled .wav files
    for file in wav_files:
        file_path = os.path.join(output_folder, file)
        print("Playing:", file)

        # Process the audio file
        processed_audio = process_audio(file_path)

        # Play the processed audio
        processed_audio.export("temp.wav", format="wav")
        os.system("amixer sset 'Master' 50%")
        os.system("aplay temp.wav")
        os.remove("temp.wav")

        # Sleep for a random duration between 30 and 90 seconds
        sleep_duration = random.randint(30, 90)
        time.sleep(sleep_duration)

def is_within_time_range():
    current_hour = datetime.now().hour
    return (6 <= current_hour < 13) or (18 <= current_hour < 23)

# Continuously monitor the "output" folder and play new files within the specified time ranges
while True:
    if is_within_time_range():
        print("Monitoring the 'output' folder for new .wav files...")
        play_shuffled_files()
        print("All files have been played. Restarting the playlist...")
    else:
        print("Current time is outside the specified ranges. Waiting...")

    time.sleep(60)  # Wait for 60 seconds before checking again
