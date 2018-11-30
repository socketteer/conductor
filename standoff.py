from event import *

def threatening_precondition(aggressor, target):
    return Precondition(lambda: aggressor.pointing_gun_at[target.name],
                        lambda: "{0} is threatening {1}".format(aggressor.name, target.name),
                        lambda: "{0} is not threatening {1}".format(aggressor.name, target.name))

def threatening_anyone_precondition(aggressor, others):
    return Precondition(lambda: any(aggressor.pointing_gun_at[cowboy.name] for cowboy in others),
                        lambda: "{0} is threatening someone".format(aggressor.name),
                        lambda: "{0} is not threatening anyone".format(aggressor.name))

def threatened_precondition(target, others):
    return Precondition(lambda: any(cowboy.pointing_gun_at[target.name] for cowboy in others),
                        lambda: "{0} is being threatened".format(target.name),
                        lambda: "{0} is not being threatened".format(target.name))

def alive_precondition(cowboy):
    return Precondition(lambda: not cowboy.dead,
                        lambda: "{0} is alive".format(cowboy.name),
                        lambda: "{0} is dead".format(cowboy.name))

def kill(target, others):
    for cowboy in others:
        cowboy.pointing_gun_at[target.name] = False
    target.die()

def kill_effect(aggressor, target, others):
    return Effect(lambda: kill(target, others),
                  lambda: "{0} is dead, killed by {1}".format(target.name, aggressor.name))

def threaten(aggressor, target):
    aggressor.point_gun_at(target.name)

def threaten_effect(aggressor, target):
    return Effect(lambda: threaten(aggressor, target),
                  lambda: "{0} threatens {1}".format(aggressor.name, target.name))

def kill_event(aggressor, target, cowboys):
    return Event(preconditions=[alive_precondition(aggressor),
                                alive_precondition(target),
                                threatening_precondition(aggressor, target),
                                threatened_precondition(aggressor, cowboys - {aggressor, target}).negation()],
                 effects=[kill_effect(aggressor, target, cowboys - {target})],
                 description=lambda: "{0} kills {1}".format(aggressor.name, target.name))


def threaten_event(aggressor, target, cowboys):
    return Event(preconditions=[alive_precondition(aggressor),
                                alive_precondition(target),
                                threatening_precondition(aggressor, target).negation(),
                                threatening_anyone_precondition(aggressor, cowboys - {aggressor}).negation()],
                 effects=[threaten_effect(aggressor, target)],
                 description=lambda: "{0} threatens {1}".format(aggressor.name, target.name))

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



