from modules.common.set import *
from modules.common.state import *
import graphviz as gv

class Automata():
    def __init__(this, states, final, symbols, initial, transitions = []):
        if (
            not isinstance(states, Set) 
            or not isinstance(final, Set) 
            or not isinstance(symbols, Set) 
            or not isinstance(initial, State) 
            ): raise TypeError("Automata: states, final, symbols, initial and transitions must be of type Set and State respectively")

        this.states = states
        this.final = final
        this.symbols = symbols
        this.initial = initial
        this.transitions = transitions

    def transition(this, state, symbol):
        # TODO check implementation
        return [t.target for t in this.transitions if t.source == state and t.symbol == symbol]

    def createImage():
        # TODO
        pass