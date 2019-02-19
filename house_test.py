from room import RoomGame
from debug_util import *


game = RoomGame()
game.load_lexicon(verb_file='wordmappings')
foyer = game.create_room('foyer', aliases=['hallway'])
living_room = game.create_room(name='living_room')
dining_room = game.create_room(name='dining_room')
kitchen = game.create_room(name='kitchen')
downstairs_bathroom = game.create_room('bathroom')
mystery_room = game.create_room('mystery_room')
basement = game.create_room('basement', aliases=['cellar'])
upstairs_hallway = game.create_room('hallway')
small_bedroom = game.create_room('bedroom', aliases=['room'], attributes=['small'])
upstairs_bathroom = game.create_room('bathroom', aliases=['room'])
medium_bedroom = game.create_room('bedroom', aliases=['room'], attributes=['medium'])
large_bedroom = game.create_room('bedroom', aliases=['room'], attributes=['large', 'big'])
garage = game.create_room('garage')
shoes = game.create_item('shoes', aliases=['boots', 'footwear'], attributes=['stinky'], room=foyer, article="")


kitchen_foyer, foyer_kitchen = game.link_rooms(foyer, kitchen)
living_foyer, foyer_living = game.link_rooms(foyer, living_room)
dining_living, living_dining = game.link_rooms(living_room, dining_room)
kitchen_dining, dining_kitchen = game.link_rooms(dining_room, kitchen)
bath_kitchen, kitchen_bath = game.link_rooms(kitchen, downstairs_bathroom)
kitchen_basement, basement_kitchen = game.link_rooms(basement, kitchen)
kitchen_mystery, mystery_kitchen = game.link_rooms(mystery_room, kitchen)
upstairs_foyer, foyer_upstairs = game.link_rooms(foyer, upstairs_hallway)
game.alter_attributes(upstairs_foyer, aliases=['upstairs', 'stairs'])
game.alter_attributes(foyer_upstairs, aliases=['downstairs', 'stairs'])

hallway_bathroom, bathroom_hallway = game.link_rooms(upstairs_bathroom, upstairs_hallway)
hallway_sbr, sbr_hallway = game.link_rooms(small_bedroom, upstairs_hallway)
hallway_mbr, mbr_hallway = game.link_rooms(medium_bedroom, upstairs_hallway)
hallway_lbr, lbr_hallway = game.link_rooms(large_bedroom, upstairs_hallway)

game.create_item(name='refrigerator', room=kitchen, aliases=['fridge'], container=True)

game.init_game_state(foyer)

go_upstairs = game.action_generators['go'](upstairs_foyer)
#go_upstairs.effects[0][1] = "You go up the stairs."
go_downstairs = game.action_generators['go'](foyer_upstairs)

print('current location: ', game.current_location.id)
game.exe(go_upstairs)
game.current_location = upstairs_hallway
print('current location: ', game.current_location.id)
game.exe(go_downstairs)
#game.one_operand_actions['go'][foyer_upstairs.id] = game.go(foyer_upstairs)
#go_downstairs.effects[0][1] = "You go down the stairs."
print(go_downstairs.preconditions)
print(go_downstairs.effects)


game.run()