# Je n'est vivre

# To keep: oudh, pppony, Bb-asc/desc, slow
# To run: venv/bin/python3.12 melodies/stepping.py

# todo: use Ara melodies?
# todo: more notes in notes_from_scale
# todo: add interval to notes should pass a param that starts at 0.0 and increases (0.1, 0.2) etc, incl option to add noise to the increments)

# TODO: test the asc and desc parts individually, get them working
# TODO: export to wav for playback later


from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random
import wave, os, math
import numpy as np
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = 5
duration = 6.0
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([2]))).note
key = Note(key_note)

#scales = ['chromatic']
scales = ['major', 'pentatonicmajor', 'japanese', 'diminished', 'locrian', 'ionian', 'mixolydian', 'phrygian']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(r_scale)

# Descending arppegio
for n in range(4):
  for i in range(8):
    # simple cascade w/ overlap
    for j, note in enumerate(notes_with_intervals[::-1]):
      if i > 2:
        # add an incidental melody
        interval = 1.0
        timeline.add(time + 0.25 * j*i * math.cos(interval), Hit(Note(note[0]), duration))
        
      timeline.add(time + 0.25 * j*i, Hit(Note(note[0]), duration))

    time += duration

  if n > 3:
    for y, note in enumerate(notes_with_intervals[::-1]):
      interval = add_random_float(note[1], -0.25, 4.75)
      timeline.add(time + 0.25 * n*i + interval, Hit(Note(note[0]), duration))

print("Rendering audio...")
data = timeline.render()
data = effect.shimmer(data, 0.24)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

playback.play(data)