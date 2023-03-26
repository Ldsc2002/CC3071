from modules.driver import isDebugging, isDebugging, selectOption, readYalex

yalexOptions = [
    "data/1.yal",
]

if __name__ == '__main__':
    if isDebugging():
        selected = selectOption(yalexOptions, "Select a yalex file to test")

        readYalex(selected)
    
    else:
        pass