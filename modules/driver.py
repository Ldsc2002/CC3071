from modules.components.regex import *
from modules.components.regexTree import *
from modules.components.NFA import *
from modules.components.DFA import *
from modules.components.minimizedDFA import *
from modules.common.utils import *

def generateNFA(regex, simulate = None):
    checkFolder("out/")
    deleteAllFiles("out/")

    print("\n ----- Generating Automatas -----")
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

    tree = RegexTree(postfix, parsed, True)
    tree.printTree()

    directDFA = DFA(tree, parsed)
    directDFA.print()
    directDFA.createImage()

    minDirectDFA = minimizedDFA(directDFA)
    minDirectDFA.print()
    minDirectDFA.createImage()

    minSubsetDFA = minimizedDFA(subsetDFA)
    minSubsetDFA.print()
    minSubsetDFA.createImage()

    if simulate:
        newNFA.simulate(simulate)
        subsetDFA.simulate(simulate)
        directDFA.simulate(simulate)
        minDirectDFA.simulate(simulate)
        minSubsetDFA.simulate(simulate)