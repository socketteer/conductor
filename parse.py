import re


class ParseError(Exception):
    pass


# Makes command lowercase, removes punctuation, determiners, and other common extraneous input
def sanitize(user_input):
    """
    # Makes command lowercase, removes punctuation, determiners, and other common extraneous input
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


def parse_user_input(user_input, lexicon):
    parsed_command = []
    sanitized_user_input = sanitize(user_input)
    if not sanitized_user_input:
        print('parse_user_input ERROR: sanitized_user_input empty')
        raise ParseError
    parsed_command.append(lexicon.resolve(sanitized_user_input[0], 'verb'))
    if len(sanitized_user_input) > 1:
        parsed_command.append(lexicon.resolve(sanitized_user_input[1], 'noun'))
        if len(sanitized_user_input) > 2:
            parsed_command.append(lexicon.resolve(sanitized_user_input[2], 'noun'))
            if len(sanitized_user_input) > 3:
                print('parse_user_input ERROR: sanitized_user_input contains more than 3 parts')
                raise ParseError
    return len(parsed_command), parsed_command
