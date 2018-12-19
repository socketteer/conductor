import event

class Item:
    def __init__(self, name, portable=True):
        self.name = name
        self.portable = portable

class Container(Item):
    def __init__(self, name, preposition='in', portable=False):
        Item.__init__(self, name)
        self.contains = set()
        self.preposition = preposition
        self.portable = portable
