from event import *
from parse import sanitize
from item import Item, Container
from tbenv import TurnBasedEnv

class Game:
    def __init__(self, events=[]):
        self.items = {}
        self.actions = {}
        self.actions['look'] = Event(preconditions=[],
                                     effects=[lambda: self.look_util()],
                                     description=lambda: "look around")
        self.actions['put'] = {}
        self.actions['get'] = {}
        self.actions['drop'] = {}
        self.containers = {'inventory': Container('inventory'),
                           'floor': Container('floor', 'on')}
        self.env = TurnBasedEnv(events=events,
                                player_turn=self.turn)

    def item_in_container(self, item, container):
        return Precondition(definition=lambda: item.location == container.name)

    def put_util(self, item, dest):
        try:
            self.containers[item.location].contains.remove(item.name)
        except KeyError:
            pass
        dest.contains.add(item.name)
        item.location = dest.name

    def look_util(self):
        for container_name, container in self.containers.items():
            print('{0} {1}: {2}'.format(container.preposition,
                                        container_name,
                                        ', '.join(container.contains)))

    def put(self, item, container):
        return Event(preconditions=[self.item_in_container(item, container).negation(),
                                    self.item_in_container(item, self.containers['inventory'])],
                     effects=[lambda: self.put_util(item, container)],
                     description=lambda: "put {0} in {1}".format(item.name, container.name))

    def get(self, item):
        return Event(preconditions=[self.item_in_container(item, self.containers['inventory']).negation()],
                     effects=[lambda: self.put_util(item, self.containers['inventory'])],
                     description=lambda: "get {0}".format(item.name))

    def drop(self, item):
        return Event(preconditions=[self.item_in_container(item, self.containers['inventory'])],
                     effects=[lambda: self.put_util(item, self.containers['floor'])],
                     description=lambda: "drop {0}".format(item.name))


    def generate_actions(self):
        for item_name, item in self.items.items():
            self.actions['put'][item_name] = {}
            self.actions['get'][item_name] = self.get(item)
            self.actions['drop'][item_name] = self.drop(item)
            for container_name, container in self.containers.items():
                self.actions['put'][item_name][container_name] = self.put(item, container)

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
        self.env.run()