from modules.proto.type import *
from modules.common.set import *

class State():
    def __init__(this, stateID = '', tokenID = "", type = 1):
        this.id = stateID
        this.tokenID = tokenID
        this.type = Type(type)

    def __str__(this):
        return str(this.id)

