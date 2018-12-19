class Lexicon:
    def __init__(self):
        self.nouns = {}
        self.verbs = {}

    def resolve(self, word, pos='noun'):
        try:
            if pos == 'noun':
                return self.nouns[word]
            elif pos == 'verb':
                return self.verbs[word]
            else:
                print('Lexicon:resolve ERROR: invalid part of speech parameter {0}'.format(pos))
        except KeyError:
            return word

    def read_word_map(self, filename, pos='noun'):
        with open(filename, 'r') as wordmap:
            for line in wordmap:
                words = line.strip('\n').split(' ')
                for word in words:
                    if pos == 'noun':
                        self.nouns[word] = words[0]
                    elif pos == 'verb':
                        self.verbs[word] = words[0]
                    else:
                        print('Lexicon:read_word_map ERROR: invalid part of speech parameter {0}'.format(pos))

    def add_word(self, word, map_to, pos='noun'):
        if pos == 'noun':
            self.nouns[word] = map_to
        elif pos == 'verb':
            self.verbs[word] = map_to
        else:
            print('Lexicon:add_word ERROR: invalid part of speech parameter {0}'.format(pos))

    def print_lexicon(self):
        print('nouns:')
        for key in self.nouns:
            print('{0} -> {1}'.format(key, self.nouns[key]))
        print('\nverbs:')
        for key in self.verbs:
            print('{0} -> {1}'.format(key, self.verbs[key]))



