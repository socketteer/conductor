from basicgame import Game
from item import Item, Container



game = Game()
game.items['egg'] = Item('egg')
game.items['soup'] = Item('soup')
game.containers['table'] = Container('table', 'on')
game.containers['microwave'] = Container('microwave')
game.put_util(game.items['egg'], game.containers['table'])
game.items['egg'].temperature = 'cold'
game.items['egg'].explosive = True
game.put_util(game.items['soup'], game.containers['table'])
game.items['soup'].temperature = 'cold'
game.items['soup'].explosive = False

game.generate_actions()
game.run()
