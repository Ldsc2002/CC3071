from modules.proto.automata import *

class NFA(Automata):
    def __init__(this, startNode):
        super().__init__()

        this.counter = 0
        initial, final = this.thompsonConstruction(startNode)

        this.initial = initial
        this.final.add(final)

    def thompsonConstruction(this, node):
        if node.left is None and node.right is None:
            initial = State(str(this.counter))
            final = State(str(this.counter + 1))
            this.counter += 1

            this.states.add(initial)
            this.states.add(final)

            this.transitions.add(Transition(initial, final, Symbol(node.value)))
            this.symbols.add(node.value)
            
            this.symbols.add(node.value)

        elif node.value == '|':
            initial = State(str(this.counter))
            this.states.add(initial)
            this.counter += 1

            leftInitial, leftFinal = this.thompsonConstruction(node.left)
            this.transitions.add(Transition(initial, leftInitial, Symbol('ε')))

            this.counter += 1

            rightInitial, rightFinal = this.thompsonConstruction(node.right)
            this.transitions.add(Transition(initial, rightInitial, Symbol('ε')))

            finals = [leftFinal, rightFinal]

            final = State(str(this.counter + 1))
            this.states.add(final)
            this.counter += 1
            
            for x in range(len(finals)):
                this.transitions.add(Transition(finals.pop(), final, Symbol('ε')))

            this.symbols.add('ε')

        elif node.value == '*':
            initial = State(str(this.counter))
            this.states.add(initial)
            this.counter += 1

            leftInitial, leftFinal = this.thompsonConstruction(node.left)

            this.transitions.add(Transition(initial, leftInitial, Symbol('ε')))
            this.transitions.add(Transition(leftFinal, leftInitial, Symbol('ε')))

            final = State(str(this.counter + 1))
            this.states.add(final)
            this.counter += 1

            this.transitions.add(Transition(initial, final, Symbol('ε')))
            this.transitions.add(Transition(leftFinal, final, Symbol('ε')))

            this.symbols.add('ε')

        elif node.value == '+':
            aInitial, aFinal = this.thompsonConstruction(node.left)

            initial = State(str(this.counter))
            this.states.add(initial)
            this.counter += 1

            leftInitial, leftFinal = this.thompsonConstruction(node.left)

            this.transitions.add(Transition(initial, leftInitial, Symbol('ε')))
            this.transitions.add(Transition(leftFinal, leftInitial, Symbol('ε')))

            final = State(str(this.counter + 1))
            this.states.add(final)
            this.counter += 1

            this.transitions.add(Transition(leftFinal, final, Symbol('ε')))
            this.transitions.add(Transition(aFinal, final, Symbol('ε')))

            initial = aInitial
            this.symbols.add('ε')

        elif node.value == '?':
            initial = State(str(this.counter))
            this.states.add(initial)
            this.counter += 1

            leftInitial, leftFinal = this.thompsonConstruction(node.left)
            this.transitions.add(Transition(initial, leftInitial, Symbol('ε')))

            this.counter += 1

            rightInitial, rightFinal = this.thompsonConstruction(Node('ε'))
            this.transitions.add(Transition(initial, rightInitial, Symbol('ε')))

            finals = [leftFinal, rightFinal]

            final = State(str(this.counter + 1))
            this.states.add(final)
            this.counter += 1
            
            for x in range(len(finals)):
                this.transitions.add(Transition(finals.pop(), final, Symbol('ε')))

            this.symbols.add('ε')

        elif node.value == '.':
            leftInitial, leftFinal = this.thompsonConstruction(node.left)
            rightInitial, rightFinal = this.thompsonConstruction(node.right)

            initial = leftInitial
            final = rightFinal

        return initial, final