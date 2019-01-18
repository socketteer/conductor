import event
from basicgame import Game


class Room:
    def __init__(self, name):
        self.items = {}
        self.name = name


class RoomGame(Game):
    def __init__(self, events=[]):
        pass
        #init rooms
        #current location


