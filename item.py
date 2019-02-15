
class Item:
    def __init__(self, name, portable=True, attributes=[], aliases=[]):
        self.name = name
        self.aliases = aliases
        self.aliases.append(name)
        self.portable = portable
        self.attributes = set()
        self.add_attributes(attributes)

    def add_attribute(self, attribute):
        self.attributes.add(attribute)

    def add_attributes(self, attributes):
        for attribute in attributes:
            self.attributes.add(attribute)

    def remove_attribute(self, attribute):
        self.attributes.remove(attribute)

    def description(self):
        return 'You see a {0}.'.format(self.name)


class Container(Item):
    def __init__(self, name, preposition='in', portable=False, attributes=[], aliases=[]):
        Item.__init__(self, name, portable=portable, attributes=attributes, aliases=aliases)
        self.items = set()
        self.preposition = preposition
        self.portable = portable
