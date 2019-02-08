import event
from basicgame import Game
from gameutil import *
from roomutil import *
from item import Item, Container
from event import *

class Room:
    def __init__(self, name):
        self.items = set()
        self.items.add(self)
        self.name = name


class Portal(Item):
    def __init__(self, name, source, destination, attributes=[]):
        Item.__init__(self, name, portable=False, attributes=attributes)
        self.source = source
        self.destination = destination


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
                                                  effects=[[lambda: room_look_util(self.current_location), '']])

    def init_game_items(self):
        self.create_item('inventory', container=True)
        self.inventory = self.items['inventory']
        self.current_location = None

    def init_game_state(self, current_location):
        try:
            self.current_location = self.rooms[current_location]
        except KeyError:
            print('{0}.init_game_state ERROR: room {1} does not exist in game'.format(type(self), current_location))

    def init_actions(self):
        Game.init_actions(self)
        self.add_action('go', self.go, 1)

    def change_location(self, new_location):
        self.current_location = new_location

    def go(self, room):
        go_event = Event(preconditions=[[lambda: not self.current_location == room, "You are already in the {}".format(room.name)],
                                        item_in_room_precondition(room, self.current_location)],
                         effects=[[lambda: self.change_location(room), "You go to the {0}".format(room.name)]])
        return go_event

    def create_item(self, name, room=None, location=None, aliases=[], container=False, preposition='in'):
        if container:
            item = Container(name, preposition, aliases=aliases)
        else:
            item = Item(name, aliases=aliases)
        self.import_item(item, room, location, aliases)
        return item

    def import_item(self, item, room=None, location=None, aliases=[]):
        if room:
            room.items.add(item)
        self.items[item.name] = item
        try:
            if location:
                put_util(item, self.items[location])
        except KeyError:
            print('{0}.create_item ERROR: location {1} not in list of items'.format(type(self), location))
            return
        self.lexicon.nouns[item.name] = item.name

    def create_room(self, name):
        room = Room(name)
        self.rooms[name] = room
        self.import_item(room)
        return room

    def link_rooms(self, source, destination, two_way=True):
        source.items.add(destination)
        if two_way:
            destination.items.add(source)

    def run(self):
        if not self.current_location:
            print('{0}.run ERROR: variable current_location must be set.'.format(type(self)))
            return
        Game.run(self)
