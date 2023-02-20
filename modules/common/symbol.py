class Symbol():
    def __init__(this, symbolID):
        this.id = symbolID
        
        if symbolID == 'epsilon':
            this.cid = 'ε'
        else:
            this.cid = symbolID