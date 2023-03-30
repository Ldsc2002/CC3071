from modules.driver import isDebugging, isDebugging, selectOption, readYalex, menuInput

yalexOptions = [
    "data/1.yal",
    "data/2.yal",
    "data/3.yal",
    "data/4.yal",
]

if __name__ == '__main__':
    if isDebugging():
        operationMode = menuInput(["Test all yalex files", "Test a single yalex file"])

        if operationMode == 1:
            readYalex(yalexOptions.pop())

            for file in yalexOptions:
                readYalex(file, False)

        elif operationMode == 2:
            selected = selectOption(yalexOptions, "Select a yalex file to test")
            readYalex(selected)
    
    else:
        pass