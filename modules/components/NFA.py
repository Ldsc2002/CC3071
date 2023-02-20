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

            this.initial = initial
            this.final.add(final)
            
            this.symbols.add(node.value)

            return this

        elif node.value == '|':
            initial = State(str(this.counter))
            this.states.add(initial)
            this.counter += 1

            left = this.subsetConstruction(node.left)
            this.transitions.add(Transition(initial, left.initial, Symbol('ε')))

            final = State(str(this.counter + 1))
            this.states.add(final)
            this.counter += 1

            right = this.subsetConstruction(node.right)
            this.transitions.add(Transition(initial, right.initial, Symbol('ε')))

            if len(this.final) > 0:
                newFinal = State(str(this.counter + 1))
                this.states.add(newFinal)
                this.counter += 1
                
                for x in range(len(this.final)):
                    this.transitions.add(Transition(this.final.pop(), newFinal, Symbol('ε')))

                this.final.add(newFinal)


            this.initial = initial

            this.symbols.add('ε')

            return this