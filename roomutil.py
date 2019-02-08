import gameutil

def room_look_util(room):
    print('You are in the {0}.'.format(room.name))
    gameutil.look_util(room.items)


"""
precondition templates
"""


def item_in_room_precondition(item, room):
    return [lambda: item in room.items, 'there is no {0} at your location'.format(item.name)]


"""
effect templates
"""

