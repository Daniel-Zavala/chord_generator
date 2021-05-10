# constants for music generation algorithm
# created as own class to facilitate customization

import pychord
import pretty_midi

class constants:
    
    def __init__(self):
        
        self.repetitions = 1 # number of chord sets generated (text file and midi file)
        self.chordn = 1 # number of chords per set
        self.length = 1 # note duration; duration = 60 bpm / length
        self.velocity = 100 # wat?
        self.notes = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
        self.qualities = [] # qualities for generating chords
        self.qn = [] # number of notes per chord, related ot qualities, upper limit of qualities list when randomizing
        self.inst_group = 1 # instrument group to be used by Pretty Midi
        self.chords_str = [] # list where the series of chords generated will be stored
        self.instruments = pretty_midi.constants.INSTRUMENT_MAP
        
        for x in pychord.constants.qualities.DEFAULT_QUALITIES:
            self.qualities.append(str(x[0]))


constants = constants() # instantiate object