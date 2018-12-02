def clause(predicates):
    return lambda: any(predicate() is True for predicate in predicates)


class Event:
    def __init__(self, preconditions, effects):
        """
        :param preconditions: expressions which all must return true for event to occur
        :param effects: effects of event -- methods to execute if event occurs
        """
        self.preconditions = preconditions
        self.effects = effects
        #self.description = description

    def query(self):
        #print('querying event "{0}"'.format(self.description()))

        if all(predicate() is True for predicate in self.preconditions):
            self.execute()
            return True
        else:
            return False

    def execute(self):
        for effect in self.effects:
            effect()
