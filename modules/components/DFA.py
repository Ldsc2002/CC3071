from modules.proto.automata import *
from modules.components.NFA import *
from modules.components.regexTree import *

class DFA(Automata):
    def __init__(this, regex):
        if isinstance(regex, RegexTree):
            super().__init__()

            this.directConstruction(regex)
        elif isinstance(regex, NFA):
            this.states = Set()
            this.final = Set()
            this.symbols = Set()
            this.initial = State()
            this.transitions = Set()

            this.subsetConstruction(regex)
        else:
            raise Exception('Invalid parameter for DFA constructor')


    def directConstruction(this, tree):
        pass

    def subsetConstruction(this, nfa):
        this.symbols = nfa.symbols
        
        if "ε" in this.symbols:
            this.symbols.remove("ε")

        counter = 0
        state = State(str(counter), Type(0))

        stack = nfa.states.elements

        if nfa.initial in nfa.final:
            this.final.add(state)
            state.type = Type(3)

        this.states.add(state)
        this.initial = state
        counter += 1

        for state in stack:
            for symbol in this.symbols:
                states = this.possibleDest(state, symbol, nfa.transitions)
                newStates = Set()

                for s in states:
                    test = this.epsilonClosure(s)
                    newStates.union(this.epsilonClosure(s))

                if len(newStates) > 0:
                    for target in newStates:
                        if target in this.states:
                            for s in this.states:
                                if s == target:
                                    target = s
                                    break

                        else:
                            target.id = str(counter)
                            counter += 1
                            target.type = Type(1)

                            if target in nfa.final:
                                this.final.add(target)
                                target.type = Type(2)

                            this.states.add(target)

                            stack.append(target)

                        if not this.checkTransitionExists(state, symbol, target):
                            this.transitions.add(Transition(state, target, Symbol(symbol)))

        return this
    
    def epsilonClosure(this, state):
        closure = Set()
        closure.add(state)

        for transition in this.transitions:
            if transition.symbol == "ε" and transition.source.id == state.id:
                closure.union(this.epsilonClosure(transition.target))

        return closure
    
    def possibleDest(this, state, symbol, transitions):
        moves = Set()
    
        for transition in transitions:
            if transition.source.id == state.id and transition.symbol.id == symbol:
                moves.add(transition.target)

        return moves

    
    def checkTransitionExists(this, state, symbol, target):
        for transition in this.transitions:
            if transition.source.id == state.id and transition.symbol.id == symbol and transition.target.id == target.id:
                True

        return False