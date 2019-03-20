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

    def query(self, game):
        """
        :param game:
        :return: whether event is executed, message from predicate which failed
                or None
        """
        for predicate in self.preconditions.values():
            success = predicate[0](game)
            if not success:
                return False, predicate[1](game)
        return True, None

    def execute(self, game):
        """
        :param game:
        :return:
        """
        msg = ""
        for effect in self.effects.values():
            effect[0](game)
            msg += effect[1](game)
        return msg


