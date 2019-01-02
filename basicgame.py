from event import *
from parse import parse_user_input, ParseError
from item import Item, Container
from tbenv import TurnBasedEnv
from lexicon import Lexicon


class InvalidOperation(Exception):
    pass

class NoGenerator(Exception):
    pass

class Game:
    def __init__(self, events=[]):
        self.lexicon = Lexicon()
        self.items = {}
        self.containers = {}
        self.action_generators = {}
        self.zero_operand_actions = {}
        self.one_operand_actions = {}
        self.two_operand_actions = {}
        self.zero_operand_actions['look'] = Event(preconditions=[],
                                                  effects=[lambda: self.look_util()])
        self.add_universal_action('put', self.put, 2)
        self.add_universal_action('get', self.get, 1)
        self.add_universal_action('drop', self.drop, 1)
        self.add_universal_action('open', self.open, 1)
        self.add_universal_action('close', self.close, 1)
        self.add_universal_action('look', self.inspect, 1)

        self.create_item('inventory', container=True)
        self.create_item('floor', aliases=['ground'], container=True, preposition='on')
        self.inventory = self.items['inventory']
        self.events = events
        self.env = 'uninitialized'

    def init_env(self):
        self.env = TurnBasedEnv(events=self.events,
                                player_turn=self.turn)

    def load_lexicon(self, verb_file=None, noun_file=None):
        if verb_file:
            self.lexicon.read_word_map(verb_file, 'verb')
        if noun_file:
            self.lexicon.read_word_map(noun_file, 'noun')

    def item_in(self, item, container):
        return item.location == container

    def put_util(self, item, dest):
        try:
            if not hasattr(dest, 'contains'):
                raise InvalidOperation
            if hasattr(item, 'location'):
                self.containers[item.location.name].contains.remove(item)
        except KeyError:
            print('{0}.put_util ERROR: item location not in containers'.format(type(self)))
            return
        dest.contains.add(item)
        item.location = dest

    def open_util(self, container):
        container.open = True

    def close_util(self, container):
        container.open = False

    def accessible(self, container):
        return (not hasattr(container, 'open')) or container.open

    def look_util(self):
        for container_name, container in self.containers.items():
            if container.contains:
                print('{0} {1}: {2}'.format(container.preposition,
                                            container_name,
                                            ', '.join([contents.name for contents in container.contains])))

    def description_util(self, item):
        if hasattr(item, 'description'):
            return item.description()
        else:
            return 'It is a {0}'.format(item.name)

    def inspect(self, item):
        return Event(preconditions=[],
                     effects=[lambda: print(self.description_util(item))])

    def put(self, item, container):
        return Event(preconditions=[lambda: item.portable,
                                    lambda: not self.item_in(item, container),
                                    lambda: hasattr(container, 'contains'),
                                    lambda: self.item_in(item, self.inventory),
                                    lambda: self.accessible(container)],
                     effects=[lambda: print('you put the {0} {1} the {2}'.format(item.name,
                                                                                 container.preposition,
                                                                                 container.name)),
                              lambda: self.put_util(item, container)])

    def get(self, item):
        return Event(preconditions=[lambda: item.portable,
                                    lambda: not self.item_in(item, self.inventory),
                                    lambda: self.accessible(item.location)],
                     effects=[lambda: print('you take the {0}'.format(item.name)),
                              lambda: self.put_util(item, self.inventory)])

    def drop(self, item):
        return Event(preconditions=[lambda: item.portable,
                                    lambda: self.item_in(item, self.inventory)],
                     effects=[lambda: print('you drop the {0}'.format(item.name)),
                              lambda: self.put_util(item, self.containers['floor'])])

    def open(self, container):
        return Event(preconditions=[lambda: hasattr(container, 'open'),
                                    lambda: not container.open],
                     effects=[lambda: print('you open the {0}'.format(container.name)),
                              lambda: self.open_util(container)])

    def close(self, container):
        return Event(preconditions=[lambda: hasattr(container, 'open'),
                                    lambda: container.open],
                     effects=[lambda: print('you close the {0}'.format(container.name)),
                              lambda: self.close_util(container)])

    def create_item(self, name, location=None, aliases=[], container=False, preposition='in'):
        if container:
            item = Container(name, preposition)
        else:
            item = Item(name)
        self.import_item(item, location, aliases, container)

    def import_item(self, item, location=None, aliases=[], container=False):
        self.items[item.name] = item
        if container:
            self.containers[item.name] = item
        try:
            if location:
                self.put_util(item, self.containers[location])
        except KeyError:
            print('{0}.create_item ERROR: location {1} not in self.containers'.format(type(self), location))
            return
        self.lexicon.nouns[item.name] = item.name
        self.add_item_aliases(item.name, aliases)

    def add_item_aliases(self, name, aliases):
        for alias in aliases:
            self.lexicon.nouns[alias] = name

    def add_universal_action(self, action_name, action_generator, action_type):
        if action_type == 0:
            print('do not use this method to create zero operand actions; create directly instead')
            return
        elif action_type == 1:
            self.one_operand_actions[action_name] = {}
        elif action_type == 2:
            self.two_operand_actions[action_name] = {}
        else:
            print('{0}.add_universal_action ERROR: invalid action_type {1}'.format(type(self), action_type))
            return
        self.action_generators[action_name] = action_generator

    def generate_actions(self):
        for item_name, item in self.items.items():
            for action_name, action in self.two_operand_actions.items():
                action[item_name] = {}
                for other_item_name, other_item in self.items.items():
                    action[item_name][other_item_name] = self.action_generators[action_name](item, other_item)
            for action_name, action in self.one_operand_actions.items():
                action[item_name] = self.action_generators[action_name](item)

    def generate_actions_template(self):
        for item_name, item in self.items.items():
            for action_name, action in self.two_operand_actions.items():
                action[item_name] = {}

    def exe(self, action, target1=None, target2=None, action_type=1):
        try:
            if action_type == 0:
                print('do not use this method to execute zero operand actions; execute directly instead')
                return False
            elif action_type == 1:
                return self.one_operand_actions[action][target1].query()
            elif action_type == 2:
                return self.two_operand_actions[action][target1][target2].query()
        except KeyError:
            if not self.generate_action(action, target1, target2, action_type):
                raise NoGenerator
            else:
                return self.exe(action, target1, target2, action_type)

    def generate_action(self, action, target1, target2, action_type=1):
        #print('attempting to generate action: {0} {1} {2}'.format(action, target1, target2))
        if action in self.action_generators:
            if action_type == 1:
                self.one_operand_actions[action][target1] = self.action_generators[action](self.items[target1])
            else:
                self.two_operand_actions[action][target1][target2] = self.action_generators[action](self.items[target1],
                                                                                                    self.items[target2])
            return True
        else:
            return False

    def turn(self):
        try:
            command = input('\n>')
            try:
                command_type, parsed_command = parse_user_input(command, self.lexicon)
            except ParseError:
                return self.turn()
            '''except KeyError:
                print('{0}.turn ERROR: entity resolution failure'.format(type(self)))
                return self.turn()'''
            if command_type == 1:
                if parsed_command[0] == 'exit':
                    quit()
                elif parsed_command[0] == 'pass':
                    return True
                else:
                    result = self.zero_operand_actions[parsed_command[0]].query()
            elif command_type == 2:
                result = self.exe(parsed_command[0], parsed_command[1], action_type=1)
            elif command_type == 3:
                result = self.exe(parsed_command[0], parsed_command[1], parsed_command[2], action_type=2)
            else:
                print('{0}.turn ERROR: invalid command type {1}'.format(type(self), command_type))
                return self.turn()
            if not result:
                print('that is impossible')
                return self.turn()
            else:
                return True
        except KeyError:
            print('action or target invalid')
            return self.turn()
        except NoGenerator:
            print('no generator found for action')
            return self.turn()
        except TypeError:
            print('error: probably tried to apply action to invalid target')
            return self.turn()

    def run(self):
        if self.env == 'uninitialized':
            self.init_env()
        self.env.run()
