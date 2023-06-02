from modules.driver import isDebugging, isDebugging, menuInput, readYapar

yalexOptions = [
    "data/1.yal",
    "data/3.yal",
]

yaparOptions = [
    "data/1.yalp",
    "data/3.yalp",
]

simulatorOptions = [
    "data/1T.txt",
    "data/1T.txt",
]

if __name__ == '__main__':
    if isDebugging():
        selected = menuInput(yaparOptions, "Select a yapar file to test")
        readYapar(yalexOptions[selected - 1], yaparOptions[selected - 1], simulatorOptions[selected - 1])
    
    else:
        pass