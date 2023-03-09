from modules.driver import generateNFA, textInput

if __name__ == '__main__':
    regex = textInput("Please enter a regular expression")
    simulate = textInput("Do you want to simulate the NFA? (y/n)")
    
    if simulate == "y":
        word = textInput("Please enter a word to simulate")
        generateNFA(regex, word)
    else:
        generateNFA(regex)