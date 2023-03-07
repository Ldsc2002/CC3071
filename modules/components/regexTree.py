from modules.common.node import *
import pydot

class RegexTree():
    def __init__(this, postfix, forDFA = False):
        this.postfix = postfix
        this.tree = this.buildTree(forDFA)

    def buildTree(this, forDFA = False):
        if forDFA:
            this.postfix = this.postfix + '#.'

        stack = []
        for token in this.postfix:
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
                stack.append(Node('?', left))
            elif token == '*':
                left = stack.pop()
                stack.append(Node('*', left))
            elif token == '+': 
                left = stack.pop()
                stack.append(Node('+', left))
            else:
                stack.append(Node(token))
        return stack.pop()

    def printTree(this):
        graph = pydot.Dot(graph_type='graph')
        this.tree.printTree(graph)
        graph.write_png('out/regexTree.png')