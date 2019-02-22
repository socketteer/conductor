from event import *
from roomutil import *
from gameutil import *
import game_actions


def go(portal):
    go_event = Event(preconditions={'is_portal': [lambda game: hasattr(portal, 'destination'), "You cannot go there."],
                                    'not_already_in': [lambda game: not game.current_location == portal.destination,
                                                       "You are already in the {}.".format(portal.destination.name)],
                                    'portal_in_room': item_in_room_precondition(portal),
                                    'passable': passable_precondition(portal)},
                     effects={'enter door': enter_door_effect(portal),
                              'change_location': [lambda game: game.change_location(portal.destination),
                                                  "You go to the {0}.".format(portal.destination.name)]})
    return go_event


def get(item):
    return Event(preconditions={'item_in_room': item_in_room_precondition(item),
                                'portable': portable_precondition(item),
                                'not_in_inventory': [lambda game: not item_in(item, game.inventory),
                                                     "{0}{1} is already in your inventory.".format(item.article, item.name)],
                                'location_accessible': location_accessible_precondition(item)},
                 effects={'get': room_get_effect(item)})


def drop(item):
    return Event(preconditions={'portable': portable_precondition(item),
                                'in_inventory': [lambda game: item_in(item, game.inventory),
                                                 "{0}{1} is not in your inventory.".format(item.article, item.name)]},
                 effects={'drop': room_drop_effect(item)})


def put(item, container):
    return Event(preconditions={'portable': portable_precondition(item),
                                'item_location_accessible': location_accessible_precondition(item),
                                'item_accessible': item_accessible_precondition(item),
                                'container': container_precondition(container),
                                'item_not_in_container': item_not_in_precondition(item, container),
                                'container_accessible': container_accessible_precondition(container),
                                'container_location_accessible': location_accessible_precondition(container)},
                 effects={'put': room_put_effect(item, container)})


def open(item):
    if hasattr(item, 'door'):
        return Event(preconditions={'not_open': [lambda game: not game.items[item.id].door.open,
                                                 "{0}{1} is already open.".format(item.article, item.name)],
                                    'not locked': [lambda game: not game.items[item.id].door.locked,
                                                   "{0}{1} is locked".format(item.article, item.name)]},
                     effects={'open': open_door_effect(item)})
    else:
        return game_actions.open(item)


def close(item):
    if hasattr(item, 'door'):
        return Event(preconditions={'open': [lambda game: game.items[item.id].door.open,
                                             "{0}{1} is already closed.".format(item.article, item.name)]},
                     effects={'close': close_door_effect(item)})
    else:
        return game_actions.close(item)