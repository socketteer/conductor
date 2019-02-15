from basicgame import *
from gameutil import *
from roomutil import *
from item import Item, Container
from event import *
from parse import *


class Room(Container):
    def __init__(self, name, aliases=[], attributes=[], article='the '):
        # TODO two word names
        Container.__init__(self, name, portable=False, aliases=aliases, attributes=attributes, article=article)
        self.items = set()
        self.items.add(self)
        self.name = name
        self.floor = Container('{0}_floor'.format(self.name), preposition='on', aliases=['floor'])
        self.items.add(self.floor)

    def description(self):
        return enumerate_items(self)


class Portal(Item):
    def __init__(self, name, destination, aliases=[], attributes=[], article='the '):
        Item.__init__(self, name, portable=False, aliases=aliases, attributes=attributes, article=article)
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
        self.zero_operand_actions['inventory'] = Event(preconditions=[],
                                                       effects=[access_inventory_effect(self.inventory)])
        self.current_location = None

    def init_game_state(self, current_location):
        try:
            self.current_location = self.rooms[current_location]
        except KeyError:
            raise OperationError('{0}.init_game_state ERROR: room {1} does not exist in game'.format(type(self), current_location))

    def init_actions(self):
        Game.init_actions(self)
        self.add_action('go', self.go, 1)

    def accessible_items(self):
        accessible = self.current_location.items.union(self.inventory.items)
        accessible.add(self.inventory)
        return accessible

    def change_location(self, new_location):
        self.current_location = new_location

    def go(self, room):
        go_event = Event(preconditions=[[lambda: not self.current_location == room, "You are already in the {}".format(room.name)],
                                        item_in_room_precondition(room, self.current_location)],
                         effects=[[lambda: self.change_location(room), "You go to the {0}".format(room.name)]])
        return go_event

    def get(self, item):
        return Event(preconditions=[item_in_room_precondition(item, self.current_location),
                                    portable_precondition(item),
                                    item_not_in_precondition(item, self.inventory),
                                    location_accessible_precondition(item.location)],
                     effects=[room_get_effect(item, self.inventory, self.current_location)])

    def drop(self, item):
        return Event(preconditions=[portable_precondition(item),
                                    item_in_precondition(item, self.inventory)],
                     effects=[room_drop_effect(item, self.current_location)])

    def put(self, item, container):
        return Event(preconditions=[portable_precondition(item),
                                    location_accessible_precondition(item.location),
                                    item_accessible_precondition(item, self.current_location, self.inventory),
                                    item_not_in_precondition(item, container),
                                    container_precondition(container),
                                    location_accessible_precondition(container)],
                     effects=[room_put_effect(item, self.current_location, container)])

    def create_item(self, name, room=None, location=None, aliases=[], attributes=[], container=False, preposition='in', article='auto'):
        if container:
            item = Container(name, preposition, aliases=aliases, attributes=attributes, article=article)
        else:
            item = Item(name, aliases=aliases, attributes=attributes, article=article)
        self.add_item(item, room, location)
        return item

    def add_item(self, item, room=None, location=None):
        if room:
            room.items.add(item)
            try:
                if location:
                    put_util(item, self.items[location])
                else:
                    put_util(item, room.floor)
            except KeyError:
                raise OperationError('{0}.create_item ERROR: location {1} not in self.containers'.format(type(self), location))
        self.items[item.name] = item
        self.update_lexicon(item)

    def create_room(self, name):
        room = Room(name)
        self.rooms[name] = room
        self.add_item(room)
        self.add_item(room.floor)
        return room

    def link_rooms(self, source, destination, two_way=True, portal1name='default', portal2name='default'):
        source.items.add(destination)
        dest_portal = Portal("{0}_door".format(destination.name), destination=destination, aliases=["door", "doorway"])
        self.add_item(dest_portal, room=source)
        if two_way:
            destination.items.add(source)
            source_portal = Portal("{0}_door".format(source.name), destination=source, aliases=["door", "doorway"])
            self.add_item(source_portal, room=destination)

    def run(self):
        if not self.current_location:
            raise OperationError('{0}.run ERROR: variable current_location must be set.'.format(type(self)))
        Game.run(self)

    def report_state(selgamef):
        pass

    def turn(self):
        try:
            self.report_state()
            user_input = input('\n>')
            try:
                command, objects = process_input(user_input, self.lexicon)
            except ParseError as e:
                print(repr(e))
                return self.turn()
            command = self.lexicon.resolve(command, pos='verb')
            if len(objects) == 0:
                if command == 'exit':
                    quit()
                elif command == 'pass':
                    return True
                else:
                    result = self.exe(self.zero_operand_actions[command])
            elif len(objects) == 1:
                obj = resolve_phrase(objects[0].noun, objects[0].adjectives, self.accessible_items(), self.lexicon)
                result = self.process_command(command, obj.name, action_type=1)
            elif len(objects) == 2:
                obj1 = resolve_phrase(objects[0].noun, objects[0].adjectives, self.accessible_items(), self.lexicon)
                obj2 = resolve_phrase(objects[1].noun, objects[1].adjectives, self.accessible_items(), self.lexicon)
                result = self.process_command(command, obj1.name, obj2.name, action_type=2)
            else:
                raise CommandError("Too many objects in input {0}".format(user_input))
            if not result:
                return False
            else:
                return True
        except NoGenerator as e:
            print(repr(e))
            return False
        except TypeError as e:
            print(repr(e))
            return False
        except KeyError as e:
            print(repr(e))
            return False
        except CommandError as e:
            print(repr(e))
            return False
        except ResolutionFailure as e:
            print(repr(e))
            return False
        except ResolutionAmbiguity as e:
            print(repr(e))
            return False
