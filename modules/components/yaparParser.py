from modules.proto.automata import *

class YaparParser(Automata):
    def __init__(this, file, yalex):
        this.file = file
        this.yalex = yalex
        this.parse()
        this.parseSLR()
        this.filename = "DFA_Yapar_" + file.split("/")[-1].split(".")[0]
        this.shape = "square"

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
            """ 
            PARAMETERS:
                production: production to be checked in format 'S -> . A B'
            RETURNS:
                list of productions that can be derived from the given production 
            """

            productions = [production]

            for p1 in productions:
                for p2 in grammar:
                    # If the left side of the production is the same as the right side of the grammar
                    if p1.split('.')[1].strip().split(' ')[0] == p2.split('->')[0].strip():
                        p2 = p2.split('->')
                        p2[1] = p2[1].strip().split('.')[1]
                        p2[1] = ' . ' + p2[1].strip()
                        p2 = '->'.join(p2)

                        if p2 not in productions:
                            productions.append(p2)
        
            return productions
                            
        def goto(production, symbol):   
            """ 
            PARAMETERS:
                production: production to be checked in format 'S -> . A B'
                symbol: symbol to be checked
            RETURNS:
                list of productions that can be derived from the given production and symbol
                returns None if no productions can be derived
            """  

            productions = []

            # Verify if the symbol is in the right side of the production
            for p in production.id:
                if p.split('.')[1].strip().split(' ')[0] == symbol:
                    left, right = p.split(".")
                    right = right.strip().split(' ')

                    if len(right) == 1:
                        p = left + " " + right[0] + " ."
                    else:
                        p = left + " " + right[0] + " ." + " ".join(right[1:])
                    
                    productions.append(p)

            # If no productions can be derived, return None
            if productions == []:
                return None
            else:
                # Verify all new productions
                for p in productions:
                    right = p.split('.')[1].strip().split(' ')[0].strip()

                    # If the production is not a terminal, check if it can be derived
                    if right not in this.tokens:
                        currentClosure = closure(p)

                        for c in currentClosure:
                            if c not in productions:
                                productions.append(c)

            # Check if any production is final
            for production in productions:
                if production.replace('.', '').strip() == initialGrammar.replace('.', '').strip():
                    right = initialGrammar.split('.')[1].strip().split(' ')[0].strip()
                    left = production.split('.')[0].strip().split(' ')[-1].strip()

                    if left == right:
                        # Return final state
                        return State(productions, type=2)
                    
            # Return new state
            return State(productions, type=1)
        
        def addState(newState):
            """ 
            PARAMETERS:
                newState: state to be added to the list of states

            Adds the given state to the list of states if it is not already in the list
            """

            equal = True
            
            for state in this.states:
                for s in state.id:
                    if s not in newState.id:
                        equal = False
                        break

                if equal:
                    break

                for s in newState.id:
                    if s not in state.id:
                        equal = False
                        break

                if equal:
                    break
                elif state != this.states[-1]:
                    equal = True

            if not equal:
                this.states.append(newState)

        terminals = this.tokens
        this.symbols = Set()
        grammar = Set()
        initialGrammar = ""

        # Add initial production to the beginning of the productions
        newItem = {list(this.productions.keys())[0] + "'": [this.productions[list(this.productions.keys())[0]][0]]}
        this.productions = {**newItem, **this.productions}

        # Format the productions to be in the form of A -> . a b c and find the initial state
        for token, production in this.productions.items():
            production.insert(0, '.')

            tempProduction = ""
            for p in production:
                if p not in this.symbols:
                    this.symbols.add(p)

                # If production includes another production, split it and reset tempProduction
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

        # Create the initial state
        this.initial = State(closure(initialGrammar), type=0) 
        this.states = [this.initial]
        this.transitions = Set()
        this.final = Set()

        for state in this.states:
            for symbol in this.symbols:
                nextState = goto(state, symbol)

                if nextState != None:
                    addState(nextState)

                    # Verify if the state is final
                    if nextState.type.name == "final":
                        this.final.add(nextState)

                    this.transitions.add(Transition(state, nextState, Symbol(symbol)))