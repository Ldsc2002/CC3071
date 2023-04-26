import os
from modules.components.DFA import *
from modules.common.utils import isDebugging

class CodeGen():
    def __init__(this, DFA, tokens):
        this.DFA = DFA
        this.tokens = tokens
        this.isDebugging = isDebugging()
        print("\nCreating Python code...")
        this.compile()

    def compile(this):
        filename = "out/" + "scanner.py"
       
        if os.path.isfile(filename):
            os.remove(filename)       
        else:
            with open(filename, "w") as file:
                file.write("tokens = " + str(this.tokens) + "\n")

                statesDict = {}
                for state in this.DFA.states:
                    statesDict[state.id] = state.tokenID
                file.write("states = " + str(statesDict) + "\n")

                finalsArray = []
                for state in this.DFA.final:
                    finalsArray.append(state.id)
                file.write("finals = " + str(finalsArray) + "\n")

                transitionsDict = {}
                for transition in this.DFA.transitions:
                    if transition.source.id not in transitionsDict:
                        transitionsDict[transition.source.id] = {}
                    transitionsDict[transition.source.id][transition.symbol.cid] = transition.target.id
                file.write("transitions = " + str(transitionsDict) + "\n")

                file.write("def executeToken(token, text):\n")
                for token in this.tokens:
                    file.write("\tif token == \"" + token + "\" or text == \"" + token + "\":\n")

                    if this.tokens[token] == "":
                        file.write("\t\treturn None\n")
                    else: 
                        if this.isDebugging:
                            tempString = this.tokens[token].replace("return ", "")
                            file.write("\t\treturn '" + tempString + "'\n")
                        else:    
                            file.write("\t\t" + this.tokens[token] + "\n")

                file.write("with open(\"input.txt\", \"r\") as file:\n")
                file.write("\tdata = file.read().splitlines()\n")
                file.write("newData = ''\n")
                file.write("for item in data:\n")
                file.write("\tnewData += item\n")
                file.write("\tnewData += ' '\n")
                file.write("data = newData\n")

                file.write("current = 0\n")
                file.write("valid = ''\n")
                file.write("for symbol in data:\n")
                file.write("\tif symbol not in transitions[current]:\n")
                file.write("\t\tif len(valid) > 0:\n")
                file.write("\t\t\tprint('Valid token found: ' + valid)\n")
                
                if this.isDebugging:
                    file.write("\t\t\tprint(executeToken(states[current], valid))\n")
                else:
                    file.write("\t\t\texecuteToken(states[current], valid)\n")
                
                file.write("\t\tcurrent = 0\n")
                file.write("\t\tvalid = ''\n")
                file.write("\t\tprint('Invalid symbol found: ' + symbol)\n")
                file.write("\telse:\n")
                file.write("\t\tvalid += symbol\n")
                file.write("\t\tcurrent = transitions[current][symbol]\n")

                print(f"{filename} created successfully.")
        

    
        
