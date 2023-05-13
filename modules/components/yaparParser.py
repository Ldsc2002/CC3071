from modules.common.set import Set
from modules.common.state import State

class YaparParser():
    def __init__(this, file, yalex):
        this.file = file
        this.yalex = yalex
        this.parse()
        this.parseSLR()

    def parse(this):        
        tokens = []
        productions = {}
        readingTokens = True
        prevProduction = None
        skip = False

        with open(this.file, 'r') as file:
            lines = file.read().splitlines()

            for line in lines:
                if "*/" in line:
                    skip = False
                    continue

                if skip:
                    continue

                if "/*" in line:
                    skip = True
                    continue

                if line != '':
                    if readingTokens:
                        if line == '%%':
                            readingTokens = False
                            continue
                        
                        line = line.replace("%token", "")
                        line = line.strip()

                        if line.count(' ') > 0:
                            line = line.split(' ')
                            for token in line:
                                tokens.append(token)
                        else:
                            tokens.append(line)

                    else:
                        line = line.strip()
                        
                        if prevProduction == None:
                            line = line.replace(":", "")
                            productions[line] = []
                            prevProduction = line

                        else: 
                            if line.count(' ') > 0:
                                line = line.split(' ')
                                for token in line:
                                    if token == ';':
                                        prevProduction = None
                                        break

                                    productions[prevProduction].append(token)
                            else:
                                if line == ';':
                                    prevProduction = None
                                    continue

                                productions[prevProduction].append(line)

        # Create a list of tokens from the yalex file
        yalexTokens = []
        for token in this.yalex.tokens:
            newToken = this.yalex.tokens[token]
            newToken = newToken.replace("return ", "")
            newToken = newToken.strip()
            yalexTokens.append(newToken)

        # Check if all tokens in the yapar file are in the yalex file
        for token in tokens:
            if token not in yalexTokens:
                raise Exception("Token '" + token + "' not found in yalex file")


        this.tokens = tokens
        this.productions = productions

    def parseSLR(this):
        def closure(production):
            productions = [production]

            for p1 in productions:
                for p2 in grammar:
                    term1 = p1.split('->')[1].split('.')[1].strip().split(' ')[0].strip()
                    term2 = p2.split('->')[0].strip()

                    if term1 == term2:
                        p2 = p2.split('->')
                        p2[1] = p2[1].strip().split('.')[1]
                        p2[1] = ' . ' + p2[1].strip()
                        p2 = '->'.join(p2)

                        if p2 not in productions:
                            productions.append(p2)
        
            return productions
                            
        def goto(production, symbol):            
            pass

        terminals = this.tokens
        symbols = Set()
        grammar = Set()
        initialGrammar = ""

        newItem = {list(this.productions.keys())[0] + "'": [this.productions[list(this.productions.keys())[0]][0]]}
        this.productions = {**newItem, **this.productions}

        for token, production in this.productions.items():
            production.insert(0, '.')

            tempProduction = ""
            for p in production:
                if p not in symbols:
                    symbols.add(p)

                if p == "|":
                    tempProduction = tempProduction.strip()
                    grammar.add(token + " -> " + tempProduction)
                    tempProduction = ". "
                    continue

                tempProduction += p + " "
                
            tempProduction = tempProduction.strip()

            if token not in terminals and initialGrammar == "":
                initialGrammar = token + " -> " + tempProduction

            grammar.add(token + " -> " + tempProduction)

        this.initial = State(closure(initialGrammar), type=0) 
        this.states = [this.initial]

        for state in this.states:
            for symbol in symbols:
                nextState = goto(state, symbol)

        print("DONE")