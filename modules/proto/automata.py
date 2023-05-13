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
        this.shape = "circle"

    def createImage(this):
        g = Digraph('AFN', filename=("out/" + this.filename), format='png')
        g.attr(rankdir='LR')

        for state in this.states:
            if isinstance(state.id, list):
                nodeText = ""
                for s in state.id:
                    nodeText += str(s) + "\n"
                nodeText = nodeText.strip()
            else:
                nodeText = str(state.id)

            if state in this.final:
                if this.shape == "circle":
                    g.node(nodeText, label=nodeText, shape='doublecircle')
                else:
                    g.node(nodeText, label=nodeText, shape=this.shape, color='green')

                if state == this.initial:
                    g.node("", shape='none', width='0', height='0')
                    g.edge("", nodeText)
            else:
                if state == this.initial:
                    g.node("", shape='none', width='0', height='0')
                    g.edge("", nodeText)
                    
                g.node(nodeText, label=nodeText, shape=this.shape)

        for transition in this.transitions:
            if isinstance(transition.source.id, list):
                sourceID = ""
                for s in transition.source.id:
                    sourceID += str(s) + "\n"
                sourceID = sourceID.strip()
            else:
                sourceID = str(transition.source.id)

            if isinstance(transition.target.id, list):
                targetID = ""
                for s in transition.target.id:
                    targetID += str(s) + "\n"
                targetID = targetID.strip()
            else:
                targetID = str(transition.target.id)

            g.edge(sourceID, targetID, label=transition.symbol.cid)

        g.view()

    def simulate(this, word, printResult = True):
        def eClosure(state):
            stack = [state]
            closure = Set()
            visited = Set()
            closure.add(state.id)

            while len(stack) > 0:
                state = stack.pop()
                
                for transition in this.transitions:
                    if transition.source.id == state.id and transition.symbol.cid == "ε":
                        if transition.target.id not in visited:
                            visited.add(transition.target.id)
                            stack.append(transition.target)
 
                        closure.add(transition.target.id)

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

        if printResult:
            if inFinal:
                print("\nThe word '" + word + "' is accepted by the automata " + this.filename)
            else:
                print("\nThe word '" + word + "' is not accepted by the automata " + this.filename)

        return inFinal

    def print(this):
        if "NFA" in this.filename:
            print("\nNFA: ")
        elif "minDFA" in this.filename:
            if "Direct" in this.filename:
                print("\nDirect Minimized DFA: ")
            elif "Subset" in this.filename:
                print("\nSubset Minimized DFA: ")
        elif "DFA" in this.filename:
            if "Direct" in this.filename:
                print("\nDirect DFA: ")
            elif "Subset" in this.filename:
                print("\nSubset DFA: ")
        elif "Yapar" in this.filename:
            print("\nYapar: ")

        states = Set()
        for state in this.states:
            states.add(state.id)

        print("States: ", states)
        print("Initial: ", this.initial)
        print("Final: ", this.final)
        print("Symbols: ", this.symbols)
        print("Transitions: ", this.transitions)