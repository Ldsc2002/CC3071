class Regex():
    def __init__(this, infix):
        this.infix = infix
        this.postfix = this.infixToPostfix(infix)

    def infixToPostfix(this, regex):
        regex = this.validateInfix(regex)

        specials = {'*': 5, '+': 4, '?': 3, '.': 2, '|': 1}

        pofix = ""
        stack = []

        for c in regex:
            if c == '(':
                stack.append(c)
            elif c == ')':
                while stack and stack[-1] != '(':
                    pofix = pofix + stack.pop()
                stack.pop()
            elif c in specials:
                while stack and stack[-1] != '(' and specials.get(
                        c, 0) <= specials.get(stack[-1], 0):
                    pofix = pofix + stack.pop()

                stack.append(c)
            else:
                pofix = pofix + c

        while stack:
            pofix = pofix + stack.pop()

        return pofix
    
    def validateInfix(this, infix):
        symbols = ['*', '+', '?', '.', '|']

        while True:
            if infix[-1] in symbols:
                infix = infix[:-1]
            else:
                break

        return infix

            

