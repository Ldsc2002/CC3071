from modules.proto.type import *
from modules.common.set import *

class State():
    def __init__(this, stateID, type = Type(0), states = Set()):
        this.id = stateID
        this.type = type

