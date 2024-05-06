from .scale import Scale
from .note import Note

import random

class Melody:
    ''' Melody class for creating and manipulating melodies
    '''
    def __init__(self, scale, pattern=None, shuffle=True):
        self.scale = scale
        self.notes = list(scale)
        if shuffle:
            random.shuffle(self.notes)
        self.pattern = pattern if pattern else self.generate_pattern()

    def __repr__(self):
        return 'Melody(%s)' % repr(self.notes)

    def __len__(self):
        return len(self.notes)

    def __iter__(self):
        return iter(self.notes)

    def generate_pattern(self):
        ''' Generate a random pattern for the melody
        '''
        pattern = []
        for i in range(len(self.notes)):
            if i % 2 == 0:
                pattern.append(i)
            else:
                pattern.append(len(self.notes) - i - 1)
        return pattern

    def play(self, duration=0.25, octaves=1):
        ''' Play the melody with the given duration and number of octaves
        '''
        for octave in range(octaves):
            for i in self.pattern:
                yield self.notes[i % len(self.notes)].transpose(12 * octave), duration

    @classmethod
    def from_scale(cls, root, scale_type, shuffle=True):
        ''' Create a melody from a scale
        '''
        root_note = Note(root)
        scale = Scale(root_note, scale_type)
        return cls(scale, shuffle=shuffle)

    def ascending(self):
        ''' Create an ascending melody
        '''
        self.pattern = sorted(range(len(self.notes)))

    def descending(self):
        ''' Create a descending melody
        '''
        self.pattern = sorted(range(len(self.notes)), reverse=True)

    def shuffle(self):
        ''' Shuffle the notes of the melody
        '''
        random.shuffle(self.notes)
        self.pattern = self.generate_pattern()
        
"""
# Create a melody from a C major scale
melody = Melody.from_scale('C', 'major')

# Play the melody
for note, duration in melody.play(duration=0.5, octaves=2):
    # Generate audio for each note and duration
    # ...

# Create an ascending melody
melody.ascending()

# Play the ascending melody
for note, duration in melody.play(duration=0.25, octaves=1):
    # Generate audio for each note and duration
    # ...
"""