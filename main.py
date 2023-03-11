from modules.driver import generateNFA, textInput, isDebugging, menuInput, selectOption

options = [
    "(a*|b*)c",
    "(b|b)*abb(a|b)*",
    "(a|E)b(a+)c?",
    "(a|b)*a(a|b)(a|b)",
    "b*ab?",
    "b+abc+",
    "0(0|1)*0",
    "((E|0)1*)*",
    "(0|1)*0(0|1)(0|1)",
    "(00)*(11)*",
    "0|1)1*(0|1)",
    "0?(1|E)?0*",
    "((1?)*)*",
    "(01)*(10)*",
    "a(a?b*|c+)b|baa"
]

if __name__ == '__main__':
    if isDebugging():
        regex = "a(a?b*|c+)b|baa"
        simulate = "baa"
    
    else:
        operationMode = menuInput(["Select regex from defaults list", "Input regex manually"], "Select an operation mode")

        if operationMode == 1:
            regex = selectOption(options, "Select a regex")

        elif operationMode == 2:
            regex = textInput("Please enter a regular expression", 1)
        
        simulate = textInput("Please enter a word to simulate (leave blank to skip)")
    
    if len(simulate) > 0:
        generateNFA(regex, simulate)
    else:
        generateNFA(regex)