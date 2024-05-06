import os, math
from musical.theory import Note, Scale, Chord, Melody
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

key_note = Note((random.choice(Note.NOTES), random.choice([1, 2]))).note
key = Note(key_note)
scales = ['major', 'pentatonicmajor', 'japanese', 'locrian', 'ionian', 'mixolydian', 'phrygian']
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)

time = 0.0
localtime = time

measure_duration = 10.00
duration = measure_duration/4
whole_note = duration
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

timeline = Timeline()

# Create a melody from a C major scale
melody = Melody.from_scale('C', 'major')

# Play the melody
for note, duration in melody.play(duration=0.5, octaves=2):
    # Generate audio for each note and duration
    timeline.add(time + eighth_note, Hit(Note(note), duration))

time += duration

# Create an ascending melody
melody.ascending()

# Play the ascending melody
for note, duration in melody.play(duration=0.25, octaves=1):
    # Generate audio for each note and duration
    timeline.add(time + eighth_note, Hit(Note(note), duration))

time += duration

data = timeline.render()
data = effect.simple_delay(data)
data = effect.echo(data)

#from musical.utils import save_normalized_audio
#save_normalized_audio(data, 44100, os.path.basename(__file__))

playback.play(data)