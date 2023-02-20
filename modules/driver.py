from modules.components.regex import *

def testRun():
    print('\nTesting infixToPostfix')

    print('Test 1: a+b*c')
    test = Regex('a+b*c').postfix
    print('Expected: abc*+ --- Actual: ' + test)
    assert Regex('a+b*c').postfix == 'abc*+'

    print('Test 2: a+b*c+')
    test = Regex('a+b*c+').postfix
    print('Expected: abc*+ --- Actual: ' + test)
    assert Regex('a+b*c+').postfix == 'abc*+'