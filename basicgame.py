from event import *
from parse import sanitize
from item import Item, Container
from tbenv import TurnBasedEnv

class Game:
    def __init__(self, events=[]):
        self.items = {}
        self.actions = {}
        self.actions['look'] = Event(preconditions=[],
                                     effects=[lambda: self.look_util()])
        self.actions['put'] = {}
        self.actions['get'] = {}
        self.actions['drop'] = {}
        self.actions['open'] = {}
        self.actions['close'] = {}
        self.containers = {'inventory': Container('inventory'),
                           'floor': Container('floor', 'on')}
        self.inventory = self.containers['inventory']
        self.events = events
        self.env = 'uninitialized'

    def init_env(self):
        self.env = TurnBasedEnv(events=self.events,
                                player_turn=self.turn)

    def item_in(self, item, container):
        return item.location == container

    def put_util(self, item, dest):
        try:
            self.containers[item.location].contains.remove(item)
        except KeyError:
            pass
        dest.contains.add(item)
        item.location = dest

    def open_util(self, container):
        container.open = True

    def close_util(self, container):
        container.open = False

    def has_door(self, container):
        return hasattr(container, 'open')

    def accessible(self, container):
        return not self.has_door(container) or container.open

    def look_util(self):
        for container_name, container in self.containers.items():
            print('{0} {1}: {2}'.format(container.preposition,
                                        container_name,
                                        ', '.join([contents.name for contents in container.contains])))

    def put(self, item, container):
        return Event(preconditions=[lambda: not self.item_in(item, container),
                                    lambda: self.item_in(item, self.inventory),
                                    lambda: self.accessible(container)],
                     effects=[lambda: print('you put the {0} {1} the {2}'.format(item.name,
                                                                                 container.preposition,
                                                                                 container.name)),
                              lambda: self.put_util(item, container)])

    def get(self, item):
        return Event(preconditions=[lambda: not self.item_in(item, self.inventory),
                                    lambda: self.accessible(item.location)],
                     effects=[lambda: print('you take the {0}'.format(item.name)),
                              lambda: self.put_util(item, self.inventory)])

    def drop(self, item):
        return Event(preconditions=[lambda: self.item_in(item, self.inventory)],
                     effects=[lambda: print('you drop the {0}'.format(item.name)),
                              lambda: self.put_util(item, self.containers['floor'])])

    def open(self, container):
        return Event(preconditions=[lambda: self.has_door(container),
                                    lambda: not container.open],
                     effects=[lambda: print('you open the {0}'.format(container.name)),
                              lambda: self.open_util(container)])

    def close(self, container):
        return Event(preconditions=[lambda: self.has_door(container),
                                    lambda: container.open],
                     effects=[lambda: print('you close the {0}'.format(container.name)),
                              lambda: self.close_util(container)])

    def generate_actions(self):
        for item_name, item in self.items.items():
            self.actions['put'][item_name] = {}
            self.actions['get'][item_name] = self.get(item)
            self.actions['drop'][item_name] = self.drop(item)
            for container_name, container in self.containers.items():
                self.actions['put'][item_name][container_name] = self.put(item, container)

        for container_name, container in self.containers.items():
            self.actions['open'][container_name] = self.open(container)
            self.actions['close'][container_name] = self.close(container)

    #standardized 0/1/2 target?
    def turn(self):
        try:
            command = sanitize(input('\n>'))
            action = command[0]
            if len(command) > 1:
                target = command[1]
                if len(command) > 2:
                    target2 = command[2]
            if action == 'exit' or action == 'quit':
                quit()
            elif action == 'pass':
                return True
            elif len(command) == 1:
                execute = self.actions[action]
            elif len(command) == 2:
                execute = self.actions[action][target]
            elif len(command) == 3:
                execute = self.actions[action][target][target2]
            else:
                print('invalid input')
                return self.turn()
            if not execute.query():
                print('that is impossible')
                return self.turn()
            else:
                return True
        except KeyError:
            print('can\'t')
            return self.turn()

    def run(self):
        if self.env == 'uninitialized':
            self.init_env()
        self.env.run()
