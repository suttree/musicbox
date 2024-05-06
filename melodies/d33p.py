# Je n'est vivre

# To keep: oudh, pppony, Bb-asc/desc, slow
# To run: venv/bin/python3.12 melodies/stepping.py

# todo: use Ara melodies?
# todo: more notes in notes_from_scale
# todo: add interval to notes should pass a param that starts at 0.0 and increases (0.1, 0.2) etc, incl option to add noise to the increments)

# TODO: test the asc and desc parts individually, get them working
# TODO: export to wav for playback later

import os, math
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random
import wave
import numpy as np
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)

time = 0.0 
offset = 0.0
iterations = 5
duration = 4.24
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([2]))).note
key = Note(key_note)

scales = ['chromatic', 'major', 'pentatonicmajor', 'mixolydian']
alt_scales = ['japanese', 'diminished', 'locrian', 'ionian', 'mixolydian', 'phrygian']
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)

for x in range(1):
  for i in range(8):
    for j, note in enumerate(notes[::-1]):
        inc = 0.025 * math.sin(j+1) * i+1``
        if j % 2 == 0:
          inc += math.cos(j*0.25)
        timeline.add(time + inc, Hit(Note(note), duration + inc))
        if i % 5 == 0:
          timeline.add(time + inc, Hit(Note(note), duration + inc - 0.25))

    #duration += math.sin(0.276) * (i+1)
    duration += 0.246 - math.sin(i)/2``
    pp.pprint(duration))

    if duration >+ 14.4:
      duration = 4.281 + math.cos(1.40)/2
    time += duration

print("Rendering audio...")
data = timeline.render()
#data = effect.modulated_delay(data, data, 0.002, 0.023)
data = effect.reverb(data, 0.8, 0.425)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

playback.play(data)
