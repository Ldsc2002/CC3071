class Regex():
    def __init__(this, infix, alphabet = None):
        this.alphabet = alphabet
        this.infix = infix
        this.validatedInfix = None
        this.postfix = this.infixToPostfix(infix)

    def infixToPostfix(this, regex):
        regex = this.validateInfix(regex)

        specials = {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1}

        pofix = ""
        stack = []

        skip = False
        for x in range(len(regex)):
            c = regex[x]

            if skip:
                pofix = pofix + c
                
                if c == "'":
                    skip = False

            elif c == '(':
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
                if c == "'" and regex[x + 1] == "#":
                    skip = True

                pofix = pofix + c

        while stack:
            pofix = pofix + stack.pop()

        return pofix
    
    def validateInfix(this, infix):
        alphabet = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'E'
        ]

        if this.alphabet:
            alphabet = this.alphabet

        symbols = ['|', '.']
        unary = ['*', '?', '+']
        validForConcat = alphabet + ['(', ')'] + unary + ["'"]

        # Add missing concatenation symbols
        newInfix = ''
        readingAscii = False

        for x in range(len(infix)):
            if readingAscii:
                newInfix = newInfix + infix[x]

                if infix[x] == "'":
                    readingAscii = False
                
                continue

            if infix[x] == "'":
                readingAscii = True

            if x > 0 and x < len(infix):
                if infix[x - 1] in alphabet and infix[x] in alphabet:
                    newInfix = newInfix + '.'

                elif infix[x - 1] in unary and infix[x] in alphabet:
                    newInfix = newInfix + '.'

                elif (infix[x - 1] in alphabet or infix[x - 1] in unary) and infix[x] == '(':
                    newInfix = newInfix + '.'

                elif infix[x - 1] == ')' and infix[x] == '(':
                    newInfix = newInfix + '.'

                elif infix[x - 1] == ')' and infix[x] in alphabet:
                    newInfix = newInfix + '.'

            newInfix = newInfix + infix[x]
        
        infix = newInfix

        openParen = 0
        closeParen = 0
        closeBeforeOpen = False

        skip = False

        for x in range(len(infix)):
            c = infix[x]

            if skip:
                if c == "'":
                    skip = False
                
                continue

            elif c == "'":
                tempCounter = x + 1
                tempC = ""

                if infix[tempCounter] == "#":
                    c = alphabet[0]
                    skip = True
                    continue

                while tempCounter < len(infix) and infix[tempCounter] != "'":
                    tempC = tempC + infix[tempCounter]
                    tempCounter += 1

                c = int(tempC)

                skip = True

            if c in symbols:
                if x == 0 or x == len(infix) - 1:
                    raise ValueError("Regex cannot start or end with operator: " + c + " at index " + str(x))

                elif infix[x - 1] not in validForConcat or infix[x + 1] not in validForConcat:
                    raise ValueError("Invalid symbol in infix expression: " + c + " at index " + str(x))

            elif c in unary:
                if x == 0 or (x > 0 and infix[x - 1] not in validForConcat):
                    raise ValueError("Invalid symbol in infix expression: " + c + " at index " + str(x))

            if closeParen > openParen:
                closeBeforeOpen = True

            if c == '(':
                openParen += 1

            elif c == ')':
                closeParen += 1

            elif c not in alphabet and c not in symbols and c not in unary and c != '(' and c != ')':
                raise ValueError("Invalid character in infix expression: " + c)  

        if openParen != closeParen:
            if openParen > closeParen:
                infix = infix + (openParen - closeParen) * ')'
            if closeParen > openParen:
                infix = (closeParen - openParen) * '(' + infix
        elif closeBeforeOpen:
            raise ValueError("Invalid infix expression: close parenthesis before open parenthesis")

        this.validatedInfix = infix
        return infix

            

