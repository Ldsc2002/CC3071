from modules.driver import isDebugging, isDebugging, selectOption, generateFromYalex

yalexOptions = [
    "data/1.yal",
    "data/2.yal",
    "data/3.yal",
    "data/4.yal",
]

if __name__ == '__main__':
    if isDebugging():
        selected = selectOption(yalexOptions, "Select a yalex file to test")
        generateFromYalex(selected)
    
    else:
        pass