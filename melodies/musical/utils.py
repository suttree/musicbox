import random,os
from datetime import datetime
import soundfile as sf
import numpy as np
from scipy.signal import butter, lfilter

import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter
from datetime import datetime

def save_normalized_audio(data, samplerate=44100, current_script_filename=''):
    # Save the rendered audio to a temporary file
    temp_file = "tmp/temp_audio.wav"
    sf.write(temp_file, data, samplerate=samplerate)

    audio, sr = sf.read(temp_file)
    normalized_audio = audio / np.max(np.abs(audio))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output/{current_script_filename}_output_{timestamp}.wav"

    sf.write(output_file, normalized_audio, samplerate=sr)

    print(f"Audio exported as {output_file}")

    return output_file
    
def notes_from_scale(starting_note, intervals, octave=4):
    starting_note = starting_note[0].upper()
    
    # Define the order of notes in the musical alphabet
    musical_alphabet = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Initialize a list to store the notes
    scale = []
    
    # Find the index of the starting note in the musical alphabet
    current_note_index = musical_alphabet.index(starting_note)
    
    # Append the starting note to the scale with the specified octave
    scale.append(starting_note + str(octave))
    
    for interval in intervals[:-1]:  # Exclude the last interval
        # Calculate the next note index by adding the interval to the current note index
        next_note_index = (current_note_index + interval) % 12
        
        # Determine the octave of the next note
        if next_note_index < current_note_index:
            octave += 1
        
        next_note = musical_alphabet[next_note_index]
        
        # Append the next note to the scale with the appropriate octave
        scale.append(next_note + str(octave))
        
        # Update the current note index for the next iteration
        current_note_index = next_note_index
    
    return scale

def extended_notes_from_scale(starting_note, intervals, num_octaves=2, default_octave=3):
    # Define the order of notes in the musical alphabet
    musical_alphabet = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Initialize a list to store the notes
    scale = []
    
    # Extract the note name and octave number from the starting note
    note_name = starting_note[:-1].upper() if starting_note[-1].isdigit() else starting_note.upper()
    octave = int(starting_note[-1]) if starting_note[-1].isdigit() else default_octave
    
    # Find the index of the starting note in the musical alphabet
    current_note_index = musical_alphabet.index(note_name)
    
    for _ in range(num_octaves):
        for interval in intervals:
            # Append the current note to the scale with the appropriate octave
            scale.append(musical_alphabet[current_note_index] + str(octave))
            
            # Calculate the next note index by adding the interval to the current note index
            next_note_index = (current_note_index + interval) % 12
            
            # Increment the octave if the next note crosses the octave boundary
            if next_note_index < current_note_index:
                octave += 1
            
            # Update the current note index for the next iteration
            current_note_index = next_note_index
    
    return scale

def add_intervals_to_notes(notes):
    notes_with_intervals = []
    interval = 0.0
    
    for note in notes:
        notes_with_intervals.append([note, add_random_float(interval, -0.8, 1.02)])
        interval += 1.2

    return notes_with_intervals
    
def add_random_float(value, min_val=0.0, max_val=1.0):
    random_float = random.uniform(min_val, max_val)
    return round(value + random_float, 2)