import event
from basicgame import Game
from lexicon import Lexicon
from gameutil import *
from item import Item, Container
from event import *

class Room:
    def __init__(self, name):
        self.items = set()
        self.name = name


class RoomGame(Game):
    def __init__(self, events=[]):
        Game.__init__(self, events)

    def init_game_structure(self):
        self.items = {}
        self.rooms = {}
        self.action_generators = {}
        self.zero_operand_actions = {}
        self.one_operand_actions = {}
        self.two_operand_actions = {}
        self.zero_operand_actions['look'] = Event(preconditions=[],
                                                  effects=[[lambda: look_util(self.current_location.items), '']])

    def init_game_items(self):
        self.create_item('inventory', container=True)
        self.inventory = self.items['inventory']
        self.current_location = None

    def create_item(self, name, room=None, location=None, aliases=[], container=False, preposition='in'):
        if container:
            item = Container(name, preposition)
        else:
            item = Item(name)
        self.import_item(item, room, location, aliases)

    def import_item(self, item, room=None, location=None, aliases=[]):
        if not room and not location:
            print('{0}.import_item ERROR: must specify room or location'.format(type(self)))
            return
        self.items[item.name] = item
        if room:
            room.items.add(item)
        try:
            if location:
                put_util(item, self.items[location])
        except KeyError:
            print('{0}.create_item ERROR: location {1} not in self.containers'.format(type(self), location))
            return
        self.lexicon.nouns[item.name] = item.name
        self.add_item_aliases(item.name, aliases)

    def create_room(self, name):
        pass

    def create_portal(self, room1, room2):
        pass
