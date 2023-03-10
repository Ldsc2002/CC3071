from modules.proto.automata import *

class minimizedDFA(Automata):
    def __init__(this, nfa):
        this.filename = "min" + nfa.filename
        this.initial = nfa.initial
        this.states = nfa.states
        this.final = nfa.final
        this.transitions = nfa.transitions
        this.symbols = nfa.symbols
        
        this.minimize()

    def minimize(this):
        def verifyTransitionExists(source, target, symbol, testTransitions):
            for transition in testTransitions:
                if transition.source.id == source and transition.target.id == target and transition.symbol.id == symbol.id:
                    return True
            return False

        F = this.final
        Q = this.states

        difference = Set()
        testIDs = Set()

        for state in F:
            testIDs.add(state.id)

        for state in Q:
            if state.id not in testIDs.elements:
                difference.add(state)

        P = Set()
        W = Set()
        P.add(F)
        W.add(F)

        if len(difference) > 0:
            P.add(difference)
            W.add(difference)

        while len(W) > 0:
            A = W.pop()

            for symbol in this.symbols.elements:
                X = Set()
                
                for transition in this.transitions:
                    if transition.symbol.id == symbol:
                        for state in A:
                            if transition.target.id == state.id:
                                X.add(transition.source)

                for partition in P:
                    intersection = Set()
                    difference = Set()
                    testIDs = Set()

                    for xState in X:
                        testIDs.add(xState.id)

                    for xState in X:
                        for pState in partition:
                            if xState.id == pState.id:
                                intersection.add(xState)

                    for pState in partition:
                        if pState.id not in testIDs.elements:
                            difference.add(pState)

                    if len(intersection) > 0 and len(difference) > 0:
                        P.remove(partition)
                        P.add(intersection)
                        P.add(difference)

                        if partition in W:
                            W.remove(partition)
                            W.add(intersection)
                            W.add(difference)
                        else:
                            if len(intersection) <= len(difference):
                                W.add(intersection)
                            else:
                                W.add(difference)

        P.elements.sort(key = len, reverse = False)
        P.elements.sort(key = lambda x: x.elements[0].id)

        this.states = Set()
        
        newFinal = Set()
        newInitial = None
        newStates = []
        for enum, partition in enumerate(P):
            newState = State(enum)       

            this.states.add(newState)
            newStates.append([enum, partition])

            for state in partition:
                for final in this.final:
                    if state.id == final.id:
                        newFinal.add(newState)

                if state.id == this.initial.id:
                    newInitial = newState

        this.final = newFinal
        this.initial = newInitial

        newTransitions = Set()
        for transition in this.transitions:
            for state, partition in newStates:
                for item in partition:
                    if transition.source.id == item.id:
                        for state2, partition2 in newStates:
                            for item2 in partition2:
                                if transition.target.id == item2.id and not verifyTransitionExists(state, state2, transition.symbol, newTransitions):
                                    newTransitions.add(Transition(State(state), State(state2), transition.symbol))
                                    break  
        
        this.transitions = newTransitions