from modules.proto.automata import *
from modules.components.NFA import *
from modules.components.regexTree import *

class DFA(Automata):
    def __init__(this, regex):
        super().__init__()

        if isinstance(regex, RegexTree):
            this.directConstruction(regex)

        elif isinstance(regex, NFA):
            this.subsetConstruction()
            
        else:
            raise Exception('Invalid parameter for DFA constructor')


    def directConstruction(this, tree):
        pass

    def subsetConstruction(this):
        this.symbols = this.symbols
        
        if "ε" in this.symbols:
            this.symbols.remove("ε")

        subsets = {}
        skips = []

        for state in this.states:
            if state.id in skips:
                continue

            initial = this.eClosure(state)
            initial.sort()

            initialKey = ""
            for i in initial:
                initialKey += i

            subsets[initialKey] = {}
            for symbol in this.symbols:
                subsets[initialKey][symbol] = ""

            for testState in initial:
                for transition in this.transitions:
                    if transition.source.id == testState and transition.symbol.id != "ε":
                        possibleDest = this.eClosure(transition.target)
                        possibleDest.sort()
                        
                        possibleDestKey = ""
                        for i in possibleDest:
                            possibleDestKey += i
                        
                        subsets[initialKey][transition.symbol.id] = possibleDestKey

            for state in initial:
                if state not in skips:
                    skips.append(state)

        newStates = {}
        stateKeys = {}

        this.transitions = Set()
        this.states = Set()
        finals = Set()

        for x in range(len(subsets)):
            newStates[x] = subsets[list(subsets.keys())[x]]
            stateKeys[list(subsets.keys())[x]] = x

            arrayTest = list(subsets.keys())[x]

            for state in arrayTest:
                for final in this.final:
                    if state == final.id:
                        finals.add(x)
                        break

        for subset in newStates:
            for symbol in newStates[subset]:
                if newStates[subset][symbol] != "":
                    newStates[subset][symbol] = stateKeys[newStates[subset][symbol]]
        
        this.final = Set()
        for subset in newStates:
            state = State(subset)
            this.states.add(state)

            if subset == 0:
                this.initial = state

            if subset in finals:
                this.final.add(state)

            for symbol in newStates[subset]:
                if newStates[subset][symbol] != "":
                    this.transitions.add(Transition(State(subset), State(newStates[subset][symbol]), Symbol(symbol)))
        
    def eClosure(this, state):
        closure = Set()
        closure.add(state.id)

        for transition in this.transitions:
            if transition.source == state and transition.symbol.id == "ε":
                closure.union(this.eClosure(transition.target))

        return closure
