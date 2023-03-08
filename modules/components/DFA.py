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

        for state in this.states:
            initial = this.eClosure(state)
            initial.sort()
                        
            initial, exists = this.setExists(initial, subsets)

            if not exists:
                subsets[initial] = {}
                for symbol in this.symbols:
                    subsets[initial][symbol] = Set()

            for testState in initial:
                for transition in this.transitions:
                    if transition.source.id == testState and transition.symbol.id != "ε":
                        possibleDest = this.eClosure(transition.target)
                        possibleDest.sort()
                        
                        subsets[initial][transition.symbol.id].union(possibleDest)

        newStates = {}
        stateKeys = {}

        this.transitions = Set()
        this.states = Set()
        finals = Set()

        for x in range(len(subsets)):
            newStates[x] = subsets[list(subsets.keys())[x]]

            arrayTest = list(subsets.keys())[x]

            for state in arrayTest:
                for final in this.final:
                    if state == final.id:
                        finals.add(x)
                        break

            stateKeysValue = ""
            for y in list(subsets.keys())[x]:
                stateKeysValue += y
            
            stateKeys[stateKeysValue] = x

        for subset in newStates:
            for symbol in newStates[subset]:
                if newStates[subset][symbol].len() > 0:
                    stateKeysValue = ""
                    for x in newStates[subset][symbol]:
                        stateKeysValue += x
                    
                    test = newStates[subset][symbol]

                    newStates[subset][symbol] = stateKeys[stateKeysValue]
                
                else:
                    newStates[subset][symbol] = ""

        
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
        
    def eClosure(this, state, past = None):
        if past == None:
            past = []

        if state.id in past:
            return Set()
            
        past.append(state.id)
        closure = Set()
        closure.add(state.id)

        for transition in this.transitions:
            if transition.source == state and transition.symbol.id == "ε":
                closure.union(this.eClosure(transition.target, past))

        return closure
    
    def setExists(self, newSet, states):
        candidate = None

        for test in list(states.keys()):
            for state in newSet:
                if state not in test.elements:
                    candidate = None
                    break

                else:
                    candidate = test
            
            if candidate:
                return candidate, True

                
        return newSet, False
