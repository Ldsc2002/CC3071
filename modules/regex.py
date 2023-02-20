def infixToPostfix(regex):
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