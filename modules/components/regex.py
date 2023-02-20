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
        alphabet = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'E'
        ]

        symbols = ['*', '+', '?', '.', '|']

        openParen = 0
        closeParen = 0
        for c in infix:
            if c == '(':
                openParen += 1
            elif c == ')':
                closeParen += 1

            if c not in alphabet and c not in symbols and c != '(' and c != ')':
                raise ValueError(
                    "Invalid character in infix expression: " + c)

        if openParen != closeParen:
            if openParen > closeParen:
                infix = infix + (openParen - closeParen) * ')'
            if closeParen > openParen:
                infix = (closeParen - openParen) * '(' + infix

        while True:
            if infix[-1] in symbols:
                infix = infix[:-1]
            if infix[0] in symbols:
                infix = infix[1:]
            else:
                break

        return infix

            

