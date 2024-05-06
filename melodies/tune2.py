import os, math
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random
pp = pprint.PrettyPrinter(indent=4)

key_note = Note((random.choice(Note.NOTES), random.choice([0, 1, 2, 3]))).note
key = Note(key_note)
scales = ['japanese', 'locrian', 'ionian', 'mixolydian', 'phrygian']
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = notes_from_scale(key.note, scale.intervals, 4)
notes_with_intervals = add_intervals_to_notes(notes)

time = 0.0
localtime = time

measure_duration = 16.00
half_measure = measure_duration/2
duration = measure_duration/4
whole_note = duration
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

timeline = Timeline()
notes = notes_from_scale(key.note, scale.intervals)
notesi = add_intervals_to_notes(notes)

pp.pprint(scale)
pp.pprint(key)
pp.pprint(r_scale)

for j in range(6):  
  timeline.add(time + sixteenth_note, Hit(Note(notes[2]), duration))
  timeline.add(time + sixteenth_note, Hit(Note(notes[4]), duration))
  
  timeline.add(time + eighth_note, Hit(Note(notes[-2]), duration))
  timeline.add(time + eighth_note, Hit(Note(notes[-4]), duration))
  
  timeline.add(time + quarter_note, Hit(Note(notes[0]), duration))
  timeline.add(time + quarter_note, Hit(Note(notes[1]).shift_down_octave(2), duration))

  timeline.add(time + half_note, Hit(Note(notes[0]).shift_down_octave(1), duration))
  
  time += duration
  
  if j >= 0 and j % 2 == 0:  
    timeline.add(time + quarter_note, Hit(Note(notes[0]).shift_down_octave(2), half_measure))

    time += half_note
    for j, note in enumerate(notes[2::-2]):
        timeline.add(time + eighth_note, Hit(Note(note), duration))

    time += math.sin(time) * j
  time += math.cos(time) * j
  
data = timeline.render()
data = effect.shimmer(data, 0.24)
data = effect.flanger(data, freq=0.025)
data = effect.chorus(data, freq=0.04)
data = effect.reverb(data, 0.8, 0.425)

data = data * 0.1
from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

playback.play(data)
