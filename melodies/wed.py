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
iterations = random.randint(8, 28)
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

def play_chord(notes, duration):
  timeline.add(time, Hit(Note(notes[0]), duration))
  timeline.add(time, Hit(Note(notes[2]).shift_down_octave(2), duration))
  timeline.add(time, Hit(Note(notes[3]), duration))
  timeline.add(time, Hit(Note(notes[5]), duration))

for i in range(iterations):
  play_chord(notes, measure_duration*2)
  for j, note in enumerate(notes[::-2]):
    timeline.add(time + eighth_note, Hit(Note(note), duration*2))
    timeline.add(time + eighth_note + eighth_note, Hit(Note(note), duration*2))
    
  #time += half_measure
  #play_chord(notes[::1], duration)
  #for j, note in enumerate(notes[::-2]):
  #  timeline.add(time + eighth_note, Hit(Note(note), duration*2))
    
  #play_chord(notes[0::5], duration)
  #for j, note in enumerate(notes[2::]):
  #  timeline.add(time + eighth_note, Hit(Note(note), duration*2))
  #  timeline.add(time + eighth_note + eighth_note, Hit(Note(note), duration*2))

  #for j, note in enumerate(notes[::-4]):
  #  timeline.add(time + eighth_note, Hit(Note(note), duration))

  time += duration * 2
  random.shuffle(notes)
time += duration * 2

notes = extended_notes_from_scale(key.note, scale.intervals, 2)
for j, note in enumerate(notes[::-4]):
  timeline.add(time + eighth_note, Hit(Note(note), duration))
  time += 0.1
  
print("Rendering audio...")
data = timeline.render()

#data = effect.simple_delay(data, 250, 0.98, 1.77)
#data = effect.shimmer(data, 0.234)
data = effect.reverb(data, 0.8, 0.525)
data = effect.echo(data)
data = effect.simple_delay(data, 128, 0.09, 0.77)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)
