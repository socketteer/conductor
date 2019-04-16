import txtvrse


class InitError(Exception):
    pass

# TODO game param instead of items_dict

class Item:
    def __init__(self, name, portable=True, id='auto', article='auto', game=-1):
        self.name = name
        self.aliases = {'thing', 'object', 'item'}
        self.aliases.add(name)
        self.portable = portable
        self.attributes = set()
        self.assign_article(article)
        self.assign_id(id, game)

    def assign_id(self, id, game):
        if id == 'auto':
            if game == -1:
                raise InitError("for auto id assignment, need to pass game")
            else:
                i = 1
                while self.name + str(i) in game.items:
                    i += 1
                self.id = self.name + str(i)
        else:
            self.id = id

    def assign_article(self, article):
        if article == 'auto':
            if any(vowel == self.name[0] for vowel in ['a', 'e', 'i', 'o', 'u']):
                self.article = 'an'
            else:
                self.article = 'a'
        else:
            self.article = article

    def add_attributes(self, attributes):
        if attributes:
            for attribute in attributes:
                self.attributes.add(attribute)

    def add_aliases(self, aliases):
        if aliases:
            for alias in aliases:
                self.aliases.add(alias)

    def remove_attribute(self, attribute):
        self.attributes.remove(attribute)

    def description(self):
        description = ""
        description += 'you see {0} {1}{2}.'.format(self.article, ', '.join(self.attributes) + ' ', self.name)
        return description

    def modify_game(self, game):
        pass


class Container(Item):
    def __init__(self, name, id='auto', preposition='in', portable=False, article='a', game=-1):
        Item.__init__(self, name=name, id=id, portable=portable, article=article, game=game)
        self.items = set()
        self.preposition = preposition

    def description(self):
        description = Item.description(self)
        if txtvrse.accessible(self):
            description += ' {0} the {1} is {2}.'.format(self.preposition,
                                                         self.name,
                                                         txtvrse.nlitemlist(list(self.items)))
        return description
