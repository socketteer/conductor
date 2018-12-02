from basicgame import Game
from item import Item, Container
from event import *


def start_util(item):
    item.on = True


def stop_util(item):
    item.on = False


def start(item):
    return Event(preconditions=[lambda: not item.on],
                 effects=[lambda: print('you turn the {0} on'.format(item.name)),
                          lambda: start_util(item)])


def stop(item):
    return Event(preconditions=[lambda: item.on],
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
game.items['egg'] = Item('egg')
game.items['soup'] = Item('soup')
game.containers['table'] = Container('table', 'on')
game.containers['microwave'] = Container('microwave')
game.containers['microwave'].on = False
game.containers['microwave'].open = False
game.put_util(game.items['egg'], game.containers['table'])
game.items['egg'].temperature = 'cold'
game.items['egg'].explosive = True
game.put_util(game.items['soup'], game.containers['table'])
game.items['soup'].temperature = 'cold'
game.items['soup'].explosive = False

game.actions['start'] = {}
game.actions['stop'] = {}
game.actions['start']['microwave'] = start(game.containers['microwave'])
game.actions['stop']['microwave'] = stop(game.containers['microwave'])

game.events.append(cook_contents(game.containers['microwave']))
game.events.append(left_open(game.containers['microwave']))

game.generate_actions()
game.run()
