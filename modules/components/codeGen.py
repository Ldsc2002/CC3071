import os
from modules.components.DFA import *

class CodeGen():
    def __init__(this, DFA, tokens):
        this.DFA = DFA
        this.tokens = tokens
        print("\nCreating Python code...")
        this.compile()

    def compile(this):
        filename = "out/" + "hello_world.py"
       
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

                file.write("input = input(\"Enter a string: \")\n")

                file.write("def executeToken(token):\n")
                for token in this.tokens:
                    file.write("\tif token == \"" + token + "\":\n")

                    if this.tokens[token] == "":
                        file.write("\t\treturn NONE\n")
                    else: 
                        file.write("\t\t" + this.tokens[token] + "\n")
     
                file.write("current = 0\n")
                file.write("for symbol in input:\n")
                file.write("\tcurrent = transitions[current][symbol]\n")
                file.write("if current in finals:\n")
                file.write("\tprint(\"The string '\" + input + \"' is accepted by the automata.\")\n")
                file.write("\tprint(\"Token: \" + str(states[current]))\n")
                file.write("\texecuteToken(states[current])\n")
                file.write("else:\n")
                file.write("\tprint(\"The string '\" + input + \"' is not accepted by the automata.\")\n")

                print(f"{filename} created successfully.")
        

    
        
