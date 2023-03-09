from modules.proto.automata import *
from modules.components.NFA import *
from modules.components.regexTree import *

class DFA(Automata):
    def __init__(this, regex, filename):
        if isinstance(regex, RegexTree):
            this.filename = "DFA_Direct_(" + filename + ")"
            this.directConstruction(regex.tree)

        elif isinstance(regex, NFA):
            super().__init__()

            this.filename = "DFA_Subset_(" + filename + ")"
            this.subsetConstruction()
            
        else:
            raise Exception('Invalid parameter for DFA constructor')

    def directConstruction(this, node):
        def getAllNodes(node, allNodes = None):
            if allNodes is None:
                allNodes = []

            if node not in allNodes:
                allNodes.append(node)

            if node.left is not None:
                getAllNodes(node.left, allNodes)

            if node.right is not None:
                getAllNodes(node.right, allNodes)

            return allNodes 

        def isNullable(node):
            if node.left is None and node.right is None:
                return False

            elif node.value == '|':
                return isNullable(node.left) or isNullable(node.right)

            elif node.value == '*':
                return True

            elif node.value == '.':
                return isNullable(node.left) and isNullable(node.right)  
            
            elif node.value == "?":
                return True
            
            elif node.value == "+":
                return isNullable(node.left)
            
        def getFirstPos(node):
            if node.left is None and node.right is None:
                return [node.stateDFA]

            elif node.value == '|':
                return getFirstPos(node.left) + getFirstPos(node.right)

            elif node.value == '*':
                return getFirstPos(node.left)

            elif node.value == '.':
                if isNullable(node.left):
                    return getFirstPos(node.left) + getFirstPos(node.right)
                else:
                    return getFirstPos(node.left)
                
            elif node.value == "?":
                return getFirstPos(node.left)
            
            elif node.value == "+":
                return getFirstPos(node.left)
                
        def getLastPos(node):
            if node.left is None and node.right is None:
                return [node.stateDFA]

            elif node.value == '|':
                return getLastPos(node.left) + getLastPos(node.right)

            elif node.value == '*':
                return getLastPos(node.left)

            elif node.value == '.':
                if isNullable(node.right):
                    return getLastPos(node.left) + getLastPos(node.right)
                else:
                    return getLastPos(node.right)
                
            elif node.value == "?":
                return getLastPos(node.left)
            
            elif node.value == "+":
                return getLastPos(node.left)
                
        def getFollowPos(node, allNodes):
            parent = getParent(node, allNodes)

            if parent:
                if parent.value == '.' or parent.value == "|" or parent.value == "?":
                    if (node == parent.right and parent.value == '.') or (parent.value == "|") or (parent.value == "?"):
                        parent = getParent(parent, allNodes)
                        
                    if parent:
                        firstPosRight = getFirstPos(parent.right)
                        lastPosLeft = getLastPos(parent.left)

                        tempFollowPos = Set()

                        for posLeft in lastPosLeft:
                            tempItem = getFollowPos(posLeft, allNodes)

                            for item in tempItem:
                                tempFollowPos.add(item)
                            
                        for posRight in firstPosRight:
                            tempFollowPos.add(posRight)
                        
                        return tempFollowPos
                    
                elif parent.value == '*' or parent.value == "+":
                    firstPostTemp = getFirstPos(parent.left)
                    lastPosTemp = getLastPos(parent.left)

                    tempFollowPos = Set()

                    for posLast in lastPosTemp:
                        tempItem = getFollowPos(posLast, allNodes)

                        for item in tempItem:
                            tempFollowPos.add(item)

                    for posFirst in firstPostTemp:
                        tempFollowPos.add(posFirst)


                    parentFollowPos = getFollowPos(parent, allNodes)

                    for item in parentFollowPos:
                        tempFollowPos.add(item)
                        
                    return tempFollowPos
                    
            return Set()

        def getParent(node, allNodes):
            for testParent in allNodes:
                if testParent.left == node or testParent.right == node:
                    return testParent
                
            return None

        operators = [".", "|", "*", "?", "+"]
        followPosTable = {}
        symbols = Set()
        finalState = -1

        allNodes = getAllNodes(node)
        stateCount = 1
        for nodeTest in allNodes:
            if nodeTest.value not in operators:
                nodeTest.stateDFA = stateCount
                stateCount += 1

                if nodeTest.value != "#":
                    symbols.add(nodeTest.value)
        
        for nodeTest in allNodes:
            if nodeTest.value == "#":
                finalState = nodeTest.stateDFA

            if nodeTest.value not in operators:
                followPosTable[nodeTest.stateDFA] = getFollowPos(nodeTest, allNodes.copy())

        root = getFirstPos(node)
        transitionTable = {}
        stateDict = {str(root): 0}
        finals = Set()
        stack = []

        while True:
            transitionTable[str(root)] = {}

            for symbol in symbols:
                destState = []
                transitionTable[str(root)][symbol] = Set()

                for state in allNodes:
                    for stateRoot in root:
                        if state.stateDFA == stateRoot and state.value == symbol:
                            stateFollowPos = followPosTable[state.stateDFA]

                            for followPos in stateFollowPos:
                                destState.append(followPos)
                                transitionTable[str(root)][symbol].add(followPos)

                transitionTable[str(root)][symbol] = str(transitionTable[str(root)][symbol].elements)

                if str(destState) not in transitionTable and len(destState) > 0:
                    stateDict[str(destState)] = len(stateDict)
                    stack.append(destState)

                if finalState in root:
                    finals.add(str(root))

            if len(stack) > 0:
                root = stack.pop(0)
            else:
                break

        transitions = {}
        finalStates = Set()

        for state in transitionTable:
            if state in finals:
                finalStates.add(stateDict[state])

            transitions[stateDict[state]] = {}

            for symbol in transitionTable[state]:
                if transitionTable[state][symbol] != "[]":
                    transitions[stateDict[state]][symbol] = stateDict[transitionTable[state][symbol]] 

        this.states = Set()
        this.symbols = Set()
        this.transitions = Set()
        this.final = Set()

        for transition in transitions:
            state = State(transition)
            this.states.add(state)

            if transition in finalStates:
                this.final.add(state)

            if transition == 0:
                this.initial = state

            for symbol in transitions[transition]:
                this.symbols.add(symbol)
                this.transitions.add(Transition(state, State(transitions[transition][symbol]), Symbol(symbol)))

    def subsetConstruction(this):
        def eClosure(state, past = None):
            if past == None:
                past = []

            if state.id in past:
                return Set()
                
            past.append(state.id)
            closure = Set()
            closure.add(state.id)

            for transition in this.transitions:
                if transition.source.id == state.id and transition.symbol.id == "ε":
                    closure.union(eClosure(transition.target, past))

            return closure
        
        def setExists(newSet, states, testExact = False):
            candidate = None

            for test in list(states.keys()):
                if testExact and len(test.elements) != len(newSet.elements):
                    continue

                for state in newSet:
                    if state not in test.elements:
                        candidate = None
                        break

                    else:
                        candidate = test
                
                if candidate:
                    return candidate, True

                    
            return newSet, False
        
        if "ε" in this.symbols:
            this.symbols.remove("ε")

        subsets = {}

        stack = this.states.elements.copy()

        while len(stack) > 0:
            state = stack.pop(0)

            initial = eClosure(state)
            initial.sort()
                        
            initial, exists = setExists(initial, subsets)

            if not exists:
                subsets[initial] = {}
                for value in initial:
                    stack.append(State(value))

                for symbol in this.symbols:
                    subsets[initial][symbol] = Set()

            for testState in initial:
                for transition in this.transitions:
                    if transition.source.id == testState and transition.symbol.id != "ε":
                        possibleDest = eClosure(transition.target)

                        subsets[initial][transition.symbol.id].union(possibleDest)

            for symbol in this.symbols:
                statesCopy = (subsets[initial][symbol]).copy()

                if len(statesCopy) > 0:                
                    _, exists = setExists(statesCopy, subsets, True)
                    if not exists:
                        subsets[statesCopy] = {}

                        for symbol in this.symbols:
                            subsets[statesCopy][symbol] = Set()

        newStates = {}
        stateKeys = {}

        this.transitions = Set()
        this.states = Set()
        finals = Set()

        for x in range(len(subsets)):
            newStates[x] = subsets[list(subsets.keys())[x]]

            arrayTest = list(subsets.keys())[x]

            for state in arrayTest:
                for final in this.final:
                    if state == final.id:
                        finals.add(x)
                        break

            stateKeysValue = ""
            keysList = list(subsets.keys())[x]
            keysList.sort()

            for y in keysList:
                stateKeysValue += y + " "
            
            stateKeys[stateKeysValue] = x

        for subset in newStates:
            for symbol in newStates[subset]:
                if newStates[subset][symbol].len() > 0:
                    stateKeysValue = ""

                    keysList = newStates[subset][symbol]
                    
                    keysList.sort()
                    for x in keysList:
                        stateKeysValue += x + " "
                    
                    newStates[subset][symbol] = stateKeys[stateKeysValue]
                
                else:
                    newStates[subset][symbol] = ""

        this.final = Set()
        for subset in newStates:
            state = State(subset)
            this.states.add(state)

            if subset == 0:
                this.initial = state

            if subset in finals:
                this.final.add(state)

            for symbol in newStates[subset]:
                if newStates[subset][symbol] != "":
                    this.transitions.add(Transition(State(subset), State(newStates[subset][symbol]), Symbol(symbol)))
        
