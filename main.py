from modules.driver import generateNFA, textInput

if __name__ == '__main__':
    regex = textInput("Please enter a regular expression", 1)
    simulate = textInput("Please enter a word to simulate (leave blank to skip)")
    
    if len(simulate) > 0:
        generateNFA(regex, simulate)
    else:
        generateNFA(regex)