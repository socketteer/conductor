import gameutil
import debug_util
import nlgen

def room_look_util(room):
    floor_items = enumerate_items(room.floor)
    #wall_items = enumerate_items(room.walls)
    description = "You see:\n"
    description += nlgen.nlitemlist(floor_items[1:])
    description += '\n' + nlgen.nlitemlist(list(room.walls.items))
    return description


def enumerate_items(root, items=None):
    if not items:
        items = []
    items.append(root)
    if hasattr(root, 'items'):
        for item in root.items:
            items = enumerate_items(item, items)
    return items


def add_to_container(item, container):
    container.items.add(item)


def remove_from_container(item, container):
    container.items.remove(item)


def drop_util(item, room):
    gameutil.put_util(item, room.floor)
    add_to_container(item, room)


def get_util(item, inventory, room):
    gameutil.put_util(item, inventory)
    remove_from_container(item, room)


def room_put_util(item, room, destination):
    gameutil.put_util(item, destination)
    if item not in room.items:
        add_to_container(item, room)


def open_door_util(door):
    door.open = True


def close_door_util(door):
    door.open = False


def enter_door_util(portal):
    if portal.door:
        portal.door.open = True


def passable_util(portal):
    if not portal.door:
        return True
    else:
        return not portal.door.locked

"""
precondition templates
"""


def item_in_room_precondition(item):
    return [lambda game: game.items[item.id] in game.current_location.items,
            lambda game: 'There is no {0} at your location.'.format(game.items[item.id].name)]


def item_accessible_precondition(item):
    return [lambda game: game.items[item.id] in game.current_location.items
                         or game.items[item.id] in game.inventory.items,
            lambda game: 'You cannot access a {0}.'.format(game.items[item.id].name)]


def passable_precondition(portal):
    return [lambda game: passable_util(game.items[portal.id]),
            lambda game: 'The {0} is locked.'.format(game.items[portal.id].name)]

"""
effect templates
"""


def room_drop_effect(item):
    return [lambda game: drop_util(game.items[item.id], game.current_location),
            lambda game: 'You drop the {0}.'.format(game.items[item.id].name)]


def room_get_effect(item):
    return [lambda game: get_util(game.items[item.id], game.inventory, game.current_location),
            lambda game: 'You get the {0}.'.format(game.items[item.id].name)]


def access_inventory_effect():
    return [lambda game: None,
            lambda game: gameutil.list_container_contents(game.current_location)]


def room_put_effect(item, destination):
    return [lambda game: room_put_util(game.items[item.id], game.current_location, game.items[destination.id]),
            lambda game: 'You put the {0} in the {1}.'.format(game.items[item.id].name,
                                                              game.items[destination.id].name)]


def open_door_effect(item):
    return [lambda game: open_door_util(game.items[item.id].door),
            lambda game: 'You open the {0}'.format(game.items[item.id].name)]


def close_door_effect(item):
    return [lambda game: close_door_util(game.items[item.id].door),
            lambda game: 'You close the {0}'.format(game.items[item.id].name)]


def enter_door_effect(portal):
    return [lambda game: enter_door_util(game.items[portal.id]),
            lambda game: '']
