from modules.proto.automata import *

class NFA(Automata):
    def __init__(this, startNode):
        this.counter = 0
        super().__init__(State(str(this.counter)))

        automata = this.subsetConstruction(startNode)

    def subsetConstruction(this, node):
        if node.left is None and node.right is None:
            initial = State(str(this.counter))
            final = State(str(this.counter + 1))
            this.counter += 1

            this.states.add(initial)
            this.states.add(final)

            this.transitions.add(Transition(initial, final, Symbol(node.value)))
            
            this.symbols.add(node.value)
            this.final.add(final)

            this.initial = initial

            return this

        if node.value == '*':
            leftFragment = this.subsetConstruction(node.left)
            initial = State(str(this.counter))
            final = State(str(this.counter + 1))

            this.counter += 1

            this.states.add(initial)
            this.states.add(final)

            this.transitions.add(Transition(initial, leftFragment.initial, Symbol('epsilon')))
            this.transitions.add(Transition(leftFragment.final.peekLast(), final, Symbol('epsilon')))
            this.transitions.add(Transition(initial, final, Symbol('epsilon')))
            this.transitions.add(Transition(final, initial, Symbol('epsilon')))

            this.symbols.add('')
            this.final.add(final)

            this.initial = initial

            return this