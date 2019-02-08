from room import RoomGame

game = RoomGame()
game.load_lexicon(verb_file='wordmappings')
kitchen = game.create_room('kitchen')
kitchen.description = lambda: "the kitchen is big as hell and full of hot dogs"
bathroom = game.create_room('bathroom')
door = game.link_rooms(kitchen, bathroom)
game.init_game_state('kitchen')
game.print_debugging_info()
game.run()
