from modules.components.regex import *
from modules.components.regexTree import *
from modules.components.NFA import *
from modules.components.DFA import *
from modules.common.utils import *

def generateNFA(regex):
    print("\n ----- Generating NFA -----")
    print("Original Infix: " + regex)

    postfix = Regex(regex).postfix
    print("Parsed Infix: " + Regex(regex).validatedInfix)
    print("Postfix: " + postfix)

    tree = RegexTree(postfix)
    tree.printTree()

    newNFA = NFA(tree.tree)
    newNFA.print()
    # newNFA.createImage()

    subsetDFA = DFA(newNFA)
    subsetDFA.print()
    subsetDFA.createImage()

    # tree = RegexTree(postfix, True)
    # tree.printTree()

    # directDFA = DFA(tree)
    # directDFA.print()
    # directDFA.createImage()
