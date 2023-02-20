import pydot

class Node():
    def __init__(this, value, left = None, right = None):
        this.value = value
        this.left = left
        this.right = right
    
    def printTree(this, graph):
        thisNode = pydot.Node(this.value)
        graph.add_node(thisNode)

        if this.left is not None:
            this.left.printTree(graph)
            graph.add_edge(pydot.Edge(thisNode, this.left.value))

        if this.right is not None:
            this.right.printTree(graph)
            graph.add_edge(pydot.Edge(thisNode, this.right.value))