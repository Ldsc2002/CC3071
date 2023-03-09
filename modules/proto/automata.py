from modules.common.set import *
from modules.common.state import *
from modules.common.transition import *
from modules.common.node import *
from modules.common.set import *

from graphviz import Digraph

class Automata():
    def __init__(this, initial = State(), states = Set(), final = Set(), symbols = Set(), transitions = Set()):
        if (
            not isinstance(states, Set) 
            or not isinstance(final, Set) 
            or not isinstance(symbols, Set) 
            or not isinstance(transitions, Set)
            or not isinstance(initial, State) 
            ): raise TypeError("Automata: states, final, symbols, initial and transitions must be of type Set and State respectively")

        this.filename = "Automata_"
        this.states = states
        this.final = final
        this.symbols = symbols
        this.initial = initial
        this.transitions = transitions

    def createImage(this):
        g = Digraph('AFN', filename=("out/" + this.filename), format='png')
        g.attr(rankdir='LR')

        for state in this.states:
            if state in this.final:
                g.node(str(state.id), label=str(state.id), shape='doublecircle')

                if state == this.initial:
                    g.node("", shape='none', width='0', height='0')
                    g.edge("", str(state.id))
            else:
                if state == this.initial:
                    g.node("", shape='none', width='0', height='0')
                    g.edge("", str(state.id))
                    
                g.node(str(state.id), label=str(state.id), shape='circle')

        for transition in this.transitions:
            g.edge(str(transition.source.id), str(transition.target.id), label=transition.symbol.cid)

        g.view()

    def simulate(this, word):
        def eClosure(state, past = None):
            if past == None:
                past = []

            if state.id in past:
                return Set()
                
            past.append(state.id)
            closure = Set()
            closure.add(state.id)

            for transition in this.transitions:
                if transition.source.id == state.id and transition.symbol.id == "ε":
                    closure.union(eClosure(transition.target, past))

            return closure
        
        current = eClosure(this.initial)
        for symbol in word:
            for transition in this.transitions:
                if transition.source.id in current and transition.symbol.id == symbol:
                    current = eClosure(transition.target)
                    break

        inFinal = False
        for state in this.final:
            if state.id in current:
                inFinal = True
                break    

        if inFinal:
            print("\nThe word '" + word + "' is accepted by the automata " + this.filename)
        else:
            print("\nThe word '" + word + "' is not accepted by the automata " + this.filename)

    def print(this):
        states = Set()
        for state in this.states:
            states.add(state.id)

        print("\nStates: ", states)
        print("Initial: ", this.initial)
        print("Final: ", this.final)
        print("Symbols: ", this.symbols)
        print("Transitions: ", this.transitions)