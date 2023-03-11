from modules.components.regex import *
from modules.components.regexTree import *
from modules.components.NFA import *
from modules.components.DFA import *
from modules.components.minimizedDFA import *
from modules.common.utils import *

def testAutomata(regex, simulate):
    result = runWithTimeout(testFunction, (regex, simulate, True), 5, False)

    if not result:
        print("ERROR: Failed to generate automatas")

def testAutomatas(regex, simulate):
    print("\nTesting regexes...")

    if len(regex) != len(simulate):
        print("ERROR: options and testStrings must have the same length")
        exit()

    results = []

    for x in range(len(regex)):
        result = runWithTimeout(testFunction, (regex[x], simulate[x]), 5, False)

        if not result:
            print("ERROR: Failed to generate automatas")

        results.append(result)


    print("\nResults:")
    correct = 0
    
    for res in results:
        if res:
            correct += 1

    print(str(correct) + "/" + str(len(results)) + " correct")

def testFunction(regex, simulate, printRes = False):
    regex = Regex(regex)
    postfix = regex.postfix
    parsed = regex.validatedInfix

    print("\nRegex: " + parsed)

    tree = RegexTree(postfix, parsed)

    newNFA = NFA(tree.tree, parsed)
    subsetDFA = DFA(newNFA, parsed)

    tree = RegexTree(postfix, parsed, True)
    directDFA = DFA(tree, parsed)

    minDirectDFA = minimizedDFA(directDFA)
    minSubsetDFA = minimizedDFA(subsetDFA)

    transitionsDirect = []
    transitionsSubset = []

    for transition in minDirectDFA.transitions:
        transitionsDirect.append([transition.source.id, transition.symbol.cid, transition.target.id])

    for transition in minSubsetDFA.transitions:
        transitionsSubset.append([transition.source.id, transition.symbol.cid, transition.target.id])

    allEqual = True
    for transition in transitionsDirect:
        if transition not in transitionsSubset:
            allEqual = False
            break

    if printRes:
        minDirectDFA.print()
        minSubsetDFA.print()

        minDirectDFA.createImage()
        minSubsetDFA.createImage()

        print("\nTest results:")

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
                return True
            else:
                print("ERROR: Automata simulation results are different")
                return False
            
        else:
            return True
    else:
        print("ERROR: Minimized Subset DFA and Minimized Direct DFA are different")
        return False
        