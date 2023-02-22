class Set():
    def __init__(this):
        this.elements = []

    def add(this, element):
        if element not in this.elements:
            this.elements.append(element)

    def intersect(this, other):
        return Set([e for e in this.elements if e in other.elements])

    def union(this, other):
        return Set(this.elements + other.elements)

    def difference(this, other):
        return Set([e for e in this.elements if e not in other.elements])

    def peek(this):
        return this.elements[-1]

    def pop(this):
        return this.elements.pop()

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