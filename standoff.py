from event import *


def kill(target, others):
    for cowboy in others:
        cowboy.pointing_gun_at[target.name] = False
    target.die()
    print('{0} is dead'.format(target.name))


def threaten(aggressor, target):
    aggressor.point_gun_at(target.name)
    print('{0} points his gun at {1}'.format(aggressor.name, target.name))


def kill_event(aggressor, target, cowboys):
    return Event(preconditions=[lambda: not aggressor.dead,
                                lambda: not target.dead,
                                lambda: aggressor.pointing_gun_at[target.name],
                                lambda: not any(cowboy.pointing_gun_at[target.name] for cowboy in cowboys - {aggressor, target})],
                 effects=[lambda: print('{0} shoots {1}'.format(aggressor.name, target.name)),
                          lambda: kill(target, cowboys - {target})])


def threaten_event(aggressor, target, cowboys):
    return Event(preconditions=[lambda: not aggressor.dead,
                                lambda: not target.dead,
                                lambda: not aggressor.pointing_gun_at[target.name],
                                lambda: not any(aggressor.pointing_gun_at[cowboy.name] for cowboy in cowboys - {aggressor})],
                 effects=[lambda: threaten(aggressor, target)])


class Cowboy:
    def __init__(self, name):
        self.name = name
        self.pointing_gun_at = {}
        self.dead = False

    def die(self):
        self.dead = True
        for cowboy in self.pointing_gun_at:
            self.pointing_gun_at[cowboy] = False

    def point_gun_at(self, target):
        for cowboy in self.pointing_gun_at:
            self.pointing_gun_at[cowboy] = False
        self.pointing_gun_at[target] = True