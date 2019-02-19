def clause(predicates):
    return lambda: any(predicate() is True for predicate in predicates)


'''
class FailedPrecondition(Exception):
    pass
'''

class Event:
    def __init__(self, preconditions, effects):
        """
        :param preconditions: expressions which all must return true for event to occur
        :param effects: effects of event -- methods to execute if event occurs
        """
        self.preconditions = preconditions
        self.effects = effects
        #self.description = description

    def query(self, game):
        """
        :return: returns whether event is executed;
                self, and third return value is predicate which failed
                or None
        """
        for predicate in self.preconditions:
            if not predicate[0](game):
                return False, self, predicate
        self.execute(game)
        return True, self, None

    def execute(self, game):
        for effect in self.effects:
            effect[0](game)

    def report_failure(self, predicate):
        try:
            print(predicate[1])
        except TypeError:
            print("Event:report_failure ERROR: predicate has no description")

    def report_success(self):
        for effect in self.effects:
            try:
                print(effect[1])
            except TypeError:
                pass



