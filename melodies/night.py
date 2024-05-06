import os, math
from musical.theory import Note, Scale, Chord, Melody, Arpeggio
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

key_note = Note((random.choice(Note.NOTES), random.choice([1, 2]))).note
key = Note(key_note)
scales = ['major', 'pentatonicmajor', 'japanese', 'locrian', 'ionian', 'mixolydian', 'phrygian']
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)

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

# Create a note
root_note = Note('C4')

# Create a chord from the note
chord = Chord.major(root_note)

# Create an arpeggio from the chord
arpeggio = Arpeggio(chord.notes)

# Create a timeline to store the audio events
timeline = Timeline()

# Play the ascending arpeggio and add the notes to the timeline
time = 0
for i in range(2):
  for note, duration in Arpeggio.ascending(arpeggio.notes).play(duration=0.25, octaves=2):
      hit = Hit(note, half_note)
      timeline.add(time, hit)
      time += eighth_note

  # Play the descending arpeggio and add the notes to the timeline
  for note, duration in Arpeggio.descending(arpeggio.notes).play(duration=0.25, octaves=2):
      hit = Hit(note, quarter_note)
      timeline.add(time, hit)
      time += sixteenth_note

# Render the audio from the timeline
data = timeline.render()
data = effect.simple_delay(data)
#data = effect.pitch_shift(data, 3)
data = effect.echo(data)
#data = effect.wah(data)

# Play the audio
playback.play(data)