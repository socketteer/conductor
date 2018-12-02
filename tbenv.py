from env import Env

class TurnBasedEnv(Env):
    def __init__(self, events, player_turn, max_steps=None):
        Env.__init__(self, events, max_steps)
        self.player_turn = player_turn

    def step(self):
        state_change = 0
        if self.player_turn():
            state_change = 1
        for event in self.events:
            if event.query():
                state_change = 1
        return state_change