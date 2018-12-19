from basicgame import Game
from standoff import *
from event import *

def start_util(item):
    item.on = True


def stop_util(item):
    item.on = False


def start(item):
    return Event(preconditions=[lambda: hasattr(item, 'on'),
                                lambda: not item.on],
                 effects=[lambda: print('you turn the {0} on'.format(item.name)),
                          lambda: start_util(item)])


def stop(item):
    return Event(preconditions=[lambda: hasattr(item, 'on'),
                                lambda: item.on],
                 effects=[lambda: print('you turn the {0} off'.format(item.name)),
                          lambda: stop_util(item)])


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
    return Event(preconditions=[lambda: item.on,
                                lambda: not len(item.contains) == 0],
                 effects=[lambda: cook_contents_util(item)])


def left_open(item):
    return Event(preconditions=[lambda: item.on,
                                lambda: item.open],
                 effects=[lambda:irradiate()])


game = Game()
game.load_lexicon(verb_file='wordmappings')
game.create_item('microwave', aliases=['oven'], container=True)
game.create_item('table', container=True, preposition='on')
game.containers['microwave'].on = False
game.containers['microwave'].open = False
game.create_item('egg', 'table')
game.create_item('soup', 'table', aliases=['stew', 'brew'])
game.items['egg'].temperature = 'cold'
game.items['egg'].explosive = True
game.items['soup'].temperature = 'cold'
game.items['soup'].explosive = False

game.add_universal_action('start', start, 1)
game.add_universal_action('stop', stop, 1)

game.events.append(cook_contents(game.containers['microwave']))
game.events.append(left_open(game.containers['microwave']))

game.generate_actions()
game.init_env()
game.run()
