from modules.driver import generateNFA, debugAutomatas, textInput, isDebugging, menuInput, selectOption

options = [
    "(a*|b*)c",
    "(b|b)*abb(a|b)*", #TODO fix subsets hangs
    "(a|E)b(a+)c?", #TODO fix direct missing one transition
    "(a|b)*a(a|b)(a|b)", #TODO fix subsets missing states
    "b*ab?",
    "b+abc+", #TODO missing transitions
    "0(0|1)*0",
    "((E|0)1*)*",
    "(0|1)*0(0|1)(0|1)", #TODO fix subsets missing states and transitions
    "(00)*(11)*",
    "0|1)1*(0|1)",
    "0?(1|E)?0*", #TODO fix subsets crashes
    "((1?)*)*",
    "(01)*(10)*",
    "a(a?b*|c+)b|baa" #TODO fix direct missing one transition
]

testStrings = [
    "a",
    "a",
    "a",
    "a",
    "a",
    "a",
    "a",
    "a",
    "a",
    "a",
    "a",
    "a",
    "a",
    "a",
    "a",
]

if __name__ == '__main__':
    if isDebugging():
        operationMode = menuInput(["Test one", "Test all"], "Select an operation mode")

        if operationMode == 1:
            regex = selectOption(options, "Select a regex")
            simulate = textInput("Please enter a word to simulate (leave blank to skip)")
        
            debugAutomatas(regex, simulate)
        
        elif operationMode == 2:
            debugAutomatas(options, testStrings)
    
    else:
        operationMode = menuInput(["Select regex from defaults list", "Input regex manually"], "Select an operation mode")

        if operationMode == 1:
            regex = selectOption(options, "Select a regex")

        elif operationMode == 2:
            regex = textInput("Please enter a regular expression", 1)
        
        simulate = textInput("Please enter a word to simulate (leave blank to skip)")

        generateNFA(regex, simulate)