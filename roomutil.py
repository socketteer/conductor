import gameutil


def room_look_util(room):
    print(room.description())


def enumerate_items(room):
    descriptions = ""
    for item in room.items:
        if hasattr(item, 'location') and gameutil.accessible(item.location):
            descriptions += ' '
            descriptions += item.description()

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

def list_container_contents(container):
    if container.items:
        description = "The {0} contains:".format(container.name)
        for item in container.items:
            description += '\n'
            description += item.name
    else:
        description = "The {0} is empty.".format(container.name)
    return description

def room_put_util(item, room, destination):
    gameutil.put_util(item, destination)
    if item not in room.items:
        add_to_container(item, room)


"""
precondition templates
"""


def item_in_room_precondition(item, room):
    return [lambda: item in room.items, 'there is no {0} at your location'.format(item.name)]


def item_accessible_precondition(item, room, inventory):
    return [lambda: item in room.items or item in inventory.items, 'you cannot access a {0}'.format(item.name)]

"""
effect templates
"""


def room_drop_effect(item, room):
    return [lambda: drop_util(item, room), 'you drop the {0}'.format(item.name)]


def room_get_effect(item, inventory, room):
    return [lambda: get_util(item, inventory, room), 'you get the {0}'.format(item.name)]


def access_inventory_effect(inventory):
    return[lambda: print(list_container_contents(inventory)), '']


def room_put_effect(item, room, destination):
    return[lambda: room_put_util(item, room, destination),
           'you put the {0} in the {1}'.format(item.name, destination.name)]
