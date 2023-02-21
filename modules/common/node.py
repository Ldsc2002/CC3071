import pydot
import uuid
from modules.common.symbol import *

class Node(object):
    def __init__(this, value, left = None, right = None):
        this.value = Symbol(value)     
        this.left = left
        this.right = right
    
    def printTree(this, graph, parent = None):
        thisNode = pydot.Node(str(uuid.uuid4()), label = this.character)
        graph.add_node(thisNode)

        if parent is not None:
            graph.add_edge(pydot.Edge(parent, thisNode))

        if this.left is not None:
            this.left.printTree(graph, thisNode)

        if this.right is not None:
            this.right.printTree(graph, thisNode)

    def __getattribute__(this, name: str):
        if name == 'value':
            return object.__getattribute__(this, name).id
        elif name == 'character':
            return object.__getattribute__(this, "value").cid
        else:
            return object.__getattribute__(this, name)