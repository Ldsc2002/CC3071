from modules.common.set import *
from modules.common.state import *
from modules.common.transition import *
from modules.common.node import *
from modules.common.set import *

import graphviz as gv

class Automata():
    def __init__(this, initial, states = Set(), final = Set(), symbols = Set(), transitions = Set()):
        if (
            not isinstance(states, Set) 
            or not isinstance(final, Set) 
            or not isinstance(symbols, Set) 
            or not isinstance(transitions, Set)
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

    def createImage(this):
        from graphviz import Digraph

        g = Digraph('AFN', filename= 'out/Automata', format='png')

        for state in this.states:
            if state in this.final:
                g.node(str(state.id), label=str(state.id), shape='doublecircle')
            else:
                g.node(str(state.id), label=str(state.id), shape='circle')

        for transition in this.transitions:
            g.edge(str(transition.source.id), str(transition.target.id), label=transition.symbol.cid)

        g.view()