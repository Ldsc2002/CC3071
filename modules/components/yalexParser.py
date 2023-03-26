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
                    start = rule.index("|")
                    end = rule.index("{")

                    ruleName = rule[start + 1:end].strip()

                rules[ruleName] = returnVal
            else:
                rules[rule.strip()] = ""

        print("here")
