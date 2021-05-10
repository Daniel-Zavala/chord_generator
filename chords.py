# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Daniel Zavala Salazar | May 2021                                      #
#                                                                       #
# Final Project | MGT 828 - Creativity & Innovation                     #
# Yale SOM - Prof. J. Feinstein                                         #
#                                                                       #
# This is a program that generates series of musical chords through     #
# randomness. It exports a midi file and a text file containing the     #
# names of the chords in letter notation.                               #
#                                                                       #
# ***NOTE***: modify "song_route" and "export_route" variables with     #
# custom local paths before running app                                 #
#                                                                       #
# ***Requires "constants.py" (attached in same folder)                  #
#                                                                       #
# This project includes code repurposed and reorganized from:           #
#       Yuma Mihira's Pychord repository at:                            #
#       https://github.com/yuma-m/pychord                               #
#                                                                       #
#       Colin Raffel's Pretty Midi repository at:                       #
#       https://github.com/craffel/pretty-midi                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

import random
import pretty_midi
import pychord
from pychord import Chord
from constants import constants

#song_path = 'C:\\Users\\dzava\\Downloads\\piano_ci\\chord.mid'
song_route = 'C:\\Users\\dzava\\Downloads\\piano_ci\\'
song_path = ''
song_path_end = 'chord'

#export_path = 'C:\\Users\\dzava\\Downloads\\piano_ci\\out.txt'
export_route = 'C:\\Users\\dzava\\Downloads\\piano_ci\\'
export_path = ''
export_path_end = 'out'

repetitions = 1 # number of chord sets generated (text file and midi file)
inst_group = 1 # instrument group to be used by Pretty Midi

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Get musical instrument for midi from Pretty_midi constants [RANDOM]   #
# RETURN: string with instrument name                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def get_instrument(group):
    
    # instrument family value ranges:
    if group == 1 : # piano 0-23
        a, b = 0, 23
    elif group == 2 : # string 24-51
        a, b = 24, 51
    elif group == 3 : # voice 52-54
        a, b = 52, 54
    elif group == 4 : # brass 55-63
        a, b = 55, 63
    elif group == 5 : # wood 64-79
        a, b = 64, 79
    elif group == 6 : # FX 80-103
        a, b = 80, 103
    elif group == 7 : # special 104-113
        a, b = 104, 113
    elif group == 8 : # RANDOM
        a, b = 0, 113
    else : # piano as default
        a, b = 0, 23

    instrument_name = constants.instruments[random.randint(a,b)]
    
    return instrument_name

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Generate chord series by combining chord bases (from clist) with      #
# qualities (from qlist) [RANDOM]                                       #
# RECEIVE: integer representing desired series length (# of chords)     #
# RETURN: list of strings representing the chord names                  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def get_chords(length):
    clist = constants.notes
    len_clist = len(clist)
    qlist = constants.qualities
    len_qlist = len(qlist)

    out = []
    for x in range(length):
        temp = clist[random.randint(0,len_clist-1)]
        temp = temp + qlist[random.randint(0,constants.qn)]
        out.append(temp)
    return out

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Create midi file using methods from Pretty_midi                       #
# RECEIVE: list of Pychord Chords objects                               #
# EXPORT: midi file to song_path                                        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def create_midi(chords, midi_name):
    midi_data = pretty_midi.PrettyMIDI()

    #piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')

    # get value for the instrument
    instrument_name = get_instrument(constants.inst_group)

    piano_program = pretty_midi.instrument_name_to_program(instrument_name)
    piano = pretty_midi.Instrument(program=piano_program)

    length = constants.length
    for n, chord in enumerate(chords):
        for note_name in chord.components_with_pitch(root_pitch=4):
            note_number = pretty_midi.note_name_to_number(note_name)
            note = pretty_midi.Note(velocity=constants.velocity, pitch=note_number, start=n * length, end=(n + 1) * length)
            piano.notes.append(note)
    
    midi_data.instruments.append(piano)
    midi_data.write(midi_name)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Export Python list to file, each element in its own line              #
# RECEIVE: list to export || desired location for the file generated    #
# EXPORT: text file each element in its own line                        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def export_list(out, location):
    with open(location, 'w') as f:
        for item in out:
            f.write(item)
            f.write("\n")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Gets input from user until user inputs an integer                     #
# RECEIVE: None                                                         #
# RETURN: integer                                                       #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def verify_integer():
    while True:
        num = input("Choice: ")
        try:
            intvar = int(num)
            break
        except ValueError:
            pass # input is not a number, repeat
    
    print() # aesthetics spacing
    return intvar

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Gets input from user until user inputs an integer                     #
# RECEIVE: integer, indicates the quality group                         #
# RETURN: None                                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def set_qualities(group):
    # will assign upper list limit to constants.qn:
    if group == 1 : # at least 3
        a = 10
    elif group == 2 : # at least 4
        a = 31
    elif group == 3 : # at least 5
        a = 59
    elif group == 4 : # at least 6
        a = 69
    else : # at least 6 as default
        a = 69
    
    constants.qn = a

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Interface for getting user input                                      #
# RECEIVE: None                                                         #
# RETURN: None                                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def get_input():
    # Choosing how many iterations you want
    print("How many outputs would you like? (1-100)")
    constants.repetitions = verify_integer()

    # Choosing how many chords per iteration
    print("How many chords per output would you like? (1-100)")
    constants.chordn = verify_integer()

    # Choosing range of qualities per chord
    print("How many notes per chord would you like?")
    print("(1) At least 3\n(2) At least 4\n(3) At least 5\n(4) At least 6")
    constants.qn = verify_integer()
    set_qualities(constants.qn)
    

    # Choosing an instrument
    print("Choose an instrument family:")
    print("(1) Piano\n(2) Strings\n(3) Voice\n(4) Brass")
    print("(5) Wood\n(6) FX\n(7) Special\n(8) Random\n")
    constants.inst_group = verify_integer()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Outputs info to user and exports data                                 #
# RECEIVE: name of the file (string)                                    #
# RETURN: None                                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def output(out_name):
    print(constants.chords_str)
    export_list(constants.chords_str,out_name)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Runs generating process                                               #
# RECEIVE: None                                                         #
# RETURN: None                                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def generate():
    for x in range(constants.repetitions):
        constants.chords_str = get_chords(constants.chordn) # chords_str = ["C", "Dm7", "G", "C"]

        # Turn chord string list into Chord object list
        chords = [Chord(c) for c in constants.chords_str]

        # create midi file and export it to song_path
        song_path = song_route + song_path_end + str(x) + '.mid'
        create_midi(chords,song_path)

        # export chord data for reading
        export_path = export_route + export_path_end + str(x) + '.txt'
        output(export_path)

#################### MAIN ####################

get_input()

generate()

#################### END ####################