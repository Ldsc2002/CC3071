from modules.proto.automata import *
from modules.components.NFA import *
from modules.components.regexTree import *

class DFA(Automata):
    def __init__(this, regex, filename):
        if isinstance(regex, RegexTree):
            this.filename = "DFA_Direct_(" + filename + ")"
            this.directConstruction(regex.tree)

        elif isinstance(regex, NFA):
            this.states = regex.states
            this.final = regex.final
            this.symbols = regex.symbols
            this.initial = regex.initial
            this.transitions = regex.transitions

            this.filename = "DFA_Subset_(" + filename + ")"
            this.subsetConstruction()
            
        else:
            raise Exception('Invalid parameter for DFA constructor')

    def directConstruction(this, node):
        operators = [".", "|", "*", "?", "+"]

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
                
        def getFollowPos(node, allNodes, parent = None, lastValid = None):
            if lastValid is None:
                lastValid = Set()

            if parent:
                parent = getParent(parent, allNodes)
            else:
                parent = getParent(node, allNodes)

            if parent:
                if parent.value == '.':
                    lastPosLeft = getLastPos(parent.left)
                    firstPosRight = getFirstPos(parent.right)

                    if node.stateDFA in lastPosLeft:
                        for state in firstPosRight:
                            lastValid.add(state)

                        return getFollowPos(node, allNodes, parent, lastValid)
                    else:
                        return getFollowPos(node, allNodes, parent, lastValid)
                    
                elif parent.value == '*':
                    tempLastPos = getLastPos(parent)
                    tempFirstPos = getFirstPos(parent)

                    if node.stateDFA in tempLastPos:
                        for state in tempFirstPos:
                            lastValid.add(state)
                            
                        return getFollowPos(node, allNodes, parent, lastValid)
                    else:
                        return getFollowPos(node, allNodes, parent, lastValid)
                
                else:
                    return getFollowPos(node, allNodes, parent, lastValid)
            
            elif len(lastValid) > 0:
                return lastValid.sorted()
                    
            return []

        def getParent(node, allNodes):
            for testParent in allNodes:
                if testParent.left == node or testParent.right == node:
                    return testParent
                
            return None

        def buildFollowPosTable():
            stateCount = 1
            allNodes = getAllNodes(node)
            
            for nodeTest in allNodes:
                if nodeTest.value not in operators:
                    nodeTest.stateDFA = stateCount
                    stateCount += 1     

            followPosTable = {}
            allNodes = getAllNodes(node)
            finalState = -1

            for nodeTest in allNodes:
                if nodeTest.value == "#":
                    finalState = nodeTest.stateDFA

                if nodeTest.value not in operators:
                    followPosTable[nodeTest.stateDFA] = getFollowPos(nodeTest, allNodes.copy())

            return followPosTable, finalState
        
        def buildTransitionTable(followPosTable, finalState):
            allNodes = getAllNodes(node)
            
            symbols = Set()
            
            for nodeTest in allNodes:
                if nodeTest.value not in operators and nodeTest.value != "#":
                    symbols.add(nodeTest.value)

            finals = Set()
            stack = []
            visited = []
            transitionTable = {}

            root = getFirstPos(node)
            stateDict = {str(root): 0}

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
                                    if followPos not in destState:
                                        destState.append(followPos)
                                    
                                    transitionTable[str(root)][symbol].add(followPos)

                    transitionTable[str(root)][symbol] = str(transitionTable[str(root)][symbol].elements)

                    if len(destState) > 0:
                        if str(destState) not in transitionTable and destState not in visited:
                            stack.append(destState)
                            visited.append(destState)

                        if str(destState) not in stateDict:
                            stateDict[str(destState)] = len(stateDict)

                    if finalState in root:
                        finals.add(str(root))

                if len(stack) > 0:
                    root = stack.pop(0)
                else:
                    break
            
            return transitionTable, stateDict, finals
        
        def buildTransitions(transitionTable, stateDict, finals):
            transitions = {}
            finalStates = Set()

            for state in transitionTable:
                if state in finals:
                    finalStates.add(stateDict[state])

                transitions[stateDict[state]] = {}

                for symbol in transitionTable[state]:
                    if transitionTable[state][symbol] != "[]":
                        transitions[stateDict[state]][symbol] = stateDict[transitionTable[state][symbol]] 

            return transitions, finalStates
        
        def buildAutomata(transitions, finalStates):
            this.states = Set()
            this.symbols = Set()
            this.transitions = Set()
            this.final = Set()
            skips = Set()

            for transition in transitions:
                if transition in skips:
                    continue

                state = State(transition)
                this.states.add(state)

                if transition in finalStates:
                    this.final.add(state)

                if transition == 0:
                    this.initial = state

                for symbol in transitions[transition]:
                    if symbol.startswith("'#") and transitions[transition][symbol] in finalStates:
                        skips.add(transitions[transition][symbol])
                        this.final.add(state)
                        continue

                    this.symbols.add(symbol)
                    this.transitions.add(Transition(state, State(transitions[transition][symbol]), Symbol(symbol)))
        
        followPosTable, finalState = buildFollowPosTable()
        transitionTable, stateDict, finals = buildTransitionTable(followPosTable, finalState)
        
        transitions, finalStates = buildTransitions(transitionTable, stateDict, finals)
        buildAutomata(transitions, finalStates)


    def subsetConstruction(this):
        def eClosure(state):
            stack = [state]
            closure = Set()
            visited = Set()
            closure.add(state.id)

            while len(stack) > 0:
                state = stack.pop()
                
                for transition in this.transitions:
                    if transition.source.id == state.id and transition.symbol.cid == "ε":
                        if transition.target.id not in visited:
                            visited.add(transition.target.id)
                            stack.append(transition.target)
 
                        closure.add(transition.target.id)

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
        
        def buildSubsets():
            subsets = {}
            stack = [eClosure(this.states.elements.copy()[0])]

            while len(stack) > 0:                            
                initial = stack.pop(0)
                
                if initial not in subsets:
                    subsets[initial] = {}
                    for symbol in this.symbols:
                        subsets[initial][symbol] = Set()

                for testState in initial:
                    for transition in this.transitions:
                        if transition.source.id == testState and transition.symbol.cid != "ε":
                            possibleDest = eClosure(transition.target)

                            subsets[initial][transition.symbol.id].union(possibleDest)

                for symbol in this.symbols:
                    statesCopy = (subsets[initial][symbol]).copy()
                    statesCopy.sort()

                    if len(statesCopy) > 0:                
                        _, exists = setExists(statesCopy, subsets, True)
                        if not exists:
                            subsets[statesCopy] = {}
                            stack.append(statesCopy)

                            for symbol in this.symbols:
                                subsets[statesCopy][symbol] = Set()

            return subsets
        
        def getNewStates(subsets):
            newStates = {}
            stateKeys = {}
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

            return newStates, stateKeys, finals
        
        def buildTransitionTable(newStates, stateKeys):
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
            
            return newStates
            
        def buildTransitions(newStates, finals):
            this.final = Set()
            this.states = Set()
            this.transitions = Set()

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

        if "ε" in this.symbols:
            this.symbols.remove("ε")

        subsets = buildSubsets()
        newStates, stateKeys, finals = getNewStates(subsets)
        transitionTable = buildTransitionTable(newStates, stateKeys)
        buildTransitions(transitionTable, finals)