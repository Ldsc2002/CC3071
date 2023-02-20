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

    def __iter__(this):
        return iter(this.elements)