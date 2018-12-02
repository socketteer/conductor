import re

# Makes command lowercase, removes punctuation, determiners, and other common extraneous input
def sanitize(user_input):
    '''
    # Makes command lowercase, removes punctuation, determiners, and other common extraneous input
    :param user_input:
    :return:
    '''
    clean = user_input.lower()

    alpha = re.compile('[^a-zA-Z1-9_\s]')
    clean = alpha.sub('', clean)

    remove_words = ['i', 'the', 'a', 'will', 'to', 'at', 'in', 'on', 'of', 'into']

    words = clean.split()

    result_words = [word for word in words if word.lower() not in remove_words]
    return result_words