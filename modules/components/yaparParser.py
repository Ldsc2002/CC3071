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
                for p2 in this.grammar:
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
            state = None
            
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
                return newState               

            else:
                return state

        terminals = this.tokens
        this.symbols = Set()
        this.grammar = Set()
        initialGrammar = ""

        # Add initial production to the beginning of the productions
        newItem = {list(this.productions.keys())[0] + "'": [this.productions[list(this.productions.keys())[0]][0]]}
        this.productions = {**newItem, **this.productions}

        # Format the productions to be in the form of A -> . a b c and find the initial state
        for token, production in this.productions.items():
            production.insert(0, '.')

            tempProduction = ""
            for p in production:
                if p not in this.symbols and p not in ["|", ".", " "]:
                    this.symbols.add(p)

                # If production includes another production, split it and reset tempProduction
                if p == "|":
                    tempProduction = tempProduction.strip()
                    this.grammar.add(token + " -> " + tempProduction)
                    tempProduction = ". "
                    continue

                tempProduction += p + " "
                
            tempProduction = tempProduction.strip()

            if token not in terminals and initialGrammar == "":
                initialGrammar = token + " -> " + tempProduction

            this.grammar.add(token + " -> " + tempProduction)

        # Create the initial state
        this.initial = State(closure(initialGrammar), type=0) 
        this.states = [this.initial]
        this.transitions = Set()
        this.final = Set()

        for state in this.states:
            for symbol in this.symbols:
                nextState = goto(state, symbol)

                if nextState != None:
                    nextState = addState(nextState)

                    # Verify if the state is final
                    if nextState.type.name == "final":
                        this.final.add(nextState)

                    this.transitions.add(Transition(state, nextState, Symbol(symbol)))

        for i in range(len(this.states)):
            this.states[i].tokenID = i + 1

    def first(this, symbol):
        """ 
        PARAMETERS:
            symbol: symbol to be checked
        RETURNS:
            list of symbols that can be derived from the given symbol
        """  

        if symbol in this.tokens:
            return [symbol]

        firsts = []
        for production in this.grammar:
            if production.split('->')[0].strip() == symbol:
                right = production.split('->')[1].strip().split(' ')[0].strip()

                if right in this.tokens:
                    firsts.append(right)
                else:
                    firsts += this.first(right)

        return firsts
    
    def follow(this, symbol):
        """ 
        PARAMETERS:
            symbol: symbol to be checked
        RETURNS:
            list of symbols that can be derived from the given symbol
        """  

        follows = []
        for production in this.grammar:
            right = production.split('->')[1].strip().split(' ')
            left = production.split('->')[0].strip()

            if symbol in right:
                index = right.index(symbol) + 1

                if index < len(right):
                    if right[index] in this.tokens:
                        follows.append(right[index])
                    else:
                        follows += this.first(right[index])
                else:
                    if left != symbol:
                        follows += this.follow(left)

        # DELETE DUPLICATES
        newFollows = []
        for follow in follows:
            if follow not in newFollows:
                newFollows.append(follow)

        return newFollows
    
    def buildParsingTable(this):
        """ 
        Builds the parsing table
        """  

        terminals = this.tokens + ["$"]
        nonTerminals = this.symbols.difference(Set(this.tokens))
        goToTable = {}
        actionTable = {}
        stateIDs = {}

        for state in this.states:
            goToTable[state.tokenID] = {}
            actionTable[state.tokenID] = {}

            stateIDs[state.tokenID] = state

        for transition in this.transitions:
            if transition.source.tokenID not in goToTable:
                goToTable[transition.source.tokenID] = {}

            if transition.source.tokenID not in actionTable:
                actionTable[transition.source.tokenID] = {}

            if transition.symbol.id in nonTerminals:
                if goToTable[transition.source.tokenID].get(transition.symbol.id) == None:
                    goToTable[transition.source.tokenID][transition.symbol.id] = transition.target.tokenID
                else:
                    raise Exception("Grammar is not SLR(1)")
                
            if transition.symbol.id in terminals:
                if actionTable[transition.source.tokenID].get(transition.symbol.id) == None:
                    actionTable[transition.source.tokenID][transition.symbol.id] = "S" + str(transition.target.tokenID)
                else:
                    raise Exception("Grammar is not SLR(1)")
                
        for i in range(len(this.states)):
            state = this.states[i]

            for production in state.id:
                if production.split('->')[0].strip() == this.initial.id[0].split('->')[0].strip():
                    if actionTable[state.tokenID].get("$") == None:
                        actionTable[state.tokenID]["$"] = "ACCEPT"
                    else:
                        raise Exception("Grammar is not SLR(1)")
                
                if production == state.id[-1] and production.endswith("."):
                    for symbol in this.follow(production.split('->')[0].strip()):
                        if symbol in terminals:
                            if actionTable[state.tokenID].get(symbol) == None:
                                actionTable[state.tokenID][symbol] = "R" + str(list(this.productions.keys()).index(production.split('->')[0].strip()))
                            else:
                                raise Exception("Grammar is not SLR(1)")
                            
        this.goToTable = goToTable
        this.actionTable = actionTable
        this.terminals = terminals
        this.nonTerminals = nonTerminals


    def print(this):
        # Print the goto table
        print("\nGOTO TABLE:")
        print("State\t", end="")
        for symbol in this.nonTerminals:
            print(symbol + "\t", end="")
        print()

        for stateID, state in this.goToTable.items():
            print(str(stateID) + "\t", end="")
            for symbol in this.nonTerminals:
                if symbol in state:
                    print(str(state[symbol]) + "\t", end="")
                else:
                    print("\t", end="")
            print()

        # Print the action table
        print("\nACTION TABLE:")
        print("State\t", end="")
        for symbol in this.terminals:
            print(symbol + "\t", end="")
        print()

        for stateID, state in this.actionTable.items():
            print(str(stateID) + "\t", end="")
            for symbol in this.terminals:
                if symbol in state:
                    print(str(state[symbol]) + "\t", end="")
                else:
                    print("\t", end="")
            print()
        
    def simulate(this, word, printResult = True):
        """ 
        PARAMETERS:
            word: word to be simulated
            printResult: if true, prints the result of the simulation
        RETURNS:
            True if the word is accepted, False otherwise
        """  

        stack = [1]
        word = word.split(' ')
        word.append("$")
        index = 0
        result = True

        while True:
            state = stack[-1]
            symbol = word[index]

            if this.actionTable[state].get(symbol) == None:
                result = False
                break

            action = this.actionTable[state][symbol]

            if action == "ACCEPT":
                break

            if action[0] == "S":
                stack.append(symbol)
                stack.append(int(action[1:]))
                index += 1
            elif action[0] == "R":
                production = this.productions[int(action[1:])]
                left = production.split('->')[0].strip()
                right = production.split('->')[1].strip().split(' ')

                for i in range(len(right) * 2):
                    stack.pop()

                stack.append(left)
                stack.append(this.goToTable[stack[-2]][stack[-1]])
            else:
                result = False
                break

        if printResult:
            if result:
                print("\nWord accepted")
            else:
                print("\nWord not accepted")

        return result