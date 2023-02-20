class Symbol():
    def __init__(this, symbolID):
        this.id = symbolID
        
        if symbolID == 'epsilon' or symbolID == 'E':
            this.cid = 'ε'
        else:
            this.cid = symbolID