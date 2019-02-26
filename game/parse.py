import re


class ParseError(Exception):
    pass


class Object:
    def __init__(self):
        self.noun = ""
        self.adjectives = []


# Makes command lowercase, removes punctuation, determiners, and other common extraneous input
def sanitize(user_input):
    """
    # Makes input lowercase, removes punctuation, determiners, and other common extraneous input
    :param user_input:
    :return: result_words:
    """
    clean = user_input.lower()

    alpha = re.compile('[^a-zA-Z1-9_\s]')
    clean = alpha.sub('', clean)

    remove_words = ['i', 'the', 'a', 'will', 'to', 'at', 'in', 'on', 'of', 'into']

    words = clean.split()

    result_words = [word for word in words if word.lower() not in remove_words]
    return result_words


def process_input(user_input, lexicon):
    sanitized_user_input = sanitize(user_input)
    return parse(sanitized_user_input, lexicon)


def parse(phrase, lexicon):
    verb = phrase[0]
    objects = []
    phrase = phrase[1:]
    while phrase:
        obj, phrase = parse_object(phrase, lexicon)
        objects.append(obj)
    return verb, objects


def parse_object(phrase, lexicon):
    """
    :param phrase:
    :param lexicon:
    :return:
    """
    obj = Object()

    i = 0
    while i < len(phrase):
        if phrase[i] in lexicon.adjectives:
            obj.adjectives.append(phrase[i])
        elif phrase[i] in lexicon.nouns:
                obj.noun = phrase[i]
                return obj, phrase[i+1:]
        else:
            raise ParseError('word {0} not valid noun or adjective'.format(phrase[i]))
        i += 1
    raise ParseError('no valid noun found in phrase \"{0}\"'.format(' '.join(phrase)))


