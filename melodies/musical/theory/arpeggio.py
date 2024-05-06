class Arpeggio:
    ''' Arpeggio class for creating and manipulating arpeggios
    '''
    def __init__(self, notes, pattern=None):
        self.notes = tuple(notes)
        self.pattern = pattern if pattern else [0, 1, 2, 3]

    def __repr__(self):
        return 'Arpeggio(%s)' % repr(self.notes)

    def __len__(self):
        return len(self.notes)

    def __iter__(self):
        return iter(self.notes)

    def play(self, duration=0.25, octaves=1):
        ''' Play the arpeggio with the given duration and number of octaves
        '''
        for octave in range(octaves):
            for i in self.pattern:
                yield self.notes[i % len(self.notes)].transpose(12 * octave), duration

    @classmethod
    def from_chord(cls, chord, pattern=None):
        ''' Create an arpeggio from a chord
        '''
        return cls(chord.notes, pattern)

    @classmethod
    def ascending(cls, notes):
        ''' Create an ascending arpeggio
        '''
        return cls(notes, [0, 1, 2, 3])

    @classmethod
    def descending(cls, notes):
        ''' Create a descending arpeggio
        '''
        return cls(notes, [3, 2, 1, 0])