from basicgame import *
from gameutil import *
import roomutil
import gameutil
from item import Item, Container
from parse import *
import debug_util
import room_actions
import catalogue


class Room(Container):
    def __init__(self, game, name, id='auto', article='the'):
        # TODO two word names
        Container.__init__(self,
                           name,
                           id=id,
                           portable=False,
                           article=article,
                           items_dict=game.items)
        self.items.add(self)
        self.floor = Container('{0}_floor'.format(self.name),
                               preposition='on',
                               items_dict=game.items)
        self.floor.add_aliases(['floor', 'ground'])
        self.items.add(self.floor)
        self.walls = Container('{0}_walls'.format(self.name),
                               preposition='on',
                               items_dict=game.items)
        self.items.add(self.walls)


class Portal(Item):
    def __init__(self, game, name, destination, door=None, id='auto', article='the'):
        Item.__init__(self,
                      name,
                      id=id,
                      portable=False,
                      article=article,
                      items_dict=game.items)
        self.add_aliases(['room', 'place', 'location', 'area', 'door', 'doorway', 'portal'])
        self.destination = destination
        self.door = door


class Door(Item):
    def __init__(self, game, name, open=False, locked=False, id='auto', article='auto'):
        Item.__init__(self,
                      name,
                      id=id,
                      portable=False,
                      article=article,
                      items_dict=game.items)
        self.open = open
        self.locked = locked


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
                                                  effects={'look': [lambda game: None,
                                                                    lambda game: roomutil.room_look_util(game.current_location)]})

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
        self.add_action('put', room_actions.put, 2)
        self.add_action('get', room_actions.get, 1)
        self.add_action('drop', room_actions.drop, 1)
        self.add_action('open', room_actions.open, 1)
        self.add_action('close', room_actions.close, 1)
        self.add_action('go', room_actions.go, 1)
        self.add_action('look', game_actions.inspect, 1)

    def accessible_items(self):
        accessible = self.current_location.items.union(self.inventory.items)
        accessible.add(self.inventory)
        return accessible

    def change_location(self, new_location):
        self.current_location = new_location

    def create_item(self,
                    name,
                    room=None,
                    location=None,
                    container=False,
                    portable=False,
                    preposition='in',
                    article='auto',
                    id='auto'):
        if container:
            item = Container(name,
                             id=id,
                             preposition=preposition,
                             portable=portable,
                             article=article,
                             items_dict=self.items)
        else:
            item = Item(name,
                        id=id,
                        portable=portable,
                        article=article,
                        items_dict=self.items)
        self.add_item(item, room, location)
        return item

    def add_item(self, item, room=None, location=None):
        if room:
            room.items.add(item)
            try:
                if location:
                    put_util(item, location)
                else:
                    put_util(item, room.floor)
            except KeyError:
                raise OperationError('{0}.add_item ERROR: location {1} not in self.items'.format(type(self), location.id))
        self.items[item.id] = item
        self.update_lexicon(item)
        return item

    def create_room(self, name):
        room = Room(self, name)
        self.rooms[room.id] = room
        self.add_item(room)
        self.add_item(room.floor)
        return room

    def link_rooms(self,
                   source,
                   destination,
                   door=False,
                   door_open=False,
                   door_locked=False,
                   two_way=True,
                   portal1name='default',
                   portal2name='default'):
        if portal1name == 'default':
            portal1name = destination.name
        if portal2name == 'default':
            portal2name = source.name

        dest_portal = Portal(self,
                             portal1name,
                             id='{0}_to_{1}'.format(source.id, destination.id),
                             destination=destination)
        dest_portal.add_aliases(["door", "doorway"])
        dest_portal.add_aliases(destination.aliases)
        source_portal = None
        self.add_item(dest_portal, room=source, location=source.walls)
        if door:
            door = Door(self,
                        name='{0}_{1}_door'.format(source.id, destination.id),
                        open=door_open,
                        locked=door_locked)
            self.add_item(door)
            dest_portal.door = door
        if two_way:
            source_portal = Portal(self,
                                   portal2name,
                                   id='{1}_to_{0}'.format(source.id, destination.id),
                                   destination=source)
            source_portal.add_aliases(["door", "doorway"])
            source_portal.add_aliases(source.aliases)
            self.add_item(source_portal, room=destination, location=destination.walls)
            if door:
                source_portal.door = door
        return dest_portal, source_portal

    def run(self):
        if not self.current_location:
            raise OperationError('{0}.run ERROR: variable current_location must be set.'.format(type(self)))
        Game.run(self)

    def report_state(self):
        pass

    def turn(self):
        self.report_state()
        user_input = input('\n>')
        msg = None
        if not user_input:
            return self.turn()
        try:
            command, objects = process_input(user_input, self.lexicon)
        except ParseError:
            print('command not understood.')
            return self.turn()
        try:
            command = self.lexicon.resolve(command, pos='verb')
        except KeyError:
            print('command not understood.')
            return self.turn()
        try:
            if len(objects) == 0:
                if command == 'exit':
                    quit()
                elif command == 'pass':
                    return True
                else:
                    result, msg = self.exe(self.zero_operand_actions[command])
            elif len(objects) == 1:
                obj = resolve_phrase(objects[0].noun,
                                     objects[0].adjectives,
                                     self.accessible_items(),
                                     self.lexicon)
                result, msg = self.process_command(command, obj, action_type=1)
            elif len(objects) == 2:
                obj1 = resolve_phrase(objects[0].noun,
                                      objects[0].adjectives,
                                      self.accessible_items(),
                                      self.lexicon)
                obj2 = resolve_phrase(objects[1].noun,
                                      objects[1].adjectives,
                                      self.accessible_items(),
                                      self.lexicon)
                result, msg = self.process_command(command, obj1, obj2, action_type=2)
            else:
                raise CommandError("too many objects in input {0}".format(user_input))
        except ResolutionFailure:
            print('you cannot do that.')
            return self.turn()
        except ResolutionAmbiguity as e:
            print('which {0}?'.format(e.args[1]))
            return self.turn()
        except CommandError:
            print('command not understood.')
            return self.turn()
        return result, msg

