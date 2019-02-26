from debug_util import *

class ResolutionFailure(Exception):
    pass


class ResolutionAmbiguity(Exception):
    pass


def resolve_word(word, items, lex):
    #TODO lex resolution
    try:
        return [items[word]]
    except KeyError:
        candidates = []
        for item in items.values():
            if word in item.aliases:
                candidates.append(item)
        return candidates

def filter_by_attributes(attributes, items):
    # TODO resolve adjectives?
    if not attributes:
        return items
    viable = []
    for item in items:
        if all(attribute in item.attributes for attribute in attributes):
            viable.append(item)
    return viable


def resolve_phrase(word, attributes, items, lex):
    # TODO efficient order?
    items = {item.id: item for item in items}
    viable = resolve_word(word, items, lex)
    if len(viable) == 0:
        raise ResolutionFailure('unable to resolve noun {0}'.format(word))
    viable = filter_by_attributes(attributes, viable)
    if len(viable) == 0:
        raise ResolutionFailure('no object called {0} with attributes [{1}]'.format(word, ', '.join(attributes)))
    elif len(viable) == 1:
        return viable[0]
    else:
        raise ResolutionAmbiguity('phrase noun={0}, attributes=[{1}] is ambiguous; could refer '
                                  'to {2} different entities'.format(word, ' ,'.join(attributes), len(viable)),
                                  word,
                                  viable)
