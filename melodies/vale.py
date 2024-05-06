import os, math
from musical.theory import Note, Scale, Chord, Melody, Arpeggio
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

key_note = Note('g#4').note
key = Note(key_note)
scales = ['japanese']
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = notes_from_scale(key.note, scale.intervals, 2)
notesi = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(r_scale)

time = 0.0
localtime = time

measure_duration = 10.00
duration = measure_duration/4
whole_note = duration
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

timeline = Timeline()

for i in range(12):
  timeline.add(time + half_note, Hit(Note(notes[0]), duration))
  time += duration
  timeline.add(time + sixteenth_note, Hit(Note(notes[2]), duration))
  time += duration
  timeline.add(time + sixteenth_note, Hit(Note(notes[0]), duration))
  time += measure_duration

# Render the audio from the timeline
data = timeline.render(3)
data = effect.echo(data)
#data = effect.autowah(data, (200, 800))
data = effect.flanger(data, freq=0.025)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

# Play the audio
#playback.play(data)