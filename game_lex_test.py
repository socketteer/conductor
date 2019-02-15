from room import RoomGame

game = RoomGame()
game.load_lexicon(verb_file='wordmappings')
kitchen = game.create_room('kitchen')
#kitchen.description = lambda: "the kitchen is big as hell and full of hot dogs"
bathroom = game.create_room('bathroom')
door = game.link_rooms(kitchen, bathroom)
cheese = game.create_item('cheese', room=kitchen, aliases=['cheddar', 'food'], attributes=['stinky'])
soup = game.create_item('soup', room=kitchen, aliases=['stew', 'food'], attributes=['hot', 'liquid'])
egg = game.create_item('egg', room=bathroom, aliases=['food'], attributes=['hot', 'hard', 'shelled'])
game.init_game_state('kitchen')
game.print_debugging_info()
game.run()
