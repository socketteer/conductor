import event

class Item:
    def __init__(self, name):
        self.name = name
        self.location = 'N/A'

class Container(Item):
    def __init__(self, name, preposition='in'):
        Item.__init__(self, name)
        self.contains = set()
        self.preposition = preposition
