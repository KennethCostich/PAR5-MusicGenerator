import music21 as msc
import re
import copy

class Harmonizer:
    "Contains data about keys and functions to add harmonies to MIDI files"

    def __init__(self, file_path, key):
        # Store the file path of the MIDI file
        self.midi = file_path

        # Store the key of the song in the MIDI file
        self.key = key

        # Create a dictionary of keys and their relevant data
        self.degree_in_key = {
            'C': {
                'C': '1',
                'D': '2',
                'Eb': 'b3',
                'E': '3',
                'F': '4',
                'G': '5',
                'Ab': '#5',
                'A': '6',
                'Bb': '7',
                'B': 'maj7'
            },

            'G': {
                'G': '1',
                'A': '2',
                'Bb': 'b3',
                'B': '3',
                'C': '4',
                'D': '5',
                'Eb': '#5',
                'E': '6',
                'F': '7',
                'Gb': 'maj7'
            },

            'D': {
                'D': '1',
                'E': '2',
                'F': 'b3',
                'Gb': '3',
                'G': '4',
                'A': '5',
                'Bb': '#5',
                'B': '6',
                'C': '7',
                'Db': 'maj7'
            },

            'A': {
                'A': '1',
                'B': '2',
                'C': 'b3',
                'Db': '3',
                'D': '4',
                'E': '5',
                'F': '#5',
                'Gb': '6',
                'G': '7',
                'Ab': 'maj7'
            },

            'E': {
                'E': '1',
                'Gb': '2',
                'G': 'b3',
                'Ab': '3',
                'A': '4',
                'B': '5',
                'C': '#5',
                'Db': '6',
                'D': '7',
                'Eb': 'maj7'
            },

            'B': {
                'B': '1',
                'Db': '2',
                'D': 'b3',
                'Eb': '3',
                'E': '4',
                'Gb': '5',
                'G': '#5',
                'Ab': '6',
                'A': '7',
                'Bb': 'maj7'
            },

            'Gb': {
                'Gb': '1',
                'Ab': '2',
                'A': 'b3',
                'Bb': '3',
                'B': '4',
                'Db': '5',
                'D': '#5',
                'Eb': '6',
                'E': '7',
                'F': 'maj7'
            },

            'Db': {
                'Db': '1',
                'Eb': '2',
                'E': 'b3',
                'F': '3',
                'Gb': '4',
                'Ab': '5',
                'A': '#5',
                'Bb': '6',
                'B': '7',
                'C': 'maj7'
            },

            'Ab': {
                'Ab': '1',
                'Bb': '2',
                'B': 'b3',
                'C': '3',
                'Db': '4',
                'Eb': '5',
                'E': '#5',
                'F': '6',
                'Gb': '7',
                'G': 'maj7'
            },

            'Eb': {
                'Eb': '1',
                'F': '2',
                'Gb': 'b3',
                'G': '3',
                'Ab': '4',
                'Bb': '5',
                'B': '#5',
                'C': '6',
                'Db': '7',
                'D': 'maj7'
            },

            'Bb': {
                'Bb': '1',
                'C': '2',
                'Db': 'b3',
                'D': '3',
                'Eb': '4',
                'F': '5',
                'Gb': '#5',
                'G': '6',
                'Ab': '7',
                'A': 'maj7'
            },

            'F': {
                'F': '1',
                'G': '2',
                'Ab': 'b3',
                'A': '3',
                'Bb': '4',
                'C': '5',
                'Db': '#5',
                'D': '6',
                'Eb': '7',
                'E': 'maj7'
            },

            'Am': {
                'C': '3',
                'D': '4',
                'Eb': 'b5',
                'E': '5',
                'F': '6',
                'G': '7',
                'Ab': 'maj7',
                'A': '1',
                'Bb': 'b2',
                'B': '2'
            },

            'Em': {
                'G': '3',
                'A': '4',
                'Bb': 'b5',
                'B': '5',
                'C': '6',
                'D': '7',
                'Eb': 'maj7',
                'E': '1',
                'F': 'b2',
                'Gb': '2'
            },

            'Bm': {
                'D': '3',
                'E': '4',
                'F': 'b5',
                'Gb': '5',
                'G': '6',
                'A': '7',
                'Bb': 'maj7',
                'B': '1',
                'C': 'b2',
                'Db': '2'
            },

            'Gbm': {
                'A': '3',
                'B': '4',
                'C': 'b5',
                'Db': '5',
                'D': '6',
                'E': '7',
                'F': 'maj7',
                'Gb': '1',
                'G': 'b2',
                'Ab': '2'
            },

            'Dbm': {
                'E': '3',
                'Gb': '4',
                'G': 'b5',
                'Ab': '5',
                'A': '6',
                'B': '7',
                'C': 'maj7',
                'Db': '1',
                'D': 'b2',
                'Eb': '2'
            },

            'Abm': {
                'B': '3',
                'Db': '4',
                'D': 'b5',
                'Eb': '5',
                'E': '6',
                'Gb': '7',
                'G': 'maj7',
                'Ab': '1',
                'A': 'b2',
                'Bb': '2'
            },

            'Ebm': {
                'Gb': '3',
                'Ab': '4',
                'A': 'b5',
                'Bb': '5',
                'B': '6',
                'Db': '7',
                'D': 'maj7',
                'Eb': '1',
                'E': 'b2',
                'F': '2'
            },

            'Bbm': {
                'Db': '3',
                'Eb': '4',
                'E': 'b5',
                'F': '5',
                'Gb': '6',
                'Ab': '7',
                'A': 'maj7',
                'Bb': '1',
                'B': 'b2',
                'C': '2'
            },

            'Fm': {
                'Ab': '3',
                'Bb': '4',
                'B': 'b5',
                'C': '5',
                'Db': '6',
                'Eb': '7',
                'E': 'maj7',
                'F': '1',
                'Gb': 'b2',
                'G': '2'
            },

            'Cm': {
                'Eb': '3',
                'F': '4',
                'Gb': 'b5',
                'G': '5',
                'Ab': '6',
                'Bb': '7',
                'B': 'maj7',
                'C': '1',
                'Db': 'b2',
                'D': '2'
            },

            'Gm': {
                'Bb': '3',
                'C': '4',
                'Db': 'b5',
                'D': '5',
                'Eb': '6',
                'F': '7',
                'Gb': 'maj7',
                'G': '1',
                'Ab': 'b2',
                'A': '2'
            },

            'Dm': {
                'F': '3',
                'G': '4',
                'Ab': 'b5',
                'A': '5',
                'Bb': '6',
                'C': '7',
                'Db': 'maj7',
                'D': '1',
                'Eb': 'b2',
                'E': '2'
            }
        }


    def normalize(self, dic):
        new_dic = {}

        divisor = 0
        for k in dic:
            divisor += dic[k]

        if divisor > 0:
            for k in dic:
                new_dic[k] = dic[k] / divisor

        return new_dic


    def convert_note(self, note):
        """
        Given a note, converts it to it's equivalent note.
        """
        if note == 'A-' or note == 'G#':
            return 'Ab'
        elif note == 'B-' or note == 'A#':
            return 'Bb'
        elif note == 'C-' or note == 'B#':
            return 'B'
        elif note == 'D-' or note == 'C#':
            return 'Db'
        elif note == 'E-' or note == 'D#':
            return 'Eb'
        elif note == 'F-':
            return 'E'
        elif note == 'E#':
            return 'F'
        elif note == 'G-' or note == 'F#':
            return 'Gb'
        else:
            return note


    def detect_chord(self, notes):
        """
        Detects what chord is given by a list of notes.
        """
        minor = False

        if self.key[-1] == 'm':
            minor = True

        if not minor:

            chords = {
                'I': 0,
                'I7': 0,
                'Imaj7': 0,
                'ii': 0,
                'ii7': 0,
                'iii': 0,
                'iii7': 0,
                'III': 0,
                'III7': 0,
                'IV': 0,
                'IV7': 0,
                'IVmaj7': 0,
                'iv': 0,
                'iv7': 0,
                'V': 0,
                'V7': 0,
                'vi': 0,
                'vi7': 0,
                'vii': 0
            }

            for note in notes:

                try:
                    degree = self.degree_in_key[self.key][note]
                except KeyError:
                    degree = ''

                if degree == '1':
                    chords['I'] += 1
                    chords['I7'] += 1
                    chords['Imaj7'] += 1
                    chords['ii7'] += 2
                    chords['IV'] += 1
                    chords['IV7'] += 1
                    chords['IVmaj7'] += 1
                    chords['iv'] += 1
                    chords['iv7'] += 1
                    chords['vi'] += 1
                    chords['vi7'] += 1

                elif degree == '2':
                    chords['ii'] += 1
                    chords['ii7'] += 1
                    chords['iii7'] += 2
                    chords['III7'] += 2
                    chords['V'] += 1
                    chords['V7'] += 1
                    chords['vii'] += 1

                elif degree == 'b3':
                    chords['iv7'] += 2
                    chords['IV7'] += 2

                elif degree == '3':
                    chords['I'] += 2
                    chords['I7'] += 2
                    chords['Imaj7'] += 2
                    chords['iii'] += 1
                    chords['iii7'] += 1
                    chords['III'] += 1
                    chords['III7'] += 1
                    chords['IVmaj7'] += 2
                    chords['vi'] += 1
                    chords['vi7'] += 1

                elif degree == '4':
                    chords['ii'] += 1
                    chords['ii7'] += 1
                    chords['IV'] += 1
                    chords['IV7'] += 1
                    chords['IVmaj7'] += 1
                    chords['iv'] += 1
                    chords['iv7'] += 1
                    chords['vii'] += 1
                    chords['V7'] += 2

                elif degree == '5':
                    chords['I'] += 1
                    chords['I7'] += 1
                    chords['Imaj7'] += 1
                    chords['iii'] += 1
                    chords['iii7'] += 1
                    chords['V'] += 1
                    chords['V7'] += 1
                    chords['vi7'] += 2

                elif degree == '#5':
                    chords['III'] += 2
                    chords['III7'] += 2
                    chords['iv'] += 2
                    chords['iv7'] += 2

                elif degree == '6':
                    chords['ii'] += 1
                    chords['ii7'] += 1
                    chords['IV'] += 1
                    chords['IV7'] += 1
                    chords['IVmaj7'] += 1
                    chords['vi'] += 1
                    chords['vi7'] += 1

                elif degree == '7':
                    chords['I7'] += 2

                elif degree == 'maj7':
                    chords['Imaj7'] += 2
                    chords['iii'] += 1
                    chords['iii7'] += 1
                    chords['III'] += 1
                    chords['III7'] += 1
                    chords['V'] += 1
                    chords['V7'] += 1
                    chords['vii'] += 1

        else:
            chords = {
                'III': 0,
                'III7': 0,
                'IIImaj7': 0,
                'iv': 0,
                'iv7': 0,
                'v': 0,
                'v7': 0,
                'V': 0,
                'V7': 0,
                'VI': 0,
                'VI7': 0,
                'VImaj7': 0,
                'vi': 0,
                'vi7': 0,
                'VII': 0,
                'VII7': 0,
                'i': 0,
                'i7': 0,
                'ii': 0
            }

            for note in notes:
                try:
                    degree = self.degree_in_key[self.key][note]
                except KeyError:
                    degree = ''

                if degree == '1':
                    chords['i'] += 1
                    chords['i7'] += 1
                    chords['VI'] += 1
                    chords['VI7'] += 1
                    chords['VImaj7'] += 1
                    chords['iv'] += 1
                    chords['iv7'] += 1

                elif degree == 'b2':
                    chords['III7'] += 2

                elif degree == '2':
                    chords['IIImaj7'] += 2
                    chords['v'] += 1
                    chords['v7'] += 1
                    chords['V'] += 1
                    chords['V7'] += 1
                    chords['VII'] += 1
                    chords['VII7'] += 1
                    chords['ii'] += 1

                elif degree == '3':
                    chords['III'] += 1
                    chords['III7'] += 1
                    chords['IIImaj7'] += 1
                    chords['iv7'] += 2
                    chords['VI'] += 1
                    chords['VI7'] += 1
                    chords['VImaj7'] += 1
                    chords['vi'] += 1
                    chords['vi7'] += 1
                    chords['i'] += 1
                    chords['i7'] += 1

                elif degree == '4':
                    chords['iv'] += 1
                    chords['iv7'] += 1
                    chords['v7'] += 2
                    chords['V7'] += 2
                    chords['VII'] += 1
                    chords['VII7'] += 1
                    chords['ii'] += 1

                elif degree == 'b5':
                    chords['vi7'] += 2
                    chords['VI7'] += 2

                elif degree == '5':
                    chords['III'] += 2
                    chords['III7'] += 2
                    chords['IIImaj7'] += 2
                    chords['v'] += 1
                    chords['v7'] += 1
                    chords['V'] += 1
                    chords['V7'] += 1
                    chords['VImaj7'] += 2
                    chords['i'] += 1
                    chords['i7'] += 1

                elif degree == '6':
                    chords['iv'] += 1
                    chords['iv7'] += 1
                    chords['VI'] += 1
                    chords['VI7'] += 1
                    chords['VImaj7'] += 1
                    chords['vi'] += 1
                    chords['vi7'] += 1
                    chords['ii'] += 1
                    chords['VII7'] += 2

                elif degree == '7':
                    chords['III'] += 1
                    chords['III7'] += 1
                    chords['IIImaj7'] += 1
                    chords['v'] += 1
                    chords['v7'] += 1
                    chords['VII'] += 1
                    chords['VII7'] += 1
                    chords['i7'] += 2

                elif degree == 'maj7':
                    chords['V'] += 2
                    chords['V7'] += 2
                    chords['vi'] += 2
                    chords['vi7'] += 2

        return max(chords, key=chords.get)


    def generate_chords(self):
        """
        Generates and writes harmonic chords to the MIDI file.
        """
        c = msc.converter.parse(self.midi)
        c.getElementsByClass(msc.stream.Part)[0].append(msc.stream.Measure())
        chords_in_measure = []

        for i in range(1, 9):
            notes = []
            for note in c.measure(i).pitches:
                notes.append(self.convert_note(re.sub(r'[0-9]+', '', str(note))))

            correct = self.detect_chord(notes)
            new_key = self.key
            if self.key[-1] == 'm':
                new_key = self.key.lower()
            if len(self.key) > 1 and self.key[1] == 'b':
                new_key = new_key[0] + '-'

            rn = msc.roman.RomanNumeral(correct, keyOrScale=new_key)
            for i in range(len(rn.pitches)):
                rn.pitches[i].octave = 4

            chords_in_measure.append(rn)

        piano = msc.stream.Part(id='piano')
        bass = msc.stream.Part(id='bass')

        piano.insert(0, msc.instrument.Piano())
        bass.insert(0, msc.instrument.ElectricBass())

        piano_measures = []
        bass_measures = []

        for i in range(1, 9):
            chord = copy.copy(chords_in_measure[i - 1])
            note = msc.note.Note(str(chords_in_measure[i - 1].root()))
            chord.duration.quarterLength = 4.0
            note.duration.quarterLength = 4.0
            note.octave = 1
            bass_measures.append(msc.stream.Measure(number=i))
            bass_measures[i-1].insertIntoNoteOrChord(0.0, note)
            piano_measures.append(msc.stream.Measure(number=i))
            piano_measures[i-1].insertIntoNoteOrChord(0.0, chord)

        piano.append(piano_measures)
        bass.append(bass_measures)
        c.insert(0, piano)
        c.insert(0, bass)
        c.write('midi', fp='song_with_chords.mid')
