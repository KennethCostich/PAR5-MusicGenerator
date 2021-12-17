import pretty_midi

snare = 38
kick = 35
hi_hat = 42
tom = 47

def domain_to_notes(instrument, beats, midi):
    if instrument == 'kick':
        pitch = kick
    elif instrument == 'tom':
        pitch = tom
    elif instrument == 'snare':
        pitch = snare
    elif instrument == 'hi hat':
        pitch = hi_hat
    else:
        pitch = kick
    
    score = midi
    percussionInst = pretty_midi.Instrument(program=pitch, is_drum=True, name=instrument)
    score.instruments.append(percussionInst)

    thisTempo = score.estimate_tempo()

    beatLengthInSec = 60 / (thisTempo)
    sorted_keys = list(beats.keys())
    sorted_keys.sort()

    beatInterval = sorted_keys[1] - sorted_keys[0]

    for beat in beats:
        note = beats[beat]
        if note == 'quarterNote':
            percussionInst.notes.append(pretty_midi.Note(100, pitch, beat, (beat + beatInterval)))
        elif note == 'twoEigthNotes':
            percussionInst.notes.append(pretty_midi.Note(100, pitch, beat, (beat + (beatInterval/2))))
            percussionInst.notes.append(pretty_midi.Note(100, pitch, (beat + (beatInterval/2)), (beat + beatInterval)))
        elif note == 'eigthNoteRest':
            percussionInst.notes.append(pretty_midi.Note(100, pitch, beat, (beat + (beatInterval/2))))
        elif note == 'restEigthNote':
            percussionInst.notes.append(pretty_midi.Note(100, pitch, (beat + (beatInterval/2)), (beat + beatInterval)))



