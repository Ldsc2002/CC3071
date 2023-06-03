class YalexParser():
    def __init__(this, file):
        this.alphabet = []
        this.regex = this.parse(file)

    def readFile(this, file):
        letArray = []
        rulesArray = []

        readingRule = False
        with open(file, "r") as file:
            skip = 0
            lines = file.read().splitlines()

            for line in lines:
                if skip > 0:
                    skip -= 1
                    continue

                newLine = line.strip()
                newLine = newLine.replace('"', "'")

                # Ignore empty lines and comments
                if newLine == "" or newLine[0] == "#":
                    continue

                # Check for unclosed comments
                if "(*" in newLine and "*)" not in newLine:
                    if "'(*" in newLine or '"(*' in newLine:
                        continue
                    raise Exception("Missing closing comment tag: " + newLine)
                elif "*)" in newLine and "(*" not in newLine:
                    if "'*)" in newLine or '"*)' in newLine:
                        continue
                    raise Exception("Missing opening comment tag: " + newLine)

                # Remove comments
                if "(*" in newLine and "*)" in newLine:
                    first = newLine.index("(*")
                    last = newLine.index("*)")

                    newLine = newLine[:first] + newLine[last + 2:]
                    newLine = newLine.strip()

                if "{" in newLine and "}" not in newLine:
                    currentIndex = lines.index(line)
                    while "}" not in newLine:
                        newLine += " " + lines[currentIndex + 1]
                        currentIndex += 1
                        skip += 1

                # If line is not empty, validate it
                if newLine != "": 
                    if readingRule and (
                        newLine.startswith("(") or
                        newLine.startswith("{")):
                        readingRule = False

                    # Check for invalid rule syntax
                    if len(rulesArray) > 0 and "|" not in newLine and readingRule:
                        raise Exception("Missing operator '|' in rule: " + newLine)
                    elif len(rulesArray) == 0 and "|" in newLine and readingRule:
                        raise Exception("Extra operator '|' in rule: " + newLine)
                    
                    if newLine.count("'") % 2 != 0:
                        raise Exception("Missing quote in rule: " + newLine)
                    elif newLine.count('"') % 2 != 0:
                        raise Exception("Missing quote in rule: " + newLine)

                    # Add line to the array
                    if readingRule:
                        rulesArray.append(newLine)
                    else:
                        if newLine.startswith("let"):
                            if newLine.split(" ")[0] != "let":
                                newLine = "let " + newLine.split(" ", 1)[1]
                            letArray.append(newLine)

                        if newLine.startswith("rule"):
                            readingRule = True

        return letArray, rulesArray
    
    def validateYalex(this, rules, lets):
        # Check for invalid rule names
        for key in rules:
            if len(key) > 2 and key not in lets:
                # Ignore rule names with quotes
                print(key.count("'"))
                if key.count("'") == 2 or key.count('"') == 2:
                    continue

                raise Exception("Invalid rule name: " + key)
            
    def parse(this, file):
        operators = ["+", "*", "?", "|", "(", ")", ".", "[", "]"]

        letArray, rulesArray = this.readFile(file)
        
        lets = {}
        for let in letArray:
            let = let.replace("let ", "")
            
            # TODO find a better way to do this
            prev = ""
            newLet = ""
            for c in let:
                if c == " " and (prev != "'"):
                    continue
                
                newLet += c
                prev = c
            let = newLet

            let = let.strip()
            let = let.split("=")

            letVal = let[1].strip()

            if letVal.startswith("[") and letVal.endswith("]"):
                if "-" in letVal:
                    letVal = letVal[1:-1]

                    tempArray = []
                    lastIndex = 0
                    count = letVal.count("-")

                    for x in range(count):
                        index = letVal.index("-", lastIndex)

                        startA = letVal.index("'", lastIndex)
                        endA = letVal.index("'", startA + 1)

                        startB = letVal.index("'", index)
                        endB = letVal.index("'", startB + 1)

                        valA = letVal[startA + 1:endA]
                        valB = letVal[startB + 1:endB]

                        tempArray.append(valA + "-" + valB)

                        lastIndex = endB + 1

                else:
                    testCount = letVal.count("'")
                    if testCount == 0:
                        testCount = letVal.count('"')

                    if testCount > 2:
                        letVal = letVal[1:-1]

                        tempArray = []
                        currentIndex = -1
                        for x in range(len(letVal)):
                            char = letVal[x]

                            if currentIndex > x:
                                continue
                            elif currentIndex == x:
                                currentIndex = -1

                            if char == "'":
                                if currentIndex == -1:
                                    currentIndex = x
                            
                            elif currentIndex != -1:
                                start = currentIndex + 1
                                end = letVal.index("'", start)
                                
                                tempArray.append(letVal[start:end])
                                currentIndex = end + 1
                    
                    else:
                        letVal = letVal[1:-1]
                        
                        if "\\" in letVal:
                            letVal = letVal[1:-1]

                            tempArray = []
                            for char in letVal:
                                if char != "\\":
                                    tempArray.append("\\" + char)

                        else:
                            tempArray = []
                            for char in letVal:
                                if char != "'" and char != '"':
                                    tempArray.append(char)
                        
                letVal = tempArray

            lets[let[0].strip()] = letVal

        rules = {}
        for rule in rulesArray:
            rule = rule.replace("rule ", "")
            if "return" in rule:
                start = rule.index("{")
                end = rule.index("}")
                returnVal = rule[start + 1:end].strip() + rule[end + 1:].strip()

                if "'" in rule.split("{")[0]:
                    start = rule.index("'")
                    end = rule.index("'", start + 1)

                    ruleName = rule[start + 1:end].strip()
                else:
                    start = 0

                    if "|" in rule:
                        start = rule.index("|") + 1
                    
                    end = rule.index("{")

                    ruleName = rule[start:end].strip()

                rules[ruleName] = returnVal
            else:
                rules[rule.strip()] = ""

        this.validateYalex(rules, lets)

        alphabet = []
        for key in lets:
            if isinstance(lets[key], list):
                newVals = []
                case = 0
                
                for val in lets[key]:
                    if isinstance(val, str) and "-" in val:
                        case = 1
                        break
                    elif isinstance(val, str) and "\\" in val:
                        case = 2
                        break

                if case == 1:
                    for val in lets[key]:
                        start = ord(val[0])
                        end = ord(val[2])

                        for x in range(start, end + 1):
                            alphabet.append(chr(x))
                            newVals.append(chr(x))
                    
                    lets[key] = newVals

                elif case == 2:
                    newVals = []
                    for val in lets[key]:
                        if val.startswith("\\"):
                            val = val.replace("\\", "")

                            if val == "n":
                                newVals.append(ord("\n"))
                            elif val == "t":
                                newVals.append(ord("\t"))
                            elif val == "r":
                                newVals.append(ord("\r"))
                            elif val == "f":
                                newVals.append(ord("\f"))
                            elif val == "s":
                                newVals.append(ord(" "))
                            else: 
                                raise Exception("Invalid escape character: " + val)
                        else:
                            newVals.append(ord(val))

                    for val in newVals:
                        alphabet.append(val)

                    lets[key] = newVals

                else:
                    for val in lets[key]:
                        alphabet.append(val)
                        
        regexStack = []
        for key in rules:
            regexStack.append("(")

            if key in lets:
                val = lets[key]

                x = 0
                while (True):
                    if val[x] in operators:
                        if val[x] == "[":
                            x += 1                            
                            regexStack.append("(")

                            while not val[x] == "]":
                                if val[x] != "'":
                                    if val[x] in operators or val[x] == "-":
                                        regexStack.append("'" + str(ord(val[x])) + "'")
                                        alphabet.append(ord(val[x]))
                                    else:
                                        regexStack.append(val[x])
                                        alphabet.append(val[x])

                                    regexStack.append("|")
                                
                                x += 1

                            regexStack.pop() # Remove last "|"
                            regexStack.append(")")

                        elif val[x] in ["(", ")" , "|" , "*"]:
                            regexStack.append(val[x])

                        x += 1

                    else:
                        tempStr = ""
                        while not val[x] in operators:
                            tempStr += val[x]

                            x += 1

                            if x >= len(val):
                                break

                        if tempStr in lets and isinstance(lets[tempStr], str):
                            tempOperators = ""
                            newTempStr = ""
                            
                            for char in lets[tempStr]:
                                if char in operators:
                                    tempOperators += char
                                else:
                                    newTempStr += char

                            if newTempStr in lets:
                                regexStack.append(newTempStr)

                                for char in tempOperators:
                                    regexStack.append(char)
                                    regexStack.append("|")

                                regexStack.pop() # Remove last "|"

                            else:
                                regexStack.append(tempStr)

                        else:
                            if "'" in tempStr:
                                tempStr = tempStr.replace("'", "")
                            
                            if len(tempStr) > 0:
                                if len(tempStr) == 1:
                                    alphabet.append(tempStr)

                                regexStack.append(tempStr)

                    if x >= len(val):
                        break

                if key != list(rules.keys())[-1]:
                    regexStack.append("|")
            
            else:
                for char in key:
                    regexStack.append("'" + str(ord(char)) + "'")
                    alphabet.append(ord(char)) 
                    regexStack.append("|")

                regexStack.pop() # Remove last "|"

                if key != list(rules.keys())[-1]:
                    regexStack.append("|")

            if regexStack[-1] == "|":
                regexStack.pop()

            regexStack.append(".")
            regexStack.append("'#" + key + "')")
            regexStack.append("|")          

        if regexStack[-1] == "|": 
            regexStack.pop()

        this.alphabet = alphabet

        regex = ""
        for val in regexStack:
            if val in lets:
                regex += "("

                for x in range(len(lets[val])):
                    if (len(regex) > 0 and 
                        regex[-1] != "(" and 
                        regex[-1] != ")" and 
                        lets[val][x] != "(" and
                        lets[val][x] != ")"):
                        
                        regex = regex + "|"

                    if isinstance(lets[val][x], int):
                        regex += "'" + str(lets[val][x]) + "'"
                    else:
                        regex += lets[val][x]
                        
                        if (lets[val][x] not in this.alphabet and
                            lets[val][x] != "(" and
                            lets[val][x] != ")" and
                            lets[val][x] not in operators):

                            this.alphabet.append(lets[val][x])

                regex += ")"
                
            else:
                regex += val

        this.tokens = rules

        return regex
    
    def simulate(this, file, dfa, tokens):
        def executeToken(token):
            for t in tokens:
                if t == token:
                    return tokens[t].replace("return ", "")
        
        print("\nSimulating input file: " + file)
        data = open(file, 'r').read()

        statesDict = {}
        for state in dfa.states:
            statesDict[state.id] = state.tokenID

        finalsArray = []
        for state in dfa.final:
            finalsArray.append(state.id)

        transitionsDict = {}
        for transition in dfa.transitions:
            if transition.source.id not in transitionsDict:
                transitionsDict[transition.source.id] = {}
            transitionsDict[transition.source.id][transition.symbol.cid] = transition.target.id

        current = 0
        valid = ''
        result = []

        for i in range(len(data)):
            symbol = data[i]

            if symbol == ")":
                print('Valid token found: ' + valid)
            
            if current not in transitionsDict or (symbol not in transitionsDict[current] and ("'" + str(ord(symbol)) + "'") not in transitionsDict[current]):
                if len(valid) > 0:
                    print('Valid token found: ' + valid)
                    result.append(executeToken(statesDict[current]))
                current = 0
                valid = ''
                
                if i == len(data) - 1:
                    valid += symbol
                    print('Valid token found: ' + valid)

                    if symbol in transitionsDict[current] or ("'" + str(ord(symbol)) + "'") in transitionsDict[current]:    
                        if symbol in transitionsDict[current]:
                            current = transitionsDict[current][symbol]
                        else:
                            current = transitionsDict[current]["'" + str(ord(symbol)) + "'"]
                        
                        result.append(executeToken(statesDict[current]))
            else:
                valid += symbol

                if symbol in transitionsDict[current]:
                    current = transitionsDict[current][symbol]
                else:
                    current = transitionsDict[current]["'" + str(ord(symbol)) + "'"]

                if i == len(data) - 1:
                    print('Valid token found: ' + valid)
                    result.append(executeToken(statesDict[current]))

        return result
