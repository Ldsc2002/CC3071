from modules.components.regex import *
from modules.components.regexTree import *
from modules.components.NFA import *
from modules.common.utils import *

def generateNFA(regex):
    print("\n ----- Generating NFA -----")
    print("Original Infix: " + regex)

    postfix = Regex(regex).postfix
    print("Parsed Infix: " + Regex(regex).validatedInfix)
    print("Postfix: " + postfix)

    tree = RegexTree(postfix)
    tree.printTree()

    NFA(tree.tree).createImage()

def testRun():
    print('\n----- Testing Infix to AFN -----')
    testString = 'a|b'
    correctString = 'ab|'

    print('\nTest 1: Infix to Postfix')
    test = Regex(testString).postfix
    print('Expected: ' + correctString + ' --- Actual: ' + test)
    assert test == correctString

    print('\nTest 2: Regex Tree')
    test = RegexTree(test)
    test.printTree()

    print('\nTest 3: NFA')
    NFA(test.tree).createImage()
