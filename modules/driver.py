from modules.components.regex import *
from modules.components.regexTree import *
from modules.components.NFA import *
from modules.components.DFA import *
from modules.common.utils import *

def generateNFA(regex):
    print("\n ----- Generating NFA -----")
    print("Original Infix: " + regex)

    regex = Regex(regex)
    postfix = regex.postfix
    parsed = regex.validatedInfix

    print("Parsed Infix: " + parsed)
    print("Postfix: " + postfix)

    tree = RegexTree(postfix, parsed)
    tree.printTree()

    newNFA = NFA(tree.tree, parsed)
    newNFA.print()
    newNFA.createImage()

    subsetDFA = DFA(newNFA, parsed)
    subsetDFA.print()
    subsetDFA.createImage()

    # tree = RegexTree(postfix, True)
    # tree.printTree()

    # directDFA = DFA(tree)
    # directDFA.print()
    # directDFA.createImage()
