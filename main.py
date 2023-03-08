from modules.driver import generateNFA, textInput

if __name__ == '__main__':
    # regex = textInput("Please enter a regular expression")
    regex = "a(a?b*|c+)b|baa"

    generateNFA(regex)