from modules.proto.type import *
from modules.common.set import *

class State():
    def __init__(this, stateID = '', tokenID = ""):
        this.id = stateID
        this.tokenID = tokenID

    def __str__(this):
        return str(this.id)

