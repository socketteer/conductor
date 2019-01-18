from basicgame import Game
from standoff import *
from event import *
from gameutil import *

def start_util(item):
    item.on = True


def stop_util(item):
    item.on = False


def start(item):
    return Event(preconditions=[[lambda: hasattr(item, 'on'), 'you cannot start the {0}'.format(item.name)],
                                [lambda: not item.on, '{0} is already on'.format(item.name)]],
                 effects=[[lambda: start_util(item), 'you turn on the {0}'.format(item.name)]])


def stop(item):
    return Event(preconditions=[[lambda: hasattr(item, 'on'), 'you cannot stop the {0}'.format(item.name)],
                                [lambda: item.on, '{0} is already off'.format(item.name)]],
                 effects=[[lambda: stop_util(item), 'you turn off the {0}'.format(item.name)]])


def cook(item):
    if item.temperature == 'cold':
        item.temperature = 'hot'
    elif item.temperature == 'hot':
        item.temperature = 'super hot'
    elif item.temperature == 'super hot':
        explode()
        return
    if item.explosive:
        explode()


def irradiate():
    print('deadly radiation escapes the microwave. your head explodes, and you die.')
    quit()


def explode():
    print('the microwave explodes and you die')
    quit()


def cook_contents_util(item):
    for contents in item.contains:
        cook(contents)


def cook_contents(item):
    return Event(preconditions=[[lambda: item.on, 'oven is not on'],
                                [lambda: not len(item.contains) == 0, 'there is nothing in the microwave']],
                 effects=[[lambda: cook_contents_util(item)], '{0} is cooked'.format(item.name)])


def left_open(item):
    return Event(preconditions=[[lambda: item.on, 'oven is not on'],
                                [lambda: item.open, 'oven is not open']],
                 effects=[[lambda:irradiate(), 'the room is irradiated']])


game = Game()
game.load_lexicon(verb_file='wordmappings')
game.create_item('microwave', aliases=['oven'], container=True)
game.create_item('table', container=True, preposition='on')
game.containers['microwave'].on = False
game.containers['microwave'].open = False
game.containers['microwave'].description = lambda: 'You inspect the microwave. It has a door and a start button.'
game.create_item('egg', 'table')
game.create_item('soup', 'table', aliases=['stew', 'brew'])
game.items['egg'].temperature = 'cold'
game.items['egg'].explosive = True
game.items['egg'].description = lambda: 'It looks like a normal egg.'
game.items['soup'].temperature = 'cold'
game.items['soup'].explosive = False
game.items['soup'].description = lambda: 'You inspect the bowl of {0} soup.'.format(game.items['soup'].temperature)


game.add_universal_action('start', start, 1)
game.add_universal_action('stop', stop, 1)

game.events.append(cook_contents(game.containers['microwave']))
game.events.append(left_open(game.containers['microwave']))

game.generate_actions_template()
game.init_env()
game.run()

