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
iterations = random.randint(8, 22)
duration = 4.0
timeline = Timeline()

measure_duration = 16.00
half_measure = measure_duration/2
duration = measure_duration/4
whole_note = duration
three_quarter_note = duration * 0.75
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([2]))).note
key = Note(key_note)

scales = ['ionian', 'phrygian', 'major']
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)

pp.pprint(key)
pp.pprint(r_scale)

for i in range(iterations):
  timeline.add(time + sixteenth_note, Hit(Note(notes[0]).shift_up_octave(1), duration/2))
  timeline.add(time + sixteenth_note, Hit(Note(notes[2]), duration))

  timeline.add(time + eighth_note, Hit(Note(notes[-2]), duration))
  timeline.add(time + eighth_note, Hit(Note(notes[-5]), duration))

  timeline.add(time + quarter_note, Hit(Note(notes[0]).shift_up_octave(1), duration/2))
  timeline.add(time + quarter_note, Hit(Note(notes[4]), duration))

  timeline.add(time + half_note, Hit(Note(notes[0]).shift_down_octave(1), duration))
  
  for j in range(i):
    x = j % 2
    timeline.add(time + three_quarter_note, Hit(Note(notes[0]).shift_up_octave(x), duration))
    timeline.add(time + three_quarter_note, Hit(Note(notes[5]).shift_up_octave(x), duration))
  
  time += duration + math.cos(duration) * math.sin(i+1)
  
  # melodie
  for j, note in enumerate(notes[0::-2]):
    timeline.add(time + eighth_note, Hit(Note(note), duration*2))
  for j, note in enumerate(notes[5::3]):
    timeline.add(time + eighth_note, Hit(Note(note), duration))

  timeline.add(time + sixteenth_note, Hit(Note(notes[3]), duration))
  timeline.add(time + sixteenth_note/2, Hit(Note(notes[5]), duration))

  time += duration + math.cos(duration)
time += duration + math.sin(duration)

print("Rendering audio...")
data = timeline.render()

data = effect.simple_delay(data, 500, 0.2, 1.77)
data = effect.shimmer(data, 0.234)
data = effect.autowah(data, (200, 1000))
data = effect.reverb(data, 0.8, 0.525)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)