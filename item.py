class InitError(Exception):
    pass


class Item:
    def __init__(self, name, id='auto', portable=True, attributes=None, aliases=None, article='auto', items=-1):
        self.name = name
        if not aliases:
            self.aliases = []
        else:
            self.aliases = aliases
        self.aliases.append(name)
        self.portable = portable
        self.attributes = set()
        self.add_attributes(attributes)
        self.assign_article(article)
        self.assign_id(id, items)

    def assign_id(self, id, items):
        if id == 'auto':
            if items == -1:
                raise InitError("for auto id assignment, need to pass items")
            else:
                i = 1
                while self.name + str(i) in items:
                    i += 1
                self.id = self.name + str(i)
        else:
            self.id = id


    def assign_article(self, article):
        if article == 'auto':
            if any(vowel == self.name[0] for vowel in ['a', 'e', 'i', 'o', 'u']):
                self.article = 'an '
            else:
                self.article = 'a '
        else:
            self.article = article

    def add_attributes(self, attributes):
        if attributes:
            for attribute in attributes:
                self.attributes.add(attribute)

    def add_aliases(self, aliases):
        if aliases:
            for alias in aliases:
                self.aliases.append(alias)

    def remove_attribute(self, attribute):
        self.attributes.remove(attribute)

    def description(self):
        return 'You see {0}{1}.'.format(self.article, self.name)


class Container(Item):
    def __init__(self, name, id='auto', preposition='in', portable=False, attributes=None, aliases=None, article='a', items=None):
        Item.__init__(self, name=name, id=id, portable=portable, attributes=attributes, aliases=aliases, article=article, items=items)
        self.items = set()
        self.preposition = preposition
