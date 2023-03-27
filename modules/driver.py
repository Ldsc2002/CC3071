from modules.components.regex import *
from modules.components.regexTree import *
from modules.components.NFA import *
from modules.components.DFA import *
from modules.components.minimizedDFA import *
from modules.common.utils import *
from modules.components.automataTester import *
from modules.components.yalexParser import *

def readYalex(file): 
    checkFolder("out/")
    deleteAllFiles("out/")

    print("\n ----- Reading Yalex file -----")

    yalex = YalexParser(file)
    print("Infix from Yalex file: " + yalex.regex)
    
    regex = Regex(yalex.regex, yalex.alphabet)
    postfix = regex.postfix

    print("\nParsed Infix: " + regex.validatedInfix)
    print("\nPostfix: " + postfix)

    tree = RegexTree(postfix, file.split("/")[-1])
    tree.printTree()

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

def runTests(regex, simulate):
    checkFolder("out/")
    deleteAllFiles("out/")

    if isinstance(regex, str):
        testAutomata(regex, simulate)
    elif isinstance(regex, list):
        testAutomatas(regex, simulate)
        