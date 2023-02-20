def menuInput(options, text = "Menu"):
    menu = "\n" + text + ":\n"

    for i in range(len(options)):
        menu = menu + str(i + 1) + ". " + options[i] + "\n"
    menu = menu + "> "

    while(True):
        userInput = input(menu)
        try:
            inputData = int(userInput)

            if inputData <= len(options):
                return(inputData)
            else: 
                print("\nIngrese una opción válida")
        except:
            print("\nIngrese una opción válida")  

def selectOption(options, text = "Seleccione una opción"):
    menuOptions = []
    userOptions = {}
    
    for i in range(len(options)):
        userOptions[str(i + 1)] = options[i]
        menuOptions.append(options[i])
    
    selected = menuInput(menuOptions, text)
    return userOptions[str(selected)]

def textInput(text, maxLength = 20):
    while(True):
        userInput = input("\n" + text + ": ")

        try:
            inputData = str(userInput)

            if len(inputData) <= maxLength:
                return(inputData)
            else: 
                print("\nPor favor ingresar un máximo de " + str(maxLength) + "caracteres.")
        except:
            print("\nIngrese una opción válida.")  

def intInput(text, maxValue, minValue = 0):
    while(True):
        userInput = input("\n" + text + ": ")

        try:
            inputData = int(userInput)

            if minValue <= inputData <= maxValue:
                return(inputData)
            else: 
                print("\nIngrese un número entre " + str(minValue) + " y " + str(maxValue))
        except:
            print("\nIngrese una opción válida")  