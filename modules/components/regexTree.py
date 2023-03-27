from modules.common.node import *
import pydot

class RegexTree():
    def __init__(this, postfix, filename = None, forDFA = False):
        if filename is None:
            filename = postfix

        if forDFA:
            filename = "DFA_(" + filename
        else:
            filename = "NFA_(" + filename

        this.postfix = postfix
        this.filename = "Tree_" + filename + ")"
        this.tree = this.buildTree(forDFA)

    def buildTree(this, forDFA = False):
        if forDFA:
            this.postfix = this.postfix + '#.'

        stack = []
        skip = False

        for x in range(len(this.postfix)):
            token = this.postfix[x]
            
            if skip:
                if token == "'":
                    skip = False
                continue

            if token == "'":
                tempToken = token

                while True:
                    tempToken += this.postfix[this.postfix.index(tempToken[-1], x) + 1]

                    if tempToken[-1] == "'":
                        token = tempToken
                        skip = True
                        break

            if token == '.':
                right = stack.pop()
                left = stack.pop()
                stack.append(Node('.', left, right))
            elif token == '|':
                right = stack.pop()
                left = stack.pop()
                stack.append(Node('|', left, right))
            elif token == '?':
                left = stack.pop()
                stack.append(Node('|', left, Node('E')))
            elif token == '*':
                left = stack.pop()
                stack.append(Node('*', left))
            elif token == '+': 
                left = stack.pop()
                stack.append(Node('.', left, Node('*', left)))
            else:
                stack.append(Node(token))

        if len(stack) != 1:
            raise Exception("Invalid postfix expression")

        return stack.pop()

    def printTree(this):
        graph = pydot.Dot(graph_type='graph')
        this.tree.printTree(graph)
        graph.write_png('out/' + this.filename + '.png')