import os, math
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = 5
duration = 4.0
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([2]))).note
key = Note(key_note)

scales = ['major', 'pentatonicmajor']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
#notes = notes_from_scale(key.note, scale.intervals)
notes = notes_from_scale(key.note, scale.intervals)
random.shuffle(notes)
notesi = add_intervals_to_notes(notes)
#random.shuffle(notesi)

pp.pprint(key)
pp.pprint(r_scale)
pp.pprint(notes)

# Ascending arpeggio to open
for j, note in enumerate(notes):
    timeline.add(time + 0.40 * j, Hit(Note(note), duration))
time += duration
    
for i in range(20):
    for j, note in enumerate(notesi):
        interval = add_random_float(note[1], -1.24, 2.72)
        timeline.add(time + interval, Hit(Note(note[0]), duration))
    time += duration
    
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
#notes = notes_from_scale(key.note, scale.intervals)
notes = notes_from_scale(key.note, scale.intervals)
notesi = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(r_scale)
pp.pprint(notes)

# And breathe....
time += duration * 2.2 * math.sin(time)

for i in range(30):
    for j, note in enumerate(notesi):
        interval = note[1] #add_random_float(note[1], -0.25, 4.75)
        timeline.add(time + interval, Hit(Note(note[0]), duration))
    time += duration

# And breathe....
time += duration * 2.4 * math.sin(i)

# Descending arppegio to close
for j, note in enumerate(notes[::-1]):
    timeline.add(time + 1.40 * j, Hit(Note(note), duration))
time += duration * math.cos(duration)

print("Rendering audio...")
data = timeline.render()
#data = effect.tremolo(data, freq=1.7)
#data = effect.modulated_delay(data, data, 0.01, 0.002)
#data = effect.reverb(data, 0.8, 0.525)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

playback.play(data)