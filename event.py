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
        #print('querying event "{0}"'.format(self.description()))
        '''
        for predicate in self.preconditions:
            if predicate.definition():
                pass
                #print(predicate.true_description())
            else:
                print(predicate.false_description(), 'so the event "{0}" does not occur'.format(self.description()))
                return False
        print('event "{0}" occurs'.format(self.description()))
        self.execute()
        return True
        '''

        if all(predicate.definition() is True for predicate in self.preconditions):
            print(self.description())
            self.execute()
            return True
        else:
            return False

    def execute(self):
        for effect in self.effects:
            effect()

class Precondition:
    def __init__(self, definition, true_description="", false_description=""):
        self.definition = definition
        self.true_description = true_description
        self.false_description = false_description

    def negation(self):
        return Precondition(lambda: not self.definition(),
                            self.false_description,
                            self.true_description)

class Effect:
    def __init__(self, definition, description):
        self.definition = definition
        self.description = description