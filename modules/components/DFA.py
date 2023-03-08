from modules.proto.automata import *
from modules.components.NFA import *
from modules.components.regexTree import *

class DFA(Automata):
    def __init__(this, regex, filename):
        super().__init__()

        if isinstance(regex, RegexTree):
            this.tree = regex
            this.filename = "DFA_Direct_(" + filename + ")"
            this.directConstruction(regex.tree)

        elif isinstance(regex, NFA):
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

            if node.right is not None:
                getAllNodes(node.right, allNodes)

            if node.left is not None:
                getAllNodes(node.left, allNodes)

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
            
        def getFirstPos(node):
            if node.left is None and node.right is None:
                return [node]

            elif node.value == '|':
                return getFirstPos(node.left) + getFirstPos(node.right)

            elif node.value == '*':
                return getFirstPos(node.left)

            elif node.value == '.':
                if isNullable(node.left):
                    return getFirstPos(node.left) + getFirstPos(node.right)
                else:
                    return getFirstPos(node.left)
                
        def getLastPos(node):
            if node.left is None and node.right is None:
                return [node]

            elif node.value == '|':
                return getLastPos(node.left) + getLastPos(node.right)

            elif node.value == '*':
                return getLastPos(node.left)

            elif node.value == '.':
                if isNullable(node.right):
                    return getLastPos(node.left) + getLastPos(node.right)
                else:
                    return getLastPos(node.right)
                
        def followPos(node):
            if node.left is None and node.right is None:
                return {}

            elif node.value == '|':
                return {}

            elif node.value == '*':
                return {}

            elif node.value == '.':
                followPos = {}

                for leftNode in getLastPos(node.left):
                    followPos[leftNode] = getFirstPos(node.right)

                return followPos

        allNodes = getAllNodes(node)
        nodeFollowPos = {}
        nodeDict = {}
        followPosTable = {}
        finals = []

        for node in allNodes:
            nodeFollowPos[node] = followPos(node)

            if node not in nodeDict:
                nodeDict[node] = len(nodeDict)

        for node in allNodes:
            if node.value == "#":
                finals.append(nodeDict[node])

            followPosTable[nodeDict[node]] = {}

            for symbol in nodeFollowPos[node]:
                followPosTable[nodeDict[node]][symbol.value] = []

                for target in nodeFollowPos[node][symbol]:
                    followPosTable[nodeDict[node]][symbol.value].append(nodeDict[target])
        
        possibleStates = []
        for node in followPosTable:
            if len(followPosTable[node]) > 0:
                possibleStates.append(node)

            for symbol in followPosTable[node]:
                for target in followPosTable[node][symbol]:
                    if target not in possibleStates:
                        possibleStates.append(target)
        
        newFollowPosTable = {}
        for node in followPosTable:
            if node in possibleStates:
                newFollowPosTable[node] = followPosTable[node]

        followPosTable = newFollowPosTable

        for node in followPosTable:
            state = State(node)
            
            if node == 0:
                this.initial = state
            
            if node in finals:
                this.final.add(state)

            this.states.add(state)

            for symbol in followPosTable[node]:
                this.symbols.add(symbol)

                for target in followPosTable[node][symbol]:
                    this.transitions.add(Transition(state, State(target), Symbol(symbol)))
            
    def subsetConstruction(this):
        this.symbols = this.symbols
        
        if "ε" in this.symbols:
            this.symbols.remove("ε")

        subsets = {}

        stack = this.states.elements.copy()

        while len(stack) > 0:
            state = stack.pop(0)

            initial = this.eClosure(state)
            initial.sort()
                        
            initial, exists = this.setExists(initial, subsets)

            if not exists:
                subsets[initial] = {}
                for value in initial:
                    stack.append(State(value))

                for symbol in this.symbols:
                    subsets[initial][symbol] = Set()

            for testState in initial:
                for transition in this.transitions:
                    if transition.source.id == testState and transition.symbol.id != "ε":
                        possibleDest = this.eClosure(transition.target)

                        subsets[initial][transition.symbol.id].union(possibleDest)

            for symbol in this.symbols:
                statesCopy = (subsets[initial][symbol]).copy()

                if len(statesCopy) > 0:                
                    _, exists = this.setExists(statesCopy, subsets, True)
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
        
    def eClosure(this, state, past = None):
        if past == None:
            past = []

        if state.id in past:
            return Set()
            
        past.append(state.id)
        closure = Set()
        closure.add(state.id)

        for transition in this.transitions:
            if transition.source.id == state.id and transition.symbol.id == "ε":
                closure.union(this.eClosure(transition.target, past))

        return closure
    
    def setExists(this, newSet, states, testExact = False):
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