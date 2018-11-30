from env import Env
from standoff import *
import itertools

bob = Cowboy("bob")
phil = Cowboy("phil")
randy = Cowboy("randy")

#initial conditions
#phil wins
bob.pointing_gun_at["randy"] = True
bob.pointing_gun_at["phil"] = False
phil.pointing_gun_at["bob"] = True
phil.pointing_gun_at["randy"] = False
randy.pointing_gun_at["bob"] = True
randy.pointing_gun_at["phil"] = False

#stable init
'''
bob.pointing_gun_at["randy"] = True
bob.pointing_gun_at["phil"] = False
phil.pointing_gun_at["bob"] = True
phil.pointing_gun_at["randy"] = False
randy.pointing_gun_at["bob"] = False
randy.pointing_gun_at["phil"] = True
'''

cowboys = {bob, phil, randy}

events = []
for first, second in itertools.permutations(cowboys, 2):
    events.append(kill_event(first, second, cowboys))
    events.append(threaten_event(first, second, cowboys))

standoff = Env(events)
standoff.run()
