import debug_util

"""
custom exceptions
"""


class InvalidOperation(Exception):
    pass


class NoGenerator(Exception):
    pass


"""
event utils
"""


def open_util(container):
    container.open = True


def close_util(container):
    container.open = False


def accessible(container):
    return (not hasattr(container, 'open')) or container.open


def item_in(item, container):
    return item.location == container


def description_util(item):
    if hasattr(item, 'description'):
        return item.description()
    else:
        return 'It is a {0}'.format(item.name)


def put_util(item, dest):
    if hasattr(item, 'location'):
        item.location.items.remove(item)
    dest.items.add(item)
    item.location = dest


def inspect_util(item):
    pass


def look_util(containers):
    for container in containers:
        if hasattr(container, 'description'):
            print(container.description())
        else:
            print('you see the {0}'.format(container.name))
        if hasattr(container, 'items') and container.items:
            if accessible(container):
                look_util(container.items)


def list_container_contents(container):
    if container.items:
        description = "the {0} contains:".format(container.name)
        for item in container.items:
            description += '\n'
            description += item.name
    else:
        description = "the {0} is empty.".format(container.name)
    return description


"""
precondition templates
"""


def portable_precondition(item):
    return [lambda game: game.items[item.id].portable,
            lambda game: '{0} is not portable'.format(game.items[item.id].name)]


def container_accessible_precondition(container):
    return [lambda game: accessible(game.items[container.id]),
            lambda game: 'the {0} is not accessible.'.format(game.items[container.id].name)]


def container_precondition(container):
    return [lambda game: hasattr(game.items[container.id], 'items'),
            lambda game: '{0} is not a container'.format(game.items[container.id].name)]


def location_accessible_precondition(item):
    return [lambda game: not hasattr(game.items[item.id], 'location') or accessible(game.items[item.location.id]),
            lambda game: 'you cant access the {0}'.format(game.items[item.id].name)]


def openable_precondition(container):
    return [lambda game: hasattr(game.items[container.id], 'open'),
            lambda game: '{0} is not able to be opened or closed'.format(game.items[container.id].name)]


def closed_precondition(container):
    return [lambda game: not game.items[container.id].open,
            lambda game: 'the {0} is open'.format(game.items[container.id].name)]


def open_precondition(container):
    return [lambda game: game.items[container.id].open,
            lambda game: 'the {0} is closed'.format(game.items[container.id].name)]


def item_in_precondition(item, container):
    return [lambda game: item_in(game.items[item.id], game.items[container.id]),
            lambda game: 'the {0} is not in the {1}'.format(game.items[item.id].name, game.items[container.id].name)]


def item_not_in_precondition(item, container):
    return [lambda game: not item_in(game.items[item.id], game.items[container.id]),
            lambda game: 'the {0} is in the {1}'.format(game.items[item.id].name, game.items[container.id].name)]



"""
effect templates
"""


def get_effect(item):
    return [lambda game: put_util(game.items[item.id], game.inventory),
            lambda game: 'you take the {0}'.format(game.items[item.id].name)]


def put_effect(item, container):
    return [lambda game: put_util(game.items[item.id], game.items[container.id]),
            lambda game: 'you put the {0} {1} the {2}'.format(game.items[item.id].name,
                                                              container.preposition,
                                                              game.items[container.id].name)]


def inspect_effect(item):
    return [lambda game: None,
            lambda game: description_util(game.items[item.id])]


def drop_effect(item):
    return [lambda game: put_util(game.items[item.id], game.floor),
            lambda game: 'you drop the {0}'.format(game.items[item.id].name)]


def open_effect(container):
    return [lambda game: open_util(game.items[container.id]),
            lambda game: 'you open the {0}'.format(game.items[container.id].name)]


def close_effect(container):
    return [lambda game: close_util(game.items[container.id]),
            lambda game: 'you close the {0}'.format(game.items[container.id].name)]


def access_inventory_effect():
    return[lambda game: None,
           lambda game: list_container_contents(game.inventory)]
