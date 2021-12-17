import pretty_midi
import cspAlgorithms
import domainComposition
import cspConstraints
import romanNumAnalysis

class MidiComposer:
    "MIDI Composer containing functions to add scores to a MIDI file, then export"

    def __init__(self, file_path, key):
        self.file_path = file_path
        self.midi = pretty_midi.PrettyMIDI(self.file_path)
        self.key = key
        self.csp_solver = cspAlgorithms.CSPSolver()
        self.constraint_generator = cspConstraints.ConstraintGenerator(self.midi)
        self.harmonizer = romanNumAnalysis.Harmonizer(self.file_path, self.key)

    def add_toms(self):
        # get the CSP for the toms score
        csp_toms = self.constraint_generator.get_toms_csp()

        # get the toms score by solving the above CSP
        toms_score = self.csp_solver.solve(csp_toms)

        # compose the toms score onto the midi file given the found solution
        domainComposition.domain_to_notes('toms', toms_score, self.midi)

    def add_snare(self):
        # get the CSP for the snare score
        csp_snare = self.constraint_generator.get_snare_csp()

        # get the snare score by solving the above CSP
        snare_score = self.csp_solver.solve(csp_snare)

        # compose the snare score onto the midi file given the found solution
        domainComposition.domain_to_notes('snare', snare_score, self.midi)

    def add_kick(self):
        # get the CSP for the kick score
        csp_kick = self.constraint_generator.get_kick_csp()

        # get the kick score by solving the above CSP
        kick_score = self.csp_solver.solve(csp_kick)

        # compose the kick score onto the midi file given the found solution
        domainComposition.domain_to_notes('kick', kick_score, self.midi)

    def add_cyms(self):
        # get the CSP for the cymbals score
        csp_cyms = self.constraint_generator.get_cymbals_csp()

        # get the cymbals score by solving the above CSP
        cyms_score = self.csp_solver.solve(csp_cyms)

        # compose the cymbals score onto the midi file given the found solution
        domainComposition.domain_to_notes('hi hat', cyms_score, self.midi)

    def add_harmony(self):
        self.harmonizer.generate_chords()

        self.file_path = 'song_with_chords.mid'

        self.midi = pretty_midi.PrettyMIDI(self.file_path)

        self.constraint_generator = cspConstraints.ConstraintGenerator(self.midi)

    def export(self):
        self.midi.write('out.mid')

    def compose(self, addHarmony, addToms, addSnare, addKick, addCyms):
        if addHarmony:
            self.add_harmony()
        
        if addToms:
            self.add_toms()
        
        if addSnare:
            self.add_snare()

        if addKick:
            self.add_kick()

        if addCyms:
            self.add_cyms()

        self.export()