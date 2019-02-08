import entityresolution
import lexicon
import item

# init lexicon

lex = lexicon.Lexicon()

# init objects
items = {}

danny = item.Item(name='danny', attributes=['stupid', 'strong', 'sexy'], aliases=['dan', 'boy', 'pirate', 'human'])
items['danny'] = danny
andy = item.Item(name='andy', attributes=['scary', 'strong', 'studious'], aliases=['criminal', 'boy', 'pirate', 'human'])
items['andy'] = andy
arnold = item.Item(name='arnold', attributes=['smart', 'studious', 'insane'], aliases=['boy', 'student', 'human'])
items['arnold'] = arnold
becky = item.Item(name='becky', attributes=['insane', 'strong', 'sexy'], aliases=['beck', 'girl', 'pirate', 'human'])
items['becky'] = becky
cindy = item.Item(name='cindy', attributes=['smart', 'strange', 'cynical'], aliases=['cindy', 'girl', 'student', 'human'])
items['cindy'] = cindy

# test phrases
print('danny: {0}'.format(entityresolution.resolve_phrase('danny', [], items, lex).name))
print('dan: {0}'.format(entityresolution.resolve_phrase('dan', [], items, lex).name))
print('stupid dan: {0}'.format(entityresolution.resolve_phrase('dan', ['stupid'], items, lex).name))
#print("strong pirate: {0}".format(entityresolution.resolve_phrase('pirate', ['strong'], items, lex).name))
#print("cynical pirate: {0}".format(entityresolution.resolve_phrase('pirate', ['cynical'], items, lex).name))
print("cynical human: {0}".format(entityresolution.resolve_phrase('human', ['cynical'], items, lex).name))
print("smart girl: {0}".format(entityresolution.resolve_phrase('girl', ['smart'], items, lex).name))
print("strong stupid boy: {0}".format(entityresolution.resolve_phrase('boy', ['strong', 'stupid'], items, lex).name))
#print("smart stupid human: {0}".format(entityresolution.resolve_phrase('human', ['smart', 'stupid'], items, lex).name))