class YaparParser():
    def __init__(this, file, yalex):
        this.file = file
        this.yalex = yalex
        this.parse()

    def parse(this):
        tokens = []
        productions = {}
        readingTokens = True
        prevProduction = None
        skip = False

        with open(this.file, 'r') as file:
            lines = file.read().splitlines()

            for line in lines:
                if "*/" in line:
                    skip = False
                    continue

                if skip:
                    continue

                if "/*" in line:
                    skip = True
                    continue

                if line != '':
                    if readingTokens:
                        if line == '%%':
                            readingTokens = False
                            continue
                        
                        line = line.replace("%token", "")
                        line = line.strip()

                        if line.count(' ') > 0:
                            line = line.split(' ')
                            for token in line:
                                tokens.append(token)
                        else:
                            tokens.append(line)

                    else:
                        line = line.strip()
                        
                        if prevProduction == None:
                            productions[line] = ''
                            prevProduction = line

                        else: 
                            productions[prevProduction] += line

                            if line == ';' or line.endswith(';'):
                                prevProduction = None

        # Create a list of tokens from the yalex file
        yalexTokens = []
        for token in this.yalex.tokens:
            newToken = this.yalex.tokens[token]
            newToken = newToken.replace("return ", "")
            newToken = newToken.strip()
            yalexTokens.append(newToken)

        # Check if all tokens in the yapar file are in the yalex file
        for token in tokens:
            if token not in yalexTokens:
                raise Exception("Token '" + token + "' not found in yalex file")

        print("Tokens: " + str(tokens))
        print("Productions: " + str(productions))