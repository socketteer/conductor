import txtvrse
from txtvrse import Event


def put(item, container):
    return Event(preconditions={'portable': txtvrse.portable_precondition(item),
                                'item_location_accessible': txtvrse.location_accessible_precondition(item),
                                'container': txtvrse.container_precondition(container),
                                'item_not_in_container': txtvrse.item_not_in_precondition(item, container),
                                'container_accessible': txtvrse.container_accessible_precondition(container),
                                'container_location_accessible': txtvrse.location_accessible_precondition(container)},
                 effects={'get': txtvrse.get_effect(item),
                          'put': txtvrse.put_effect(item, container)})


def get(item):
    return Event(preconditions={'portable': txtvrse.portable_precondition(item),
                                'not_in_inventory': [lambda game: not txtvrse.item_in(game.items[item.id], game.inventory),
                                                     lambda game: "{0}{1} is in your inventory".format(game.items[item.id].article,
                                                                                                       game.items[item.id].name)],
                                'location_accessible': txtvrse.location_accessible_precondition(item)},
                 effects={'get': txtvrse.get_effect(item)})


def drop(item):
    return Event(preconditions={'portable': txtvrse.portable_precondition(item),
                                'in_inventory': [lambda game: txtvrse.item_in(game.items[item.id], game.inventory),
                                                 lambda game: "{0}{1} is not in your inventory".format(game.items[item.id].article,
                                                                                                       game.items[item.id].name)]},
                 effects={'drop': txtvrse.drop_effect(item)})


def open(container):
    return Event(preconditions={'can_open': txtvrse.openable_precondition(container),
                                'closed': txtvrse.closed_precondition(container)},
                 effects={'open': txtvrse.open_effect(container)})


def close(container):
    return Event(preconditions={'can_open': txtvrse.openable_precondition(container),
                                'open': txtvrse.open_precondition(container)},
                 effects={'close': txtvrse.close_effect(container)})


def inspect(item):
    return Event(preconditions={},
                 effects={'inspect': txtvrse.inspect_effect(item)})
