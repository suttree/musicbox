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

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = 5
duration = 1.4287
measure_duration = 4.826
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([2]))).note
key = Note(key_note)

scales = ['pentatonicmajor', 'major', 'mixolydian']
#scales = ['major', 'pentatonicmajor', 'japanese', 'diminished', 'locrian', 'ionian', 'mixolydian', 'phrygian']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)
pp.pprint(key)
pp.pprint(r_scale)

for n in range(4):
  for i in range(8):
    for j, note in enumerate(notes_with_intervals[::-1]):
      timeline.add(time + 0.25 * j*i, Hit(Note(note[0]), duration))
      if i > 2:
        timeline.add(time + 1.00 * j*i, Hit(Note(note[0]), duration)) 
      if i > 4:
        timeline.add(time + 2.00 * j*i, Hit(Note(note[0]), duration))
    # lullaby
    for j, note in enumerate(notes_with_intervals[::-1]):
      timeline.add(time + 0.25 * j*i, Hit(Note(note[0]), duration))
      if i > 2:
        timeline.add(time + 1.00 * j*i, Hit(Note(note[0]), duration)) 
      if i > 4:
        timeline.add(time + 2.00 * j*i, Hit(Note(note[0]), duration))

  #time += measure_duration

print("Rendering audio...")
data = timeline.render()
#data = effect.tremolo(data, freq=1.7)
data = effect.shimmer(data, 0.16)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

playback.play(data)