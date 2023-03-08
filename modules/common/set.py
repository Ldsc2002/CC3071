class Set():
    def __init__(this, elements = []):
        this.elements = []

    def add(this, element):
        if element not in this.elements:
            this.elements.append(element)

    def remove(this, element):
        if element in this.elements:
            this.elements.remove(element)

    def intersect(this, other):
        return Set([e for e in this.elements if e in other.elements])

    def union(this, other):
        for e in other.elements:
            this.add(e)

    def difference(this, other):
        return Set([e for e in this.elements if e not in other.elements])

    def peek(this):
        return this.elements[-1]

    def pop(this):
        return this.elements.pop()
    
    def sort(this):
        this.elements.sort()

    def len(this):
        return len(this.elements)

    def __str__(this):
        string = "["

        for x in range(len(this.elements)):
            string = string + str(this.elements[x])

            if x < len(this.elements) - 1:
                string = string + ", "
        
        string = string + "]"

        return string

    def __iter__(this):
        return iter(this.elements)

    def __len__(this):
        return len(this.elements)