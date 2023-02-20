from modules.components.regex import *
from modules.components.regexTree import *
from modules.components.NFA import *

def testRun():
    print('\n----- Testing infixToPostfix -----')

    print('\nTest 1: a+b*c')
    test = Regex('a+b*c').postfix
    print('Expected: abc*+ --- Actual: ' + test)
    assert test == 'abc*+'

    print('\nTest 2: a+b*c+')
    test = Regex('a+b*c+').postfix
    print('Expected: abc*+ --- Actual: ' + test)
    assert test == 'abc*+'

    print('\nTest 3: (a+b)*c)')
    test = Regex('(a+b)*c)').postfix
    print('Expected: ab+c* --- Actual: ' + test)
    assert test == 'ab+c*'

    print('\n\n----- Testing tree building -----')
    print('\nTest 1: abc*+')
    test = RegexTree('abc*+').printTree()

    print('\n\n----- Testing NFA -----')
    print('\nTest 1: abc*+')
    test = RegexTree('a').tree
    NFA(test).createImage()
