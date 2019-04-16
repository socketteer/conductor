import txtvrse.item


def read(item):
    return txtvrse.Event(preconditions={'item_in_room': txtvrse.item_in_room_precondition(item),
                                        'location_accessible': txtvrse.location_accessible_precondition(item)},
                         effects={'read': [lambda game: None, lambda game: item.text]})


class Refrigerator(txtvrse.item.Container):
    def __init__(self,
                 name="refrigerator",
                 id="auto",
                 portable=False,
                 article="auto",
                 game=-1):
        txtvrse.item.Container.__init__(self,
                                        name=name,
                                        id=id,
                                        preposition='in',
                                        portable=portable,
                                        article=article,
                                        game=game)
        self.add_aliases(['refrigerator', 'fridge', 'appliance'])
        self.open = False


class Bookcase(txtvrse.item.Container):
    def __init__(self,
                 name="bookcase",
                 id="auto",
                 portable=False,
                 article="auto",
                 game=-1):
        txtvrse.item.Container.__init__(self,
                                        name=name,
                                        id=id,
                                        preposition='in',
                                        portable=portable,
                                        article=article,
                                        game=game)
        self.add_aliases(['bookcase', 'bookshelf', 'shelf'])


class Table(txtvrse.item.Container):
    def __init__(self,
                 name="table",
                 id="auto",
                 portable=False,
                 article="auto",
                 game=-1):
        txtvrse.item.Container.__init__(self,
                                        name=name,
                                        id=id,
                                        preposition='on',
                                        portable=portable,
                                        article=article,
                                        game=game)
        self.add_aliases(['table', 'surface'])


class Counter(Table):
    def __init__(self,
                 name="counter",
                 id="auto",
                 portable=False,
                 article="auto",
                 game=-1):
        Table.__init__(self,
                       name=name,
                       id=id,
                       portable=portable,
                       article=article,
                       game=game)
        self.add_aliases(['counter', 'countertop'])


class Book(txtvrse.item.Item):
    def __init__(self,
                 name="book",
                 id="auto",
                 portable=True,
                 article="auto",
                 text="",
                 game=-1):
        txtvrse.item.Item.__init__(self,
                                   name=name,
                                   id=id,
                                   portable=portable,
                                   article=article,
                                   game=game)
        self.add_aliases(['book', 'volume', 'publication', 'tome'])
        self.text = text

    def modify_game(self, game):
        game.add_action(action_name='read',
                        action_generator=read,
                        action_type=1)
        game.overload_action(action='look',
                             target1=self,
                             new_event=read(self))


class Microwave(txtvrse.item.Container):
    def __init__(self,
                 name="microwave",
                 id="auto",
                 portable=False,
                 article="auto",
                 game=-1):
        txtvrse.item.Container.__init__(self,
                                        name=name,
                                        id=id,
                                        preposition='in',
                                        portable=portable,
                                        article=article,
                                        game=game)
        self.add_aliases(['microwave', 'oven', 'appliance'])
        self.open = False
        self.on = False


class Chair(txtvrse.item.Container):
    def __init__(self,
                 name="chair",
                 id="auto",
                 portable=False,
                 article="auto",
                 game=-1):
        txtvrse.itemContainer.__init__(self,
                                       name=name,
                                       id=id,
                                       preposition='on',
                                       portable=portable,
                                       article=article,
                                       game=game)
        self.add_aliases(['chair', 'seat', 'furniture'])


class Bed(txtvrse.item.Container):
    def __init__(self,
                 name="bed",
                 id="auto",
                 portable=False,
                 article="auto",
                 game=-1):
        txtvrse.item.Container.__init__(self,
                                        name=name,
                                        id=id,
                                        preposition='on',
                                        portable=portable,
                                        article=article,
                                        game=game)
        self.add_aliases(['bed', 'mattress', 'furniture'])


class Couch(txtvrse.item.Container):
    def __init__(self,
                 name="couch",
                 id="auto",
                 portable=False,
                 article="auto",
                 game=-1):
        txtvrse.item.Container.__init__(self,
                                        name=name,
                                        id=id,
                                        preposition='on',
                                        portable=portable,
                                        article=article,
                                        game=game)
        self.add_aliases(['couch', 'sofa', 'divan', 'seat', 'settee', 'furniture'])

