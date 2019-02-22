from event import *
from gameutil import *


def put(item, container):
    return Event(preconditions={'portable': portable_precondition(item),
                                'item_location_accessible': location_accessible_precondition(item),
                                'container': container_precondition(container),
                                'item_not_in_container': item_not_in_precondition(item, container),
                                'container_accessible': container_accessible_precondition(container),
                                'container_location_accessible': location_accessible_precondition(container)},
                 effects={'get': get_effect(item),
                          'put': put_effect(item, container)})


def get(item):
    return Event(preconditions={'portable': portable_precondition(item),
                                'not_in_inventory': [lambda game: not item_in(item, game.inventory),
                                                     "{0}{1} is in your inventory".format(item.article, item.name)],
                                'location_accessible': location_accessible_precondition(item.location)},
                 effects={'get': get_effect(item)})


def drop(item):
    return Event(preconditions={'portable': portable_precondition(item),
                                'in_inventory': [lambda game: item_in(item, game.inventory),
                                                 "{0}{1} is not in your inventory".format(item.article, item.name)]},
                 effects={'drop': drop_effect(item)})


def open(container):
    return Event(preconditions={'can_open': openable_precondition(container),
                                'closed': closed_precondition(container)},
                 effects={'open': open_effect(container)})


def close(container):
    return Event(preconditions={'can_open': openable_precondition(container),
                                'open': open_precondition(container)},
                 effects={'close': close_effect(container)})


def inspect(item):
    return Event(preconditions={},
                 effects={'inspect': inspect_effect(item)})
