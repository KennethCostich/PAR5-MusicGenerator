from music21 import *
import pretty_midi

# Load MIDI file 9.mid into PrettyMIDI object
midi9 = pretty_midi.PrettyMIDI('/Users/kennethcostichiii/Desktop/Classes/Fall 2021/Artificial Intelligence/Final Project/code/data/9.mid')

# Get the downbeats of midi9
downbeats9 = midi9.get_downbeats()

# Print downbeats
print("9.mid Downbeats:")
print(downbeats9) 

# Get the beats of midi9
beats9 = midi9.get_beats(start_time=0.0)

# Print beats
print("9.mid Beats:")
print(beats9) 

# Load MIDI file "Kiss Me - Sixpence None The Richer.mid" into PrettyMIDI object
kissMe_sixpence = pretty_midi.PrettyMIDI('/Users/kennethcostichiii/Desktop/Classes/Fall 2021/Artificial Intelligence/Final Project/code/data/Kiss Me - Sixpence None The Richer.mid')

# Get the downbeats of kissMe_sixpence
downbeats_kissMe = kissMe_sixpence.get_downbeats()

# Print downbeats
print("Kiss Me Downbeats:")
print(downbeats_kissMe) 

kissMe_21 = converter.parse('/Users/kennethcostichiii/Desktop/Classes/Fall 2021/Artificial Intelligence/Final Project/code/data/Kiss Me - Sixpence None The Richer.mid')
kissMe_21.show()
k = kissMe_21
k.write('midi', fp='song_with_chords.mid')

# music21 stuff
#midi9_21 = converter.parse('/Users/kennethcostichiii/Desktop/Classes/Fall 2021/Artificial Intelligence/Final Project/code/data/9.mid')
#midi9_21.show()