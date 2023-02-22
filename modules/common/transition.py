from modules.common.state import *
from modules.common.symbol import *

class Transition():
    def __init__(this, source, target, symbol):
        if (
            not isinstance(source, State) 
            or not isinstance(target, State) 
            or not isinstance(symbol, Symbol)
            ): raise TypeError("Transition: source, target and symbol must be of type State and Symbol respectively")

        this.source = source
        this.target = target
        this.symbol = symbol

    def __str__(this):
        return str(this.source) + " - " + str(this.symbol) + " -> " + str(this.target)