from modules.regex import infixToPostfix

def testRun():
    print('Testing infixToPostfix')
    test = infixToPostfix('a+b*c')
    print(test)
    assert test == 'abc*+'