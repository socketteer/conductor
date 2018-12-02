from interactiveenv import InteractiveEnv
from standoff import *
import itertools

def player_kill_event(aggressor, target, cowboys):
    return Event(preconditions=[alive_precondition(aggressor),
                                alive_precondition(target),
                                threatening_precondition(aggressor, target)],
                 effects=[kill_effect(aggressor, target, cowboys - {target})],
                 description=lambda: "{0} kills {1}".format(aggressor.name, target.name))


def player_threaten_event(aggressor, target):
    return Event(preconditions=[alive_precondition(aggressor),
                                alive_precondition(target),
                                threatening_precondition(aggressor, target).negation()],
                 effects=[threaten_effect(aggressor, target)],
                 description=lambda: "{0} threatens {1}".format(aggressor.name, target.name))

player = Cowboy("player")
phil = Cowboy("phil")
randy = Cowboy("randy")

#initial conditions
player.pointing_gun_at["randy"] = False
player.pointing_gun_at["phil"] = False
phil.pointing_gun_at["player"] = False
phil.pointing_gun_at["randy"] = False
randy.pointing_gun_at["player"] = False
randy.pointing_gun_at["phil"] = False

cowboys = {player, phil, randy}

env_events = []
player_threaten_events = {}
player_kill_events = {}

for first, second in itertools.permutations(cowboys - {player}, 2):
    env_events.append(kill_event(first, second, cowboys))
    env_events.append(threaten_event(first, second, cowboys))

for cowboy in cowboys - {player}:
    env_events.append(kill_event(cowboy, player, cowboys))
    player_kill_events[cowboy.name] = player_kill_event(player, cowboy, cowboys)
    env_events.append(threaten_event(cowboy, player, cowboys))
    player_threaten_events[cowboy.name] = player_threaten_event(player, cowboy)

def get_input():
    user_input = input('\n>')
    return user_input.split()

def player_turn():
    if player.dead:
        return False
    else:
        input = get_input()
        action = input[0]
        if len(input) > 1:
            target = input[1]
        if action == "shoot" or action == "kill":
            if not player_kill_events[target].query():
                print('that is not possible')
                return player_turn()
            else:
                return True
        elif action == "threaten":
            if not player_threaten_events[target].query():
                print('that is not possible')
                return player_turn()
            else:
                return True
        elif action == "pass":
            return False
        elif action == "look":
            alive = {c for c in cowboys if not c.dead}
            for c in alive:
                print('{0} is still alive'.format(c.name))
            for f, s in itertools.permutations(alive, 2):
                if f.pointing_gun_at[s.name]:
                    print('{0} is threatening {1}'.format(f.name, s.name))
            return player_turn()
        elif action == "quit":
            quit()
        else:
            print('invalid input')
            return player_turn()


standoff = InteractiveEnv(env_events, player_turn)
print("You confront randy and phil.")
standoff.run()
