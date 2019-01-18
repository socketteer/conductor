"""
good help
"""

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
        item.location.contains.remove(item)
    dest.contains.add(item)
    item.location = dest


def inspect_util(item):
    pass


def look_util(containers):
    for container in containers:
        if hasattr(container, 'description'):
            print(container.description())
        else:
            print('You see the {0}'.format(container.name))
        if hasattr(container, 'contains') and container.contains:
            if accessible(container):
                look_util(container.contains)



"""
precondition templates
"""


def portable_precondition(item):
    return [lambda: item.portable, '{0} is not portable'.format(item.name)]


def container_precondition(container):
    return [lambda: hasattr(container, 'contains'), '{0} is not a container'.format(container.name)]


def location_accessible_precondition(container):
    return [lambda: accessible(container), 'you cant access the {0}'.format(container.name)]


def openable_precondition(container):
    return [lambda: hasattr(container, 'open'), '{0} is not able to be opened or closed'.format(container.name)]


def closed_precondition(container):
    return [lambda: not container.open, 'the {0} is open'.format(container.name)]


def open_precondition(container):
    return [lambda: container.open, 'the {0} is closed'.format(container.name)]


def item_in_precondition(item, container):
    return [lambda: item_in(item, container), 'the {0} is not in the {1}'.format(item.name, container.name)]


def item_not_in_precondition(item, container):
    return [lambda: not item_in(item, container), 'the {0} is in the {1}'.format(item.name, container.name)]


def item_in_room_precondition(item, room):
    return [lambda: item in room.values(), 'there is no {0} at your location'.format(item.name)]

"""
effect templates
"""


def get_effect(item, inventory):
    return [lambda: put_util(item, inventory), 'you take the {0}'.format(item.name)]


def put_effect(item, container):
    return [lambda: put_util(item, container),
            'you put the {0} {1} the {2}'.format(item.name, container.preposition, container.name)]


def inspect_effect(item):
    return [lambda: inspect_util(item), description_util(item)]


def drop_effect(item, floor):
    return [lambda: put_util(item, floor), 'you drop the {0}'.format(item.name)]


def open_effect(container):
    return [lambda: open_util(container), 'you open the {0}'.format(container.name)]


def close_effect(container):
    return [lambda: close_util(container), 'you close the {0}'.format(container.name)]
