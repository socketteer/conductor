import parse
import lexicon

phrase1 = 'go to the kitchen'
phrase2 = 'hit the fat green boy'
phrase3 = 'eat pie'
phrase4 = 'hit the fat green'
phrase5 = 'hit the fat green boy in the fat head'

lexicon = lexicon.Lexicon()

lexicon.add_word('go', pos='verb')
lexicon.add_word('hit', pos='verb')
lexicon.add_word('eat', pos='verb')
lexicon.add_word('kitchen', pos='noun')
lexicon.add_word('pie', pos='noun')
lexicon.add_word('boy', pos='noun')
lexicon.add_word('head', pos='noun')
lexicon.add_word('green', pos='adjective')
lexicon.add_word('fat', pos='adjective')

try:
    parsed1 = parse.process_input(phrase1, lexicon)
    print(parsed1)
    parsed2 = parse.process_input(phrase2, lexicon)
    print(parsed2)
    parsed3 = parse.process_input(phrase3, lexicon)
    print(parsed3)
    """parsed4 = parse.process_input(phrase4, lexicon)
    print(parsed4)"""
    parsed5 = parse.process_input(phrase5, lexicon)
    print(parsed5[0])
    for obj in parsed5[1]:
        print(obj.noun)
        print(obj.adjectives)
except parse.ParseError as e:
    print(repr(e))


