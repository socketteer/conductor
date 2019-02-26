class Narrative:
    def __init__(self, world):
        self.world = world
        self.clock = 0
        self.scenes = {}
        self.vars = {}
        self.current_scenes = []


class Scene:
    def __init__(self, events, start_location):
        self.events = []
        self.start_location = start_location

    def start(self, narrative, world):
        world.current_location = self.start_location

    def end(self, narrative, world):
        pass

    def prompt(self, narrative, world):
        pass

    def query_events(self):
        state_change = 0
        for event in self.events:
            success, event, predicate = event.query()
            if success:
                event.report_success()
                state_change = 1
        return state_change

