from room import RoomGame
import catalogue
import roomutil
from debug_util import *

game = RoomGame()
game.load_lexicon(verb_file='wordmappings')
foyer = game.create_room('foyer')
game.alter_attributes(foyer, aliases=['hallway', 'entryway'])
living_room = game.create_room(name='living_room')
dining_room = game.create_room(name='dining_room')
kitchen = game.create_room(name='kitchen')
downstairs_bathroom = game.create_room('bathroom')
mystery_room = game.create_room('mystery_room')
basement = game.create_room('basement')
game.alter_attributes(basement, aliases=['cellar'])
upstairs_hallway = game.create_room('hallway')
small_bedroom = game.create_room('bedroom')
upstairs_bathroom = game.create_room('bathroom')
medium_bedroom = game.create_room('bedroom')
large_bedroom = game.create_room('bedroom')
garage = game.create_room('garage')
shoes = game.create_item('shoes',
                         room=foyer,
                         article="",
                         portable=True)
game.alter_attributes(shoes, aliases=['boots', 'footwear'], attributes=['stinky'])

kitchen_foyer, foyer_kitchen = game.link_rooms(foyer, kitchen)
living_foyer, foyer_living = game.link_rooms(foyer, living_room)
dining_living, living_dining = game.link_rooms(living_room, dining_room)
kitchen_dining, dining_kitchen = game.link_rooms(dining_room, kitchen)
bath_kitchen, kitchen_bath = game.link_rooms(kitchen, downstairs_bathroom, door=True)
kitchen_basement, basement_kitchen = game.link_rooms(basement, kitchen)
kitchen_mystery, mystery_kitchen = game.link_rooms(mystery_room, kitchen)
upstairs_foyer, foyer_upstairs = game.link_rooms(foyer, upstairs_hallway)
game.alter_attributes(upstairs_foyer, aliases=['upstairs', 'stairs', 'up'])
game.alter_attributes(foyer_upstairs, aliases=['downstairs', 'stairs', 'down'])

hallway_bathroom, bathroom_hallway = game.link_rooms(upstairs_bathroom, upstairs_hallway)
hallway_sbr, sbr_hallway = game.link_rooms(small_bedroom, upstairs_hallway)
hallway_mbr, mbr_hallway = game.link_rooms(medium_bedroom, upstairs_hallway)
hallway_lbr, lbr_hallway = game.link_rooms(large_bedroom, upstairs_hallway)

fridge = game.add_item(catalogue.Refrigerator(items_dict=game.items), room=kitchen)
game.alter_attributes(fridge, attributes=['white', 'big'])
cheese = game.create_item('cheese',
                          room=kitchen,
                          location=fridge,
                          portable=True)
counter = game.add_item(catalogue.Counter(items_dict=game.items), room=kitchen)


go_upstairs = game.generate_action('go', upstairs_foyer)
go_downstairs = game.generate_action('go', foyer_upstairs)

go_upstairs.effects['change_location'][1] = lambda game: "You go upstairs."
go_downstairs.effects['change_location'][1] = lambda game: "You go downstairs."


game.init_game_state(foyer)
game.run()