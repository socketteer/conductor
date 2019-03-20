import txtvrse.item

class Refrigerator(txtvrse.item.Container):
    def __init__(self,
                 name="refrigerator",
                 id="auto",
                 portable=False,
                 article="auto",
                 items_dict=-1):
        txtvrse.item.Container.__init__(self,
                           name=name,
                           id=id,
                           preposition='in',
                           portable=portable,
                           article=article,
                           items_dict=items_dict)
        self.add_aliases(['refrigerator', 'fridge', 'appliance'])
        self.open = False


class Bookcase(txtvrse.item.Container):
    def __init__(self,
                 name="bookcase",
                 id="auto",
                 portable=False,
                 article="auto",
                 items_dict=-1):
        txtvrse.item.Container.__init__(self,
                           name=name,
                           id=id,
                           preposition='in',
                           portable=portable,
                           article=article,
                           items_dict=items_dict)
        self.add_aliases(['bookcase', 'bookshelf', 'shelf'])


class Table(txtvrse.item.Container):
    def __init__(self,
                 name="table",
                 id="auto",
                 portable=False,
                 article="auto",
                 items_dict=-1):
        txtvrse.item.Container.__init__(self,
                           name=name,
                           id=id,
                           preposition='on',
                           portable=portable,
                           article=article,
                           items_dict=items_dict)
        self.add_aliases(['table', 'surface'])


class Counter(Table):
    def __init__(self,
                 name="counter",
                 id="auto",
                 portable=False,
                 article="auto",
                 items_dict=-1):
        Table.__init__(self,
                       name=name,
                       id=id,
                       portable=portable,
                       article=article,
                       items_dict=items_dict)
        self.add_aliases(['counter', 'countertop'])


class Book(txtvrse.item.Item):
    def __init__(self,
                 name="book",
                 id="auto",
                 portable=True,
                 article="auto",
                 text="",
                 items_dict=-1):
        txtvrse.item.Item.__init__(self,
                      name=name,
                      id=id,
                      portable=portable,
                      article=article,
                      items_dict=items_dict)
        self.add_aliases(['book', 'volume', 'publication', 'tome'])
        self.text = text


class Microwave(txtvrse.item.Container):
    def __init__(self,
                 name="microwave",
                 id="auto",
                 portable=False,
                 article="auto",
                 items_dict=-1):
        txtvrse.item.Container.__init__(self,
                           name=name,
                           id=id,
                           preposition='in',
                           portable=portable,
                           article=article,
                           items_dict=items_dict)
        self.add_aliases(['microwave', 'oven', 'appliance'])
        self.open = False
        self.on = False


class Chair(txtvrse.item.Container):
    def __init__(self,
                 name="chair",
                 id="auto",
                 portable=False,
                 article="auto",
                 items_dict=-1):
        txtvrse.itemContainer.__init__(self,
                           name=name,
                           id=id,
                           preposition='on',
                           portable=portable,
                           article=article,
                           items_dict=items_dict)
        self.add_aliases(['chair', 'seat', 'furniture'])


class Bed(txtvrse.item.Container):
    def __init__(self,
                 name="bed",
                 id="auto",
                 portable=False,
                 article="auto",
                 items_dict=-1):
        txtvrse.item.Container.__init__(self,
                           name=name,
                           id=id,
                           preposition='on',
                           portable=portable,
                           article=article,
                           items_dict=items_dict)
        self.add_aliases(['bed', 'mattress', 'furniture'])


class Couch(txtvrse.item.Container):
    def __init__(self,
                 name="couch",
                 id="auto",
                 portable=False,
                 article="auto",
                 items_dict=-1):
        txtvrse.item.Container.__init__(self,
                           name=name,
                           id=id,
                           preposition='on',
                           portable=portable,
                           article=article,
                           items_dict=items_dict)
        self.add_aliases(['couch', 'sofa', 'divan', 'seat', 'settee', 'furniture'])


