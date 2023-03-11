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

    print("\nRegex: " + parsed)

    tree = RegexTree(postfix, parsed)

    newNFA = runWithTimeout(NFA, (tree.tree, parsed), timeout_duration = 3)
    subsetDFA = runWithTimeout(DFA, (newNFA, parsed), timeout_duration = 3)
    
    tree = RegexTree(postfix, parsed, True)
    directDFA = runWithTimeout(DFA, (tree, parsed), timeout_duration = 3)

    minDirectDFA = runWithTimeout(minimizedDFA, (directDFA,), timeout_duration = 3)
    minSubsetDFA = runWithTimeout(minimizedDFA, (subsetDFA,), timeout_duration = 3)

    transitionsDirect = []
    transitionsSubset = []

    if newNFA == "Timeout":
        print("ERROR: NFA generation timed out")
        return
    
    if subsetDFA == "Timeout":
        print("ERROR: Subset DFA generation timed out")
        return
    
    if directDFA == "Timeout":
        print("ERROR: Direct DFA generation timed out")
        return
    
    if minDirectDFA == "Timeout":
        print("ERROR: Minimized Direct DFA generation timed out")
        return
    
    if minSubsetDFA == "Timeout":
        print("ERROR: Minimized Subset DFA generation timed out")
        return
    

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
        print("SUCCESS: Minimized Subset DFA and Minimized Direct DFA are equal")

        if simulate:
            results = []
            result = True

            results.append(newNFA.simulate(simulate, False))
            results.append(subsetDFA.simulate(simulate, False))
            results.append(directDFA.simulate(simulate, False))
            results.append(minDirectDFA.simulate(simulate, False))
            results.append(minSubsetDFA.simulate(simulate, False))

            for res in results:
                if res != results[0]:
                    result = False
                    break

            if result:
                print("SUCCESS: Automata simulation results are equal")
            else:
                print("ERROR: Automata simulation results are different")
    else:
        print("ERROR: Minimized Subset DFA and Minimized Direct DFA are different")