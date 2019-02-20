from basicgame import *
from gameutil import *
import roomutil
import gameutil
from item import Item, Container
from parse import *
import debug_util
import room_actions


class Room(Container):
    def __init__(self, name, id='auto', aliases=None, attributes=None, article='the ', items=None):
        # TODO two word names
        Container.__init__(self, name, id=id, portable=False, aliases=aliases, attributes=attributes, article=article, items=items)
        self.items = set()
        self.items.add(self)
        self.name = name
        self.floor = Container('{0}_floor'.format(self.name), preposition='on', aliases=['floor'], items=items)
        self.items.add(self.floor)

    def description(self):
        return roomutil.enumerate_items(self)


class Portal(Item):
    def __init__(self, name, destination, id='auto', aliases=None, attributes=None, article='the ', items=None):
        Item.__init__(self, name, id=id, portable=False, aliases=aliases, attributes=attributes, article=article, items=items)
        self.destination = destination


class RoomGame(Game):
    def __init__(self, events=None):
        Game.__init__(self, events)

    def init_game_structure(self):
        self.items = {}
        self.rooms = {}
        self.action_generators = {}
        self.zero_operand_actions = {}
        self.one_operand_actions = {}
        self.two_operand_actions = {}
        self.zero_operand_actions['look'] = Event(preconditions={},
                                                  effects={'look': [lambda game: roomutil.room_look_util(game.current_location), '']})

    def init_game_items(self):
        self.inventory = self.create_item('inventory', container=True)
        self.zero_operand_actions['inventory'] = Event(preconditions={},
                                                       effects={'inventory': gameutil.access_inventory_effect()})
        self.current_location = None

    def init_game_state(self, current_location):
        try:
            self.current_location = current_location
        except KeyError:
            raise OperationError('{0}.init_game_state ERROR: room {1} does not exist in game'.format(type(self), current_location.name))

    def init_actions(self):
        Game.init_actions(self)
        self.add_action('go', room_actions.go, 1)

    def accessible_items(self):
        accessible = self.current_location.items.union(self.inventory.items)
        accessible.add(self.inventory)
        return accessible

    def change_location(self, new_location):
        self.current_location = new_location

    def create_item(self, name, room=None, location=None, aliases=None, attributes=None, container=False, portable=False, preposition='in', article='auto', id='auto'):
        if container:
            item = Container(name, id=id, preposition=preposition, aliases=aliases, attributes=attributes, portable=portable, article=article, items=self.items)
        else:
            item = Item(name, id=id, aliases=aliases, attributes=attributes, portable=portable, article=article, items=self.items)
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
        self.items[item.id] = item
        self.update_lexicon(item)

    def create_room(self, name, aliases=None, attributes=None):
        room = Room(name, aliases=aliases, attributes=attributes, items=self.items)
        self.rooms[room.id] = room
        self.add_item(room)
        self.add_item(room.floor)
        return room

    def link_rooms(self, source, destination, two_way=True, portal1name='default', portal2name='default'):
        #source.items.add(destination)
        if portal1name == 'default':
            portal1name = destination.name
        if portal2name == 'default':
            portal2name = source.name
        dest_portal = Portal(portal1name, id='{0}_to_{1}'.format(source.id, destination.id), destination=destination, aliases=["door", "doorway"], items=self.items)
        source_portal = None
        self.add_item(dest_portal, room=source)
        if two_way:
            #destination.items.add(source)
            source_portal = Portal(portal2name, id='{1}_to_{0}'.format(source.id, destination.id), destination=source, aliases=["door", "doorway"], items=self.items)
            self.add_item(source_portal, room=destination)
        return dest_portal, source_portal

    def run(self):
        if not self.current_location:
            raise OperationError('{0}.run ERROR: variable current_location must be set.'.format(type(self)))
        Game.run(self)

    def report_state(self):
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
                result = self.process_command(command, obj, action_type=1)
            elif len(objects) == 2:
                obj1 = resolve_phrase(objects[0].noun, objects[0].adjectives, self.accessible_items(), self.lexicon)
                obj2 = resolve_phrase(objects[1].noun, objects[1].adjectives, self.accessible_items(), self.lexicon)
                result = self.process_command(command, obj1, obj2, action_type=2)
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
        '''except AttributeError as e:
            print(repr(e))
            return False
        except CommandError as e:
            print(repr(e))
            return False
        except ResolutionFailure as e:
            print(repr(e))
            return False
        except ResolutionAmbiguity as e:
            print(repr(e)
            return False'''
