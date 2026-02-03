import sys
from fst import FST
from fsmutils import composewords, trace

all_ipa = ['b', 'm', 'ð', 'd', 'ɹ', 'l', 'j', 'v', 'g', 'ŋ', 't', 'n', 'ɑ', 'ɝ',
           'ɛ', 'æ', 'ʌ', 'ʊ', 'ɒ', 'ə', 'e', 'a', 'ɔ', 'o', 'z', 'd', 'i', 'r',
           'ʒ', 'ʤ', 'p', 'f', 'θ', 't', 'k', 'h', 's', 'ʃ', 'ʧ', 'w', 'u', 'ɫ',
           'ɡ', 'ɪ']

def progressive():

    f = FST('progressive')

    f.add_state('start')
    f.add_state('word')
    f.add_state('ɪ')
    f.add_state('end')

    f.initial_state = 'start'
    f.set_final('end')

    #start
    f.add_arc('start', 'word', '#', ['#'])

    #word
    f.add_arc('word', 'word', '\'', ['\''])

    f.add_arc('word', 'word', '.', ['.'])

    for i in all_ipa:
        f.add_arc('word', 'word', i, [i])

    f.add_arc('word', 'end', '#', ['ɪ', 'ŋ', '#'])


    return f