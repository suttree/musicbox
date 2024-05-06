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
scales = ['major']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)
pp.pprint(key)
pp.pprint(r_scale)

# Descending arppegio
for i in range(6):
  for j, note in enumerate(notes[::-2]):
      timeline.add(time + j*i, Hit(Note(notes[-1]), duration))
      if (j > 0):
        timeline.add(time + j*i, Hit(Note(note), duration))
      
      r = list(notes)
      random.shuffle(r)
      for jj in r[::-3]:
        timeline.add(time + j*i, Hit(Note(note), duration-(math.cos(0.25)*1)))

      random.shuffle(r)
      for jj in r[::-3]:
        timeline.add(time + j*i, Hit(Note(note), duration+(math.sin(0.25)*1)))

#      for k, note in enumerate(notes):
#        if k > 0 and k % 2 == 0:
#          timeline.add(time + j*i, Hit(Note(note), duration-0.25))

      for l, note in enumerate(notes[2::]):
        if l > 0 and l % 4 == 0:
          timeline.add(time + l*i, Hit(Note(notes[-1]), duration))
          timeline.add(time + 0.025 + l*i, Hit(Note(notes[-1]), duration))
        timeline.add(time + l*i, Hit(Note(note), duration))

      time = time + 1.33
      
      if j > 3:
        timeline.add(time + 0.22 + j*i, Hit(Note(notes[-1]), duration*0.75))
        timeline.add(time + 0.22 + j*i, Hit(Note(notes[1]), duration*0.75))

#  duration += 0.5
#  time += 0.5
#
#duration -= 1.0
#time += 2.0
#
#for i in range(2):
#  for j, note in enumerate(notes[2::]):
#      #pp.pprint(note)
#      timeline.add(time + j*i, Hit(Note(notes[-1]), duration))
#      timeline.add(time + j*i, Hit(Note(note), duration))
#  duration += 0.5
#  time += 0.5
#  
print("Rendering audio...")
data = timeline.render()
data = effect.shimmer(data, 0.24)
data = effect.echo(data)
data = effect.pitch_shift(data, 2)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)