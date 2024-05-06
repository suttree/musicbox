# Je n'est vivre

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
increment = math.sin(0.1975)
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([2]))).note
key = Note(key_note)

scales = ['major', 'pentatonicmajor']
#scales = ['japanese', 'locrian', 'ionian', 'mixolydian', 'phrygian']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
#notes = notes_from_scale(key.note, scale.intervals)
notes = notes_from_scale(key.note, scale.intervals)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(r_scale)

# arppegio to open
for i in range(6):
  for i in range(4):
    localtime = time
    for j, note in enumerate(notes):
        timeline.add(time + 0.40, Hit(Note(notes[0]).shift_up_octave(1), duration/2))
    for j, note in enumerate(notes[::2]):
        timeline.add(localtime + 1.40, Hit(Note(note), duration))
        localtime += increment
    for j, note in enumerate(notes[::5]):
        timeline.add(localtime + 1.40, Hit(Note(note), duration))
        localtime += increment * math.sin(i)
    locatime = time
    time += duration

  key_note = Note((random.choice(Note.NOTES), random.choice([1, 2]))).note
  key = Note(key_note)
  notes = notes_from_scale(key.note, scale.intervals)
  notes_with_intervals = add_intervals_to_notes(notes)

  for i in range(4):
    localtime = time
    for j, note in enumerate(notes):
        timeline.add(time + 0.40, Hit(Note(notes[0]), duration/2))
    for j, note in enumerate(notes[::2]):
        timeline.add(localtime + 1.40, Hit(Note(note), duration))
        localtime += increment
    for j, note in enumerate(notes[::5]):
        timeline.add(localtime + 1.40, Hit(Note(note), duration))
        localtime += increment * math.sin(i)
    locatime = time
    time += duration
    
  key_note = Note((random.choice(Note.NOTES), random.choice([1, 2]))).note
  key = Note(key_note)
  notes = notes_from_scale(key.note, scale.intervals)
  notes_with_intervals = add_intervals_to_notes(notes)
  
  #duration -= math.cos(i)
  #  
  #for j, note in enumerate(notes_with_intervals):
  #    timeline.add(time + increment, Hit(Note(note[0]), note[1]))
  #time += duration
  #increment -= math.cos(increment)



## Ascending arpeggio to open
#for j, note in enumerate(notes):
#    timeline.add(time + 0.40 * j + math.sin(increment), Hit(Note(note), duration))
#for j, note in enumerate(notes[::2]):
#    timeline.add(time + 0.40 * j + math.cos(increment), Hit(Note(note), duration))
#time += duration + increment
#increment += math.sin(increment)
#    
#for i in range(80):
#    for j, note in enumerate(notes_with_intervals):
#        interval = add_random_float(note[1], math.cos(increment), math.sin(increment))
#        timeline.add(time + interval, Hit(Note(note[0]), note[1]))
#    time += duration
#    increment -= math.sin(increment)
#    
#r_scale = random.choice(scales)
#scale = Scale(key, r_scale)
#notes = notes_from_scale(key.note, scale.intervals)
#notes_with_intervals = add_intervals_to_notes(notes)
#
## And breathe....
#time += duration * 2.2
#
#for i in range(30):
#    for j, note in enumerate(notes_with_intervals):
#        interval = add_random_float(note[1], -math.cos(increment), math.sin(increment))
#        timeline.add(time + interval, Hit(Note(note[0]), duration))
#        timeline.add(time + increment, Hit(Note(note[0]), duration))
#    time += duration
#    increment -= math.cos(increment)
#
## And breathe....
#time += duration * 2.4

print("Rendering audio...")
data = timeline.render()
data = effect.shimmer(data, 0.024)
data = effect.tremolo(data, freq=0.4)
data = effect.reverb(data, 0.8, 0.0525)
data = effect.pitch_shift(data, 2)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)