import gameutil
import debug_util

def room_look_util(room):
    print(room.description())


def enumerate_items(room):
    descriptions = ""
    for item in room.items:
        if hasattr(item, 'location') and gameutil.accessible(item.location):
            descriptions += item.description()
            descriptions += ' '
    return descriptions


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
    if hasattr(portal, 'door'):
        portal.door.open = True


def passable_util(portal):
    if not hasattr(portal, 'door'):
        return True
    else:
        return not portal.door.locked

"""
precondition templates
"""


def item_in_room_precondition(item):
    return [lambda game: item in game.current_location.items,
            'There is no {0} at your location.'.format(item.name)]


def item_accessible_precondition(item):
    return [lambda game: item in game.current_location.items or item in game.inventory.items,
            'You cannot access a {0}.'.format(item.name)]


def passable_precondition(portal):
    return [lambda game: passable_util(game.items[portal.id]), 'The {0} is locked.'.format(portal.name)]

"""
effect templates
"""


def room_drop_effect(item):
    return [lambda game: drop_util(item, game.current_location),
            'You drop the {0}.'.format(item.name)]


def room_get_effect(item):
    return [lambda game: get_util(item, game.inventory, game.current_location),
            'You get the {0}.'.format(item.name)]


def access_inventory_effect():
    return [lambda game: print(gameutil.list_container_contents(game.current_location)), '']


def room_put_effect(item, destination):
    return [lambda game: room_put_util(item, game.current_location, destination),
            'You put the {0} in the {1}.'.format(item.name, destination.name)]


def open_door_effect(item):
    return [lambda game: open_door_util(game.items[item.id].door),
            "You open the {0}".format(item.name)]


def close_door_effect(item):
    return [lambda game: close_door_util(game.items[item.id].door),
            "You close the {0}".format(item.name)]


def enter_door_effect(portal):
    return [lambda game: enter_door_util(portal), '']
