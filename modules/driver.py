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

def debugAutomatas(regex, simulate):
    regex = Regex(regex)
    postfix = regex.postfix
    parsed = regex.validatedInfix

    tree = RegexTree(postfix, parsed)
    newNFA = NFA(tree.tree, parsed)
    subsetDFA = DFA(newNFA, parsed)
    
    tree = RegexTree(postfix, parsed, True)
    directDFA = DFA(tree, parsed)

    minDirectDFA = minimizedDFA(directDFA)
    minSubsetDFA = minimizedDFA(subsetDFA)

    transitionsDirect = []
    transitionsSubset = []

    for transition in directDFA.transitions:
        transitionsDirect.append([transition.source.id, transition.symbol.cid, transition.target.id])

    for transition in subsetDFA.transitions:
        transitionsSubset.append([transition.source.id, transition.symbol.cid, transition.target.id])

    allEqual = True
    for transition in transitionsDirect:
        if transition not in transitionsSubset:
            allEqual = False
            break

    if allEqual:
        print("\nMinimized Subset DFA and Minimized Direct DFA are equal")

        if simulate:
            results = []
            result = True

            results.append(newNFA.simulate(simulate))
            results.append(subsetDFA.simulate(simulate))
            results.append(directDFA.simulate(simulate))
            results.append(minDirectDFA.simulate(simulate))
            results.append(minSubsetDFA.simulate(simulate))

            for res in results:
                if res != results[0]:
                    result = False
                    break

            if result:
                print("\nAll automatas are working correctly")
            else:
                print("\nERROR: Automata simulation results are different")
    else:
        print("\nERROR: Minimized Subset DFA and Minimized Direct DFA are different")