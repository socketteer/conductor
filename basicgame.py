from event import *
from parse import *
from item import Item, Container
from tbenv import TurnBasedEnv
from lexicon import Lexicon
from gameutil import *
from entityresolution import *

class CommandError(Exception):
    pass

class OperationError(Exception):
    pass


class Game:
    def __init__(self, events=[], debug=False):
        self.lexicon = Lexicon()
        self.init_game_structure()
        self.init_actions()
        self.init_game_items()
        self.events = events
        self.env = 'uninitialized'
        self.debug = debug

    def print_debugging_info(self):
        print(self.items)
        #print(self.containers)
        print(self.zero_operand_actions)
        print(self.one_operand_actions)
        print(self.two_operand_actions)
        print(self.zero_operand_actions)
        #self.lexicon.print_lexicon()

    def step_debug(self):
        print('current location: {0}'.format(self.current_location.name))

    def init_game_structure(self):
        self.items = {}
        self.containers = {}
        self.action_generators = {}
        self.zero_operand_actions = {}
        self.one_operand_actions = {}
        self.two_operand_actions = {}
        self.zero_operand_actions['look'] = Event(preconditions=[],
                                                  effects=[[lambda: look_util(self.containers.values()), '']])

    def init_actions(self):
        self.add_action('put', self.put, 2)
        self.add_action('get', self.get, 1)
        self.add_action('drop', self.drop, 1)
        self.add_action('open', self.open, 1)
        self.add_action('close', self.close, 1)
        self.add_action('look', self.inspect, 1)

    def init_game_items(self):
        self.create_item('inventory', container=True)
        self.inventory = self.items['inventory']
        self.create_item('floor', aliases=['ground'], container=True, preposition='on')

    def init_env(self):
        self.env = TurnBasedEnv(events=self.events,
                                player_turn=self.turn)

    def load_lexicon(self, verb_file=None, noun_file=None):
        if verb_file:
            self.lexicon.read_word_map(verb_file, 'verb')
        if noun_file:
            self.lexicon.read_word_map(noun_file, 'noun')

    def inspect(self, item):
        return Event(preconditions=[],
                     effects=[inspect_effect(item)])

    def put(self, item, container):
        return Event(preconditions=[portable_precondition(item),
                                    location_accessible_precondition(item.location),
                                    item_not_in_precondition(item, container),
                                    container_precondition(container),
                                    location_accessible_precondition(container)],
                     effects=[get_effect(item, self.inventory),
                              put_effect(item, container)])

    def get(self, item):
        return Event(preconditions=[portable_precondition(item),
                                    item_not_in_precondition(item, self.inventory),
                                    location_accessible_precondition(item.location)],
                     effects=[get_effect(item, self.inventory)])

    def drop(self, item):
        return Event(preconditions=[portable_precondition(item),
                                    item_in_precondition(item, self.inventory)],
                     effects=[drop_effect(item, self.containers['floor'])])

    def open(self, container):
        return Event(preconditions=[openable_precondition(container),
                                    closed_precondition(container)],
                     effects=[open_effect(container)])

    def close(self, container):
        return Event(preconditions=[openable_precondition(container),
                                    open_precondition(container)],
                     effects=[close_effect(container)])

    def create_item(self, name, location=None, aliases=[], attributes=[], container=False, preposition='in', article='auto'):
        if container:
            item = Container(name, preposition, aliases=aliases, attributes=attributes, article=article)
        else:
            item = Item(name, aliases=aliases, attributes=attributes, article=article)
        self.add_item(item, location, container)
        return item

    def add_item(self, item, location=None, container=False):
        self.items[item.name] = item
        if container:
            self.containers[item.name] = item
        try:
            if location:
                put_util(item, self.containers[location])
        except KeyError:
            raise OperationError('{0}.create_item ERROR: location {1} not in self.containers'.format(type(self), location))
        self.update_lexicon(item)

    def update_lexicon(self, item):
        self.lexicon.add_word(item.name, pos='noun')
        for alias in item.aliases:
            self.lexicon.add_word(alias, pos='noun')
        for attribute in item.attributes:
            self.lexicon.add_word(attribute, pos='adjective')

    def add_action(self, action_name, action_generator, action_type):
        if action_type == 0:
            print('do not use this method to create zero operand actions; create directly instead')
            return
        elif action_type == 1:
            self.one_operand_actions[action_name] = {}
        elif action_type == 2:
            self.two_operand_actions[action_name] = {}
        else:
            raise OperationError('{0}.add_action ERROR: invalid action_type {1}'.format(type(self), action_type))
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

    def process_command(self, action, target1=None, target2=None, action_type=1):
        try:
            if action_type == 0:
                print('do not use this method to execute zero operand actions; execute directly instead')
                return False
            elif action_type == 1:
                action_event = self.one_operand_actions[action][target1]
            elif action_type == 2:
                action_event = self.two_operand_actions[action][target1][target2]
            self.exe(action_event)
        except KeyError:
            if not self.generate_action(action, target1, target2, action_type):
                raise NoGenerator("No generator exists for action {0}".format(action))
            else:
                return self.process_command(action, target1, target2, action_type)

    def exe(self, action, silent=False):
        success, event, predicate = action.query()
        if not silent:
            if not success:
                event.report_failure(predicate)
            else:
                event.report_success()
        return success

    def generate_action(self, action, target1, target2, action_type=1):
        if action in self.action_generators:
            if action_type == 1:
                self.one_operand_actions[action][target1] = self.action_generators[action](self.items[target1])
            else:
                try:
                    self.two_operand_actions[action][target1][target2] = self.action_generators[action](self.items[target1],
                                                                                                        self.items[target2])
                except KeyError:
                    self.two_operand_actions[action][target1] = {}
                    return self.generate_action(action, target1, target2, action_type)
            return True
        else:
            return False

    def turn(self):
        try:
            #self.step_debug()
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
                obj = resolve_phrase(objects[0].noun, objects[0].adjectives, self.items, self.lexicon)
                result = self.process_command(command, obj.name, action_type=1)
            elif len(objects) == 2:
                obj1 = resolve_phrase(objects[0].noun, objects[0].adjectives, self.items, self.lexicon)
                obj2 = resolve_phrase(objects[1].noun, objects[1].adjectives, self.items, self.lexicon)
                result = self.process_command(command, obj1.name, obj2.name, action_type=2)
            else:
                raise CommandError("Too many objects in input {0}".format(user_input))
                return False
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
        except KeyError:
            print('action or target invalid')
            return False

    def run(self):
        if self.env == 'uninitialized':
            self.init_env()
        self.env.run()

    def query_events(self):
        state_change = 0
        for event in self.events:
            success, event, predicate = event.query()
            if success:
                event.report_success()
                state_change = 1
        return state_change
