
class Item:
    def __init__(self, name, portable=True, attributes=[], aliases=[], article='auto'):
        self.name = name
        self.aliases = aliases
        self.aliases.append(name)
        self.portable = portable
        self.attributes = set()
        self.add_attributes(attributes)
        self.assign_article(article)

    def assign_article(self, article):
        if article == 'auto':
            if any(vowel == self.name[0] for vowel in ['a', 'e', 'i', 'o', 'u']):
                self.article = 'an '
            else:
                self.article = 'a '
        else:
            self.article = article

    def add_attribute(self, attribute):
        self.attributes.add(attribute)

    def add_attributes(self, attributes):
        for attribute in attributes:
            self.attributes.add(attribute)

    def remove_attribute(self, attribute):
        self.attributes.remove(attribute)

    def description(self):
        return 'You see {0}{1}.'.format(self.article, self.name)


class Container(Item):
    def __init__(self, name, preposition='in', portable=False, attributes=[], aliases=[], article='a'):
        Item.__init__(self, name, portable=portable, attributes=attributes, aliases=aliases, article=article)
        self.items = set()
        self.preposition = preposition
