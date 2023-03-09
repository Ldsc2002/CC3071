from modules.driver import generateNFA, textInput, isDebugging

if __name__ == '__main__':
    if isDebugging():
        regex = "a(a?b*|c+)b|baa"
        simulate = "baa"
    
    else:
        regex = textInput("Please enter a regular expression", 1)
        simulate = textInput("Please enter a word to simulate (leave blank to skip)")
    
    if len(simulate) > 0:
        generateNFA(regex, simulate)
    else:
        generateNFA(regex)