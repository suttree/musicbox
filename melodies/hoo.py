# Je n'est vivre

# To keep: oudh, pppony, Bb-asc/desc, slow
# To run: venv/bin/python3.12 melodies/stepping.py

# todo: use Ara melodies?
# todo: more notes in notes_from_scale
# todo: add interval to notes should pass a param that starts at 0.0 and increases (0.1, 0.2) etc, incl option to add noise to the increments)

# TODO: test the asc and desc parts individually, get them working
# TODO: export to wav for playback later

import os, math, random
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
key_note = Note('c#4').note
key = Note(key_note)

#scales = ['chromatic']
scales = ['ionian']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notesi = add_intervals_to_notes(notes)
pp.pprint(key)
pp.pprint(r_scale)

# Descending arppegio
for i in range(8):
  for j, note in enumerate(notes[::-2]):
      timeline.add(time + j*i, Hit(Note(notes[-1]), duration))
      timeline.add(time + j*i, Hit(Note(notesi[i][1]), duration))

      if (j > 0):
        timeline.add(time + j*i, Hit(Note(note).shift_up_octave(1), duration))
      
      r = list(notes)
      random.shuffle(r)
      for jj in r[::3]:
        timeline.add(time + j*i, Hit(Note(note), duration-(math.cos(0.27)*1)))
        
  time = time + 1.33

print("Rendering audio...")
data = timeline.render()
data = effect.simple_delay(data)
data = effect.shimmer(data, 0.24)
data = effect.echo(data)
data = effect.reverb(data, 0.8, 0.025)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)