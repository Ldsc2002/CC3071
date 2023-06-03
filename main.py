from modules.driver import isDebugging, isDebugging, menuInput, readYapar

yalexOptions = [
    "data/1.yal",
    "data/3.yal",
    "data/labF.yal",
]

yaparOptions = [
    "data/1.yalp",
    "data/3.yalp",
    "data/labF.yalp",
]

simulatorOptions = [
    "data/1Ta.txt",
    "data/1Tb.txt",
    "data/1Tc.txt",
    "data/1Td.txt",
    "data/1Te.txt",
    "data/3Fa.txt",
    "data/3Fb.txt",
    "data/3Fc.txt",
]

if __name__ == '__main__':
    if isDebugging():
        selected = menuInput(yaparOptions, "Select a yapar file to test")
        testFile = menuInput(simulatorOptions, "Select a test file to test")

        readYapar(yalexOptions[selected - 1], yaparOptions[selected - 1], simulatorOptions[selected - 1])    
    else:
        pass