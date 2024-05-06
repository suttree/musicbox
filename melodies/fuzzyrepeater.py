# Je n'est vivre

# To keep: oudh, pppony, Bb-asc/desc, slow
# To run: venv/bin/python3.12 melodies/stepping.py

# todo: use Ara melodies?
# todo: more notes in notes_from_scale
# todo: add interval to notes should pass a param that starts at 0.0 and increases (0.1, 0.2) etc, incl option to add noise to the increments)

# TODO: test the asc and desc parts individually, get them working
# TODO: export to wav for playback later

import os
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random
import wave
import numpy as np
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
offset = 0.4286
iterations = 4
duration = 4.286 # 140bpm
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([2,3]))).note
key = Note(key_note)

#scales = ['chromatic','major', 'pentatonicmajor']
scales = ['major', 'pentatonicmajor', 'ionian', 'phrygian']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 1)
notes_with_intervals = add_intervals_to_notes(notes)
pp.pprint(key)
pp.pprint(r_scale)

# fuzzy repeater
for i in range(iterations):
    # a classic waterfall/cascade, removed for now though
    #for j, note in enumerate(notes[::-1]):
    #    timeline.add(time+0.075*j+1, Hit(Note(note), duration))
    #time += duration

    # Ascending & desending xover
    for j, note in enumerate(notes):
      timeline.add(time + 0.25*j*2, Hit(Note(note), duration))
    # Descending arppegio
    for j, note in enumerate(notes[::-1]):
      timeline.add(time + 0.25*j*2, Hit(Note(note), duration))
    time += duration

    for n in range(8):
      for j, note in enumerate(notes[::-1]):
          timeline.add(time + offset * j, Hit(Note(note), duration))
          timeline.add(duration/4 + time + offset * j, Hit(Note(note), duration))
      time += duration/2

    # Cavernous ascender
    for j, note in enumerate(notes):
        timeline.add(time+0.95*j, Hit(Note(note), duration))
    time += duration

print("Rendering audio...")
data = timeline.render()
effect.shimmer(data, 0.24)
effect.tremolo(data, 0.1)
#effect.reverb(data, 0.8, 0.025)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

playback.play(data)