import pydot
from modules.common.symbol import *

class Node(object):
    def __init__(this, value, left = None, right = None):
        this.value = Symbol(value)     
        this.left = left
        this.right = right
    
    def printTree(this, graph, id = 0):
        thisNode = pydot.Node(id, label = this.character)
        graph.add_node(thisNode)
        id += 1

        if this.left is not None:
            this.left.printTree(graph, id)
            graph.add_edge(pydot.Edge(thisNode, id))
            id += 1

        if this.right is not None:
            this.right.printTree(graph, id)
            graph.add_edge(pydot.Edge(thisNode, id))
            id += 1

    def __getattribute__(this, name: str):
        if name == 'value':
            return object.__getattribute__(this, name).id
        elif name == 'character':
            return object.__getattribute__(this, "value").cid
        else:
            return object.__getattribute__(this, name)