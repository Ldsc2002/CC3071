class YalexParser():
    def __init__(this, file):
        this.regex = this.parse(file)

    def parse(this, file):
        letArray = []
        rulesArray = []

        readingRule = False

        with open(file, "r") as file:
            lines = file.read().splitlines()

            for line in lines:
                newLine = line.strip()

                if newLine == "" or newLine[0] == "#":
                    continue

                if "(*" in newLine and "*)" in newLine:
                    first = newLine.index("(*")
                    last = newLine.index("*)")

                    newLine = newLine[:first] + newLine[last + 2:]
                    newLine = newLine.strip()

                if newLine != "": 
                    if readingRule:
                        rulesArray.append(newLine)
                    else:
                        if newLine.startswith("let"):
                            letArray.append(newLine)

                        if newLine.startswith("rule"):
                            readingRule = True
        
        lets = {}
        for let in letArray:
            let = let.replace("let ", "")
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
                        
                letVal = tempArray

            lets[let[0].strip()] = letVal

        rules = {}
        for rule in rulesArray:
            if "return" in rule:
                start = rule.index("{")
                end = rule.index("}")
                returnVal = rule[start + 1:end].strip() + rule[end + 1:].strip()

                if "'" in rule:
                    start = rule.index("'")
                    end = rule.index("'", start + 1)

                    ruleName = rule[start + 1:end].strip()
                else:
                    start = 0

                    if "|" in rule:
                        start = rule.index("|")
                    
                    end = rule.index("{")

                    ruleName = rule[start + 1:end].strip()

                rules[ruleName] = returnVal
            else:
                rules[rule.strip()] = ""

        stack = []
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

                    lets[key] = newVals

            else:   
                stack.append(key)

        regexStack = []
        for key in stack:
            operators = ["+", "*", "?", "|", "(", ")", ".", "[", "]", "-"]
            val = lets[key]

            x = 0
            while (True):
                if val[x] in operators:
                    regexStack.append(val[x])
                    x += 1

                else:
                    tempStr = ""
                    while not val[x] in operators:
                        tempStr += val[x]

                        x += 1

                        if x >= len(val):
                            break

                    regexStack.append(tempStr)

                if x >= len(val):
                    break

        regex = ""
        for val in regexStack:
            if val in lets:
                regex += "("

                for x in range(len(lets[val])):
                    if isinstance(lets[val][x], int):
                        regex += "'" + str(lets[val][x]) + "'"
                    else:
                        regex += lets[val][x]

                    if x != len(lets[val]) - 1:
                        regex += "|"

                regex += ")"
                
            else:
                regex += val
                
                if val != regexStack[-1] and val != ")" and val != "(" and val != "|":
                    regex += "|"

        return regex