import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import txtvrse

housegame = txtvrse.room.RoomGame()
housegame.load_lexicon(verb_file='txtvrse/wordmappings')
foyer = housegame.create_room('foyer')
housegame.alter_attributes(foyer, aliases=['hallway', 'entryway'])
living_room = housegame.create_room(name='living_room')
dining_room = housegame.create_room(name='dining_room')
kitchen = housegame.create_room(name='kitchen')
downstairs_bathroom = housegame.create_room('bathroom')
mystery_room = housegame.create_room('mystery_room')
basement = housegame.create_room('basement')
housegame.alter_attributes(basement, aliases=['cellar'])
upstairs_hallway = housegame.create_room('hallway')
small_bedroom = housegame.create_room('bedroom')
upstairs_bathroom = housegame.create_room('bathroom')
medium_bedroom = housegame.create_room('bedroom')
large_bedroom = housegame.create_room('bedroom')
garage = housegame.create_room('garage')
shoes = housegame.create_item('shoes',
                              room=foyer,
                              article="",
                              portable=True)
housegame.alter_attributes(shoes, aliases=['boots', 'footwear'], attributes=['stinky'])

kitchen_foyer, foyer_kitchen = housegame.link_rooms(foyer, kitchen)
living_foyer, foyer_living = housegame.link_rooms(foyer, living_room)
dining_living, living_dining = housegame.link_rooms(living_room, dining_room)
kitchen_dining, dining_kitchen = housegame.link_rooms(dining_room, kitchen)
bath_kitchen, kitchen_bath = housegame.link_rooms(kitchen, downstairs_bathroom, door=True)
kitchen_basement, basement_kitchen = housegame.link_rooms(basement, kitchen)
kitchen_mystery, mystery_kitchen = housegame.link_rooms(mystery_room, kitchen)
upstairs_foyer, foyer_upstairs = housegame.link_rooms(foyer, upstairs_hallway)
housegame.alter_attributes(upstairs_foyer, aliases=['upstairs', 'stairs', 'up'])
housegame.alter_attributes(foyer_upstairs, aliases=['downstairs', 'stairs', 'down'])

hallway_bathroom, bathroom_hallway = housegame.link_rooms(upstairs_bathroom, upstairs_hallway)
hallway_sbr, sbr_hallway = housegame.link_rooms(small_bedroom, upstairs_hallway)
hallway_mbr, mbr_hallway = housegame.link_rooms(medium_bedroom, upstairs_hallway)
hallway_lbr, lbr_hallway = housegame.link_rooms(large_bedroom, upstairs_hallway)

fridge = housegame.add_item(txtvrse.catalogue.Refrigerator(items_dict=housegame.items), room=kitchen)
housegame.alter_attributes(fridge, attributes=['white', 'big'])
cheese = housegame.create_item('cheese',
                               room=kitchen,
                               location=fridge,
                               portable=True)
counter = housegame.add_item(txtvrse.catalogue.Counter(items_dict=housegame.items), room=kitchen)

go_upstairs = housegame.generate_action('go', upstairs_foyer)
go_downstairs = housegame.generate_action('go', foyer_upstairs)

go_upstairs.effects['change_location'][1] = lambda game: "You go upstairs."
go_downstairs.effects['change_location'][1] = lambda game: "You go downstairs."

housegame.init_game_state(foyer)
housegame.run()
