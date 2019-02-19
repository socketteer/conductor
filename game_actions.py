from event import *
from gameutil import *


def put(item, container):
    return Event(preconditions=[portable_precondition(item),
                                location_accessible_precondition(item.location),
                                item_not_in_precondition(item, container),
                                container_precondition(container),
                                location_accessible_precondition(container)],
                 effects=[get_effect(item),
                          put_effect(item, container)])


def get(item):
    return Event(preconditions=[portable_precondition(item),
                                [lambda game: not item_in(item, game.inventory),
                                 "{0}{1} is in your inventory".format(item.article, item.name)],
                                location_accessible_precondition(item.location)],
                 effects=[get_effect(item)])


def drop(item):
    return Event(preconditions=[portable_precondition(item),
                                [lambda game: item_in(item, game.inventory),
                                 "{0}{1} is not in your inventory".format(item.article, item.name)]],
                 effects=[drop_effect(item)])


def open(container):
    return Event(preconditions=[openable_precondition(container),
                                closed_precondition(container)],
                 effects=[open_effect(container)])


def close(container):
    return Event(preconditions=[openable_precondition(container),
                                open_precondition(container)],
                 effects=[close_effect(container)])


def inspect(item):
    return Event(preconditions=[],
                 effects=[inspect_effect(item)])
