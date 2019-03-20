from env import Env

# deprecated

class TurnBasedEnv(Env):
    def __init__(self, player_turn, max_steps=None):
        Env.__init__(self, events=[], max_steps=max_steps)
        self.player_turn = player_turn

    def step(self):
        state_change = 0
        for event in self.events:
            success, event, predicate = event.query()
            if success:
                for effect in event.effects:
                    print(effect[1])
                state_change = 1
        return state_change

    def run(self):
        while True:
            self.step()
            self.player_turn()
