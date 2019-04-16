import txtvrse


class CommandError(Exception):
    pass


class OperationError(Exception):
    pass


class Game:
    def __init__(self, events=None, debug=False):
        self.lexicon = txtvrse.Lexicon()
        self.init_game_structure()
        self.init_actions()
        self.init_game_items()
        if events:
            self.events = events
        else:
            self.events = []
        self.debug = debug

    def print_debugging_info(self):
        print(self.items)
        print(self.zero_operand_actions)
        print(self.one_operand_actions)
        print(self.two_operand_actions)
        print(self.zero_operand_actions)
        # self.lexicon.print_lexicon()

    '''def step_debug(self):
        print('current location: {0}'.format(self.current_location.name))
    '''

    def init_game_structure(self):
        self.items = {}
        self.containers = {}
        self.action_generators = {}
        self.zero_operand_actions = {}
        self.one_operand_actions = {}
        self.two_operand_actions = {}
        self.zero_operand_actions['look'] = txtvrse.Event(preconditions={},
                                                          effects={'look': [
                                                              lambda: txtvrse.look_util(self.containers.values()), '']})

    def init_actions(self):
        self.add_action('put', txtvrse.put, 2)
        self.add_action('get', txtvrse.get, 1)
        self.add_action('drop', txtvrse.drop, 1)
        self.add_action('open', txtvrse.open, 1)
        self.add_action('close', txtvrse.close, 1)
        self.add_action('look', txtvrse.inspect, 1)

    def init_game_items(self):
        self.create_item('inventory', container=True)
        self.inventory = self.items['inventory']
        self.floor = self.create_item('floor', container=True, preposition='on')
        self.floor.add_aliases(['ground'])

    def load_lexicon(self, verb_file=None, noun_file=None):
        if verb_file:
            self.lexicon.read_word_map(verb_file, 'verb')
        if noun_file:
            self.lexicon.read_word_map(noun_file, 'noun')

    def create_item(self, name, location=None, container=False, preposition='in', article='auto'):
        if container:
            item = txtvrse.Container(name, preposition, article=article, game=self)
        else:
            item = txtvrse.Item(name, article=article, game=self)
        self.add_item(item, location, container)
        return item

    def add_item(self, item, location=None, container=False):
        self.items[item.id] = item
        if container:
            self.containers[item.id] = item
        try:
            if location:
                txtvrse.put_util(item, self.containers[location])
        except KeyError:
            raise OperationError(
                '{0}.create_item ERROR: location {1} not in self.containers'.format(type(self), location))
        self.update_lexicon(item)
        item.modify_game(self)

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
        self.lexicon.add_word(action_name, pos='verb')
        return action_generator

    def generate_actions(self):
        for item_id, item in self.items.items():
            for action_name, action in self.two_operand_actions.items():
                action[item_id] = {}
                for other_item_id, other_item in self.items.items():
                    action[item_id][other_item_id] = self.action_generators[action_name](item, other_item)
            for action_name, action in self.one_operand_actions.items():
                action[item_id] = self.action_generators[action_name](item)

    def generate_actions_template(self):
        for item_id, item in self.items.items():
            for action_name, action in self.two_operand_actions.items():
                action[item_id] = {}

    def process_command(self, action, target1=None, target2=None, action_type=1):
        try:
            if action_type == 0:
                print('do not use this method to execute zero operand actions; execute directly instead')
                return False
            elif action_type == 1:
                action_event = self.one_operand_actions[action][target1.id]
            elif action_type == 2:
                action_event = self.two_operand_actions[action][target1.id][target2.id]
            return self.exe(action_event)
        except KeyError:
            if not self.generate_action(action, target1, target2, action_type):
                raise txtvrse.NoGenerator("No generator exists for action {0}".format(action))
            else:
                return self.process_command(action, target1, target2, action_type)

    def exe(self, action, silent=False):
        success, msg = action.query(self)
        if not silent:
            if success:
                msg = action.execute(self)
        return success, msg

    def generate_action(self, action, target1, target2=None, action_type=1):
        if action in self.action_generators:
            try:
                if action_type == 1:
                    self.one_operand_actions[action][target1.id] = self.action_generators[action](target1)
                    act = self.one_operand_actions[action][target1.id]
                    return act
                else:
                    try:
                        self.two_operand_actions[action][target1.id][target2.id] = self.action_generators[action](
                            target1,
                            target2)
                        act = self.two_operand_actions[action][target1.id][target2.id]
                        return act
                    except KeyError:
                        self.two_operand_actions[action][target1.id] = {}
                        return self.generate_action(action, target1, target2, action_type)
            except AttributeError as e:
                raise AttributeError('Invalid type for action')
        else:
            return None

    def overload_action(self, action, target1, new_event, target2=None, action_type=1):
        if action in self.action_generators:
            try:
                if action_type == 1:
                    self.one_operand_actions[action][target1.id] = new_event
                    act = self.one_operand_actions[action][target1.id]
                    return act
                else:
                    try:
                        self.two_operand_actions[action][target1.id][target2.id] = new_event
                        act = self.two_operand_actions[action][target1.id][target2.id]
                        return act
                    except KeyError:
                        self.two_operand_actions[action][target1.id] = {}
                        return self.overload_action(action, target1, target2, new_event, action_type)
            except AttributeError as e:
                raise AttributeError('Invalid type for action')
        else:
            return None

    def turn(self):
        try:
            # self.step_debug()
            user_input = input('\n>')
            try:
                command, objects = txtvrse.process_input(user_input, self.lexicon)
            except txtvrse.ParseError as e:
                print(repr(e))
                return self.turn()
            command = self.lexicon.resolve(command, pos='verb')
            if len(objects) == 0:
                if command == 'exit':
                    quit()
                elif command == 'pass':
                    return True
                else:
                    result, msg = self.exe(self.zero_operand_actions[command])
            elif len(objects) == 1:
                obj = txtvrse.resolve_phrase(objects[0].noun, objects[0].adjectives, self.items, self.lexicon)
                result, msg = self.process_command(command, obj, action_type=1)
            elif len(objects) == 2:
                obj1 = txtvrse.resolve_phrase(objects[0].noun, objects[0].adjectives, self.items, self.lexicon)
                obj2 = txtvrse.resolve_phrase(objects[1].noun, objects[1].adjectives, self.items, self.lexicon)
                result, msg = self.process_command(command, obj1, obj2, action_type=2)
            else:
                raise CommandError("Too many objects in input {0}".format(user_input))
            return result, msg
        except txtvrse.NoGenerator as e:
            print(repr(e))
            return False
        except TypeError as e:
            print(repr(e))
            return False
        except KeyError:
            print('action or target invalid')
            return False

    def run(self):
        while True:
            state_change, msg = self.query_events()
            if state_change:
                print(msg)
            result, msg = self.turn()
            print(msg)

    def query_events(self):
        state_change = 0
        msg = None
        for event in self.events:
            success, _ = event.query(self)
            if success:
                msg = event.execute()
                state_change = 1
        return state_change, msg

    def alter_attributes(self, item, aliases=None, attributes=None):
        if aliases and not isinstance(aliases, list):
            aliases = [aliases]
        if attributes and not isinstance(attributes, list):
            attributes = [attributes]
        item.add_aliases(aliases)
        item.add_attributes(attributes)
        self.update_lexicon(item)
