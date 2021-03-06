import txtvrse


def go(portal):
    go_event = txtvrse.Event(preconditions={'is_portal': [lambda game: hasattr(game.items[portal.id], 'destination'),
                                                          lambda game: "You cannot go there."],
                                            'not_already_in': [lambda game: not game.current_location == game.items[
                                                portal.id].destination,
                                                               lambda game: "You are already in the {}.".format(
                                                                   game.items[portal.id].destination.name)],
                                            'portal_in_room': txtvrse.item_in_room_precondition(portal),
                                            'passable': txtvrse.passable_precondition(portal)},
                             effects={'enter door': txtvrse.enter_door_effect(portal),
                                      'change_location': [
                                          lambda game: game.change_location(game.items[portal.id].destination),
                                          lambda game: "You go to the {0}.".format(
                                              game.items[portal.id].destination.name)]})
    return go_event


def get(item):
    return txtvrse.Event(preconditions={'item_in_room': txtvrse.item_in_room_precondition(item),
                                        'portable': txtvrse.portable_precondition(item),
                                        'not_in_inventory': [
                                            lambda game: not txtvrse.item_in(game.items[item.id], game.inventory),
                                            lambda game: "{0}{1} is already in your inventory.".format(
                                                game.items[item.id].article,
                                                game.items[item.id].name)],
                                        'location_accessible': txtvrse.location_accessible_precondition(item)},
                         effects={'get': txtvrse.room_get_effect(item)})


def drop(item):
    return txtvrse.Event(preconditions={'portable': txtvrse.portable_precondition(item),
                                        'in_inventory': [
                                            lambda game: txtvrse.item_in(game.items[item.id], game.inventory),
                                            lambda game: "{0}{1} is not in your inventory.".format(
                                                game.items[item.id].article,
                                                game.items[item.id].name)]},
                         effects={'drop': txtvrse.room_drop_effect(item)})


def put(item, container):
    return txtvrse.Event(preconditions={'portable': txtvrse.portable_precondition(item),
                                        'item_location_accessible': txtvrse.location_accessible_precondition(item),
                                        'item_accessible': txtvrse.item_accessible_precondition(item),
                                        'container': txtvrse.container_precondition(container),
                                        'item_not_in_container': txtvrse.item_not_in_precondition(item, container),
                                        'container_accessible': txtvrse.container_accessible_precondition(container),
                                        'container_location_accessible': txtvrse.location_accessible_precondition(
                                            container)},
                         effects={'put': txtvrse.room_put_effect(item, container)})


def open(item):
    if hasattr(item, 'door'):
        return txtvrse.Event(preconditions={'not_open': [lambda game: not game.items[item.id].door.open,
                                                         lambda game: "{0}{1} is already open.".format(
                                                             game.items[item.id].article,
                                                             game.items[item.id].name)],
                                            'not locked': [lambda game: not game.items[item.id].door.locked,
                                                           lambda game: "{0}{1} is locked".format(
                                                               game.items[item.id].article,
                                                               game.items[item.id].name)]},
                             effects={'open': txtvrse.open_door_effect(item)})
    else:
        return txtvrse.game_actions.open(item)


def close(item):
    if hasattr(item, 'door'):
        return txtvrse.Event(preconditions={'open': [lambda game: game.items[item.id].door.open,
                                                     lambda game: "{0}{1} is already closed.".format(
                                                         game.items[item.id].article,
                                                         game.items[item.id].name)]},
                             effects={'close': txtvrse.close_door_effect(item)})
    else:
        return txtvrse.game_actions.close(item)
