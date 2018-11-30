class Env:
    def __init__(self, events, max_steps=None):
        self.events = events
        self.max_steps = max_steps
        self.time = 0

    def step(self):
        state_change = 0
        for event in self.events:
            if event.query():
                state_change = 1
        return state_change

    def run(self):
        while self.step():
            self.time += 1
            if self.max_steps:
                if self.time >= self.max_steps:
                    print("step limit ({0}) reached".format(self.max_steps))
                    return
        print("total steps to reach equilibrium: {0}".format(self.time))
