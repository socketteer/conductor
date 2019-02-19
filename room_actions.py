from event import *
from roomutil import *
from gameutil import *


def go(portal):
    go_event = Event(preconditions=[[lambda game: hasattr(portal, 'destination'), "You cannot go there."],
                                    [lambda game: not game.current_location == portal.destination,
                                     "You are already in the {}.".format(portal.destination.name)],
                                    item_in_room_precondition(portal)],
                     effects=[[lambda game: game.change_location(portal.destination),
                               "You go to the {0}.".format(portal.destination.name)]])
    return go_event


def get(item):
    return Event(preconditions=[item_in_room_precondition(item),
                                portable_precondition(item),
                                item_not_in_precondition(item),
                                location_accessible_precondition(item.location)],
                 effects=[room_get_effect(item)])


def drop(item):
    return Event(preconditions=[portable_precondition(item),
                                item_in_precondition(item)],
                 effects=[room_drop_effect(item)])


def put(item, container):
    return Event(preconditions=[portable_precondition(item),
                                location_accessible_precondition(item.location),
                                item_accessible_precondition(item),
                                item_not_in_precondition(item, container),
                                container_precondition(container),
                                location_accessible_precondition(container)],
                 effects=[room_put_effect(item, container)])
