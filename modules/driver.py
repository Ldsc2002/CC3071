from modules.components.regex import *
from modules.components.regexTree import *
from modules.components.NFA import *

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
