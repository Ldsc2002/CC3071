from modules.proto.automata import *

class NFA(Automata):
    def __init__(this, states, final, symbols, initial, transitions = []):
        super().__init__(states, final, symbols, initial, transitions)

    def subsetConstruction(this):
        # TODO implement subset construction
        pass