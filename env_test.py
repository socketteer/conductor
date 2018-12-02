from basicgame import Game
from item import Item, Container
from event import *


def start_util(item):
    item.on = True


def stop_util(item):
    item.on = False


def start(item):
    return Event(preconditions=[lambda: not item.on],
                 effects=[lambda: start_util(item)])


def stop(item):
    return Event(preconditions=[lambda: item.on],
                 effects=[lambda: stop_util(item)])

def cook(item):
    if(item.temperature == 'cold'):
        item.temperature = 'hot'
    elif(item.temperature == 'hot'):
        item.temperature = 'super hot'
    elif(item.temperature == 'super hot'):
        explode()
        return
    if(item.explosive):
        explode()


def explode():
    print('the microwave explodes and you die')
    quit()

cook_contents = Event(preconditions = [],
                      effects = [])

events = [cook_contents]

game = Game(events)
game.items['egg'] = Item('egg')
game.items['soup'] = Item('soup')
game.containers['table'] = Container('table', 'on')
game.containers['microwave'] = Container('microwave')
game.containers['microwave'].on = False
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

game.generate_actions()
game.run()
