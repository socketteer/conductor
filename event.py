def clause(predicates):
    return lambda: any(predicate() is True for predicate in predicates)

class Event:
    def __init__(self, preconditions, effects, description):
        """
        :param preconditions: expressions which all must return true for event to occur
        :param effects: effects of event -- methods to execute if event occurs
        """
        self.preconditions = preconditions
        self.effects = effects
        self.description = description

    def query(self):
        print('attempting to', self.description())
        for predicate in self.preconditions:
            if predicate.definition():
                print(predicate.true_description())
            else:
                print(predicate.false_description(), 'so the event "{0}" does not occur'.format(self.description()))
                return False
        print('event "{0}" occurs'.format(self.description()))
        self.execute()
        return True
        '''if all(predicate.definition() is True for predicate in self.preconditions):
            self.execute()
            return True
        else:
            return False'''

    def execute(self):
        for effect in self.effects:
            print(effect.description())
            effect.definition()

class Predicate:
    def __init__(self, truth_value):
        self.set(truth_value)

    def set(self, truth_value):
        self.truth_value = truth_value

    def query(self):
        return self.truth_value

class Precondition:
    def __init__(self, definition, true_description, false_description):
        self.definition = definition
        self.true_description = true_description
        self.false_description = false_description

class Effect:
    def __init__(self, definition, description):
        self.definition = definition
        self.description = description

hungry = Predicate(True)
hasfork = Predicate(True)
cannibal = Predicate(False)
evil = Predicate(False)
sick = Predicate(False)

hungry_or_evil = Precondition(clause([hungry.query, evil.query]),
                              lambda: "you are hungry and evil" if (hungry.query() and evil.query()) else ("you are hungry" if hungry.query() else "you are evil"),
                              lambda: "you are neither hungry nor evil")


hasfork_p = Precondition(hasfork.query, lambda: "you have a fork", lambda: "you don't have a fork")

not_hungry_anymore = Effect(lambda: hungry.set(False), lambda: "you are not hungry anymore")


cannibal_or_sick = Effect(lambda: cannibal.query() or sick.set(True),
                          lambda: "you are a cannibal, so you don't get sick" if cannibal.query() else "you get sick because you're not a cannibal")

eat_bob = Event(preconditions=[hungry_or_evil, hasfork_p],
                effects=[not_hungry_anymore, cannibal_or_sick],
                description=lambda: "eat bob")


eat_bob.query()

eat_bob.query()

evil.set(True)

eat_bob.query()
