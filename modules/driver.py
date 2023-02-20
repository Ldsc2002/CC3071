from modules.components.regex import *

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