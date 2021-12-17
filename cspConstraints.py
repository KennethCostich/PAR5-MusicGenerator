import pretty_midi
import copy
import cspAlgorithms
import domainComposition

class ConstraintGenerator:
    "Contains functions to generate beat constraints for a MIDI file"

    def __init__(self, midi):
        self.midi = midi

        # Get the beats of midi
        self.beats_list = midi.get_beats(start_time=0.0)

        # convert to set
        self.beats = set(self.beats_list)

        # Get the downbeats of midi
        self.downbeats_list = self.midi.get_downbeats()

        # convert to set
        self.downbeats = set(self.downbeats_list)

        # initialize domains for each instrument to be added
        self.snare_beats_domain = {}
        self.kick_beats_domain = {}
        self.cymbal_beats_domain = {}
        self.toms_beats_domain = {}

        # create a list of sorted keys
        self.sorted_keys = list(self.beats)
        self.sorted_keys.sort()

    def get_snare_csp(self):
        """
        Constructs a CSP as a triple for the snare score.
        """
        # initialize the domain for every variable
        for k in self.beats:
            self.snare_beats_domain[k] = ['quarterNote', 'twoEigthNotes', 'eigthNoteRest', 'restEigthNote', 'rest']

        # directly enforce unary constraints on the variable domains
        for beat in self.snare_beats_domain:
            if beat in self.downbeats:
                self.snare_beats_domain[beat] = ['quarterNote', 'rest']
            else:
                self.snare_beats_domain[beat] = ['eigthNoteRest', 'restEigthNote', 'rest']

        # initialize a dictionary of binary constraints ("arc" constraints) for the snare score
        snare_binary_constraints = {}
        start = True
        after_start = True
        before_last = False
        last = False

        # populate snare binary constraints
        for i in range(len(list(self.snare_beats_domain.keys()))):
            beat1 = self.sorted_keys[i]
            if not start:
                snare_binary_constraints[(beat1, self.sorted_keys[i - 1])] = (lambda a, b: a != b)
                if not after_start:
                    snare_binary_constraints[(beat1, self.sorted_keys[i - 2])] = (lambda a, b: a == b)
            if not last:
                snare_binary_constraints[(beat1, self.sorted_keys[i + 1])] = (lambda a, b: a != b)
                if not before_last:
                    snare_binary_constraints[(beat1, self.sorted_keys[i + 2])] = (lambda a, b: a == b)
            
            start = False
            if i == 1:
                after_start = False
            if i + 3 == len(list(self.snare_beats_domain.keys())):
                before_last = True
            elif i + 2 == len(list(self.snare_beats_domain.keys())):
                last = True

        # get the variables for the snare CSP
        snare_vars = self.beats

        # get the domains for the snare CSP
        snare_domain_copy = copy.deepcopy(self.snare_beats_domain)

        # get the constraints to be enforced for the snare CSP
        snare_constraints = snare_binary_constraints

        # construct the snare CSP as a triple
        csp_snare = (snare_vars, snare_domain_copy, snare_constraints)

        # return the snare CSP
        return csp_snare

    def get_toms_csp(self):
        """
        Constructs a CSP as a triple for the toms score.
        """
        # initialize the domain for every variable
        for k in self.beats:
            self.toms_beats_domain[k] = ['quarterNote', 'twoEigthNotes', 'eigthNoteRest', 'restEigthNote', 'rest']
        
        # directly enforce unary constraints on the variable domains
        for beat in self.toms_beats_domain:
            if beat in self.downbeats:
                self.toms_beats_domain[beat] = ['quarterNote', 'rest']
            else:
                self.toms_beats_domain[beat] = ['twoEigthNotes', 'eigthNoteRest', 'restEigthNote']
        
        # initialize a dictionary of binary constraints ("arc" constraints) for the toms score
        toms_binary_constraints = {}
        start = True
        last = False

        # populate toms binary constraints
        for i in range(len(list(self.toms_beats_domain.keys()))):
            beat1 = self.sorted_keys[i]
            if not start:
                toms_binary_constraints[(beat1, self.sorted_keys[i - 1])] = (lambda a, b: a != b)
            if not last:
                toms_binary_constraints[(beat1, self.sorted_keys[i + 1])] = (lambda a, b: a != b)
            start = False
            if i + 2 == len(list(self.toms_beats_domain.keys())):
                last = True

        # get the variables for the toms CSP
        toms_vars = self.beats

        # get the domains for the toms CSP
        toms_domain_copy = copy.deepcopy(self.toms_beats_domain)

        # get the constraints to be enforced for the toms CSP
        toms_constraints = toms_binary_constraints

        # construct the toms CSP as a triple
        csp_toms = (toms_vars, toms_domain_copy, toms_constraints)

        # return the toms CSP
        return csp_toms

    def get_kick_csp(self):
        """
        Constructs a CSP as a triple for the kick score.
        """
        # initialize the domain for every variable
        for k in self.beats:
            self.kick_beats_domain[k] = ['quarterNote', 'twoEigthNotes', 'eigthNoteRest', 'restEigthNote', 'rest']

        # directly enforce unary constraints on the variable domains
        for beat in self.kick_beats_domain:
            if beat in self.downbeats:
                self.kick_beats_domain[beat].remove('twoEigthNotes')
                self.kick_beats_domain[beat].remove('eigthNoteRest')
                self.kick_beats_domain[beat].remove('rest')
                self.kick_beats_domain[beat].remove('restEigthNote')
        
        # initialize a dictionary of binary constraints ("arc" constraints) for the kick score
        # for the kick, this will remain EMPTY
        kick_binary_constraints = {}

        # get the variables for the kick CSP
        kick_vars = self.beats

        # get the domains for the kick CSP
        kick_domain_copy = copy.deepcopy(self.kick_beats_domain)

        # get the constraints to be enforced for the kick CSP
        kick_constraints = kick_binary_constraints

        # construct the kick CSP as a triple
        csp_kick = (kick_vars, kick_domain_copy, kick_constraints)

        # return the kick CSP
        return csp_kick
    
    def get_cymbals_csp(self):
        """
        Constructs a CSP as a triple for the cymbals score.
        """
        # initialize the domain for every variable
        for k in self.beats:
            self.cymbal_beats_domain[k] = ['quarterNote', 'twoEigthNotes', 'eigthNoteRest', 'restEigthNote', 'rest']

        # directly enforce unary constraints on the variable domains
        for beat in self.cymbal_beats_domain:
            if beat in self.downbeats:
                self.cymbal_beats_domain[beat].remove('rest')
                self.cymbal_beats_domain[beat].remove('restEigthNote')

        # initialize a dictionary of binary constraints ("arc" constraints) for the cymbal score
        cymbal_binary_constraints = {}
        start = True
        last = False

        # populate cymbal binary constraints
        for i in range(len(self.sorted_keys)):
            beat1 = self.sorted_keys[i]
            if not start:
                cymbal_binary_constraints[(beat1, self.sorted_keys[i - 1])] = (lambda a, b: a == b)
            if not last:
                cymbal_binary_constraints[(beat1, self.sorted_keys[i + 1])] = (lambda a, b: a == b)
            start = False
            if i + 2 == len(list(self.cymbal_beats_domain.keys())):
                last = True

        # get the variables for the cymbals CSP
        cym_vars = self.beats

        # get the domains for the cymbals CSP
        cym_domain_copy = copy.deepcopy(self.cymbal_beats_domain)

        # get the constraints to be enforced for the cymbals CSP
        cym_constraints = cymbal_binary_constraints

        # construct the cymbals CSP as a triple
        csp_cymbals = (cym_vars, cym_domain_copy, cym_constraints)

        # return the cymbals CSP
        return csp_cymbals

    
