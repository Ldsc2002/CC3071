from modules.driver import generateNFA, textInput

if __name__ == '__main__':
    regex = textInput("Please enter a regular expression")

    generateNFA(regex)