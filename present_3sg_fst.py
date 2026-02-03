import sys
from fst import FST
from fsmutils import composewords, trace

voiced = ['b', 'm', 'ð', 'd', 'ɹ', 'l', 'j', 'v', 'ɡ', 'ɫ',
          'ŋ', 'ɪ', 'ɛ', 'æ', 'ʌ', 'ʊ', 'ɒ', 'ə', 'e', 'ɡ',
          'a', 'ɔ', 'o', 'w', 'n', 'i', 'u', 'ɑ', 'r', 'ɝ']

voiceless = ['p', 'f', 'θ', 't', 'k', 'h']

sibilant = ['s', 'z', 'ʃ', 'ʒ', 'ʤ', 'ʧ']

markers = ['#']

def pres_regular():

    f_reg = FST('pres_reg')

    f_reg.add_state('start')
    f_reg.add_state('voiced')
    f_reg.add_state('sibilant')
    f_reg.add_state('voiceless')
    f_reg.add_state('marker')
    f_reg.add_state('end')

    f_reg.initial_state = 'start'
    f_reg.set_final('end')

    # starting arcs
    f_reg.add_arc('start', 'marker', '#', ['#'])

    # voiced arcs
    for i in voiced:
        f_reg.add_arc('voiced', 'voiced', i, [i])

    for i in voiceless:
        f_reg.add_arc('voiced', 'voiceless', i, [i])
    
    for i in sibilant:
        f_reg.add_arc('voiced', 'sibilant', i, [i])
    
    for i in markers:
        f_reg.add_arc('voiced', 'marker', i, [i])

    # voiceless arcs
    for i in voiceless:
        f_reg.add_arc('voiceless', 'voiceless', i, [i])
    
    for i in voiced:
        f_reg.add_arc('voiceless', 'voiced', i, [i])
    
    for i in sibilant:
        f_reg.add_arc('voiceless', 'sibilant', i, [i])

    for i in markers:
        f_reg.add_arc('voiceless', 'marker', i, [i])

    # sibilant arcs
    for i in sibilant:
        f_reg.add_arc('sibilant', 'sibilant', i, [i])
    
    for i in voiced:
        f_reg.add_arc('sibilant', 'voiced', i, [i])

    for i in voiceless:
        f_reg.add_arc('sibilant', 'voiceless', i, [i])
    
    for i in markers:
        f_reg.add_arc('sibilant', 'marker', i, [i])

    # marker arcs
    for i in markers:
        f_reg.add_arc('marker', 'marker', i, [i])
    
    for i in voiced:
        f_reg.add_arc('marker', 'voiced', i, [i])

    for i in voiceless:    
        f_reg.add_arc('marker', 'voiceless', i, [i])
    
    for i in sibilant:
        f_reg.add_arc('marker', 'sibilant', i, [i])

    # ending arcs
    f_reg.add_arc('voiced', 'end', '#', ['z', '#'])
    f_reg.add_arc('voiceless', 'end', '#', ['s', '#'])
    f_reg.add_arc('sibilant', 'end', '#', ['ɪ', 'z', '#'])

    return f_reg

def pres_irreg():

    f_irreg = FST('pres_irreg')

    # initialize our states
    f_irreg.add_state('start')
    f_irreg.add_state('marker')

    # be = is
    f_irreg.add_state('b')
    f_irreg.add_state('i_b')
    # f_irreg.add_state('#_bi')

    f_irreg.add_state('k')
    # can
    f_irreg.add_state('æ_k')
    f_irreg.add_state('n_kæ')
    # f_irreg.add_state('#_kæn')

    # could
    f_irreg.add_state('ʊ_k')
    f_irreg.add_state('d_kʊ')
    # f_irreg.add_state('#_kʊd')

    # do
    f_irreg.add_state('d')
    f_irreg.add_state('u_d')
    # f_irreg.add_state('#_du')

    # have
    f_irreg.add_state('h')
    f_irreg.add_state('æ_h')
    f_irreg.add_state('v_hæ')
    # f_irreg.add_state("#_hæv")

    f_irreg.add_state('m')
    # may
    f_irreg.add_state('e_m')
    f_irreg.add_state('ɪ_me')
    # f_irreg.add_state('#_meɪ')

    # might
    f_irreg.add_state('a_m')
    f_irreg.add_state('ɪ_ma')
    f_irreg.add_state('t_maɪ')
    # f_irreg.add_state('#_maɪt')

    # must
    f_irreg.add_state('ʌ_m')
    f_irreg.add_state('s_mʌ')
    f_irreg.add_state('t_mʌs')
    # f_irreg.add_state('#_mʌst')

    # say
    f_irreg.add_state('s')
    f_irreg.add_state('e_s')
    f_irreg.add_state('ɪ_se')
    # f_irreg.add_state('#_seɪ')

    f_irreg.add_state('ʃ')
    # shall
    f_irreg.add_state('æ_ʃ')
    f_irreg.add_state('l_ʃæ')
    # f_irreg.add_state('#_ʃæl')

    # should
    f_irreg.add_state('ʊ_ʃ')
    f_irreg.add_state('d_ʃʊ')
    # f_irreg.add_state('#_ʃʊd')

    f_irreg.add_state('w')
    # will
    f_irreg.add_state('ɪ_w')
    f_irreg.add_state('l_wɪ')
    # f_irreg.add_state('#_wɪl')

    # would
    f_irreg.add_state('ʊ_w')
    f_irreg.add_state('d_wʊ')
    # f_irreg.add_state('#_wʊd')

    f_irreg.add_state('end')

    f_irreg.initial_state = 'start'
    f_irreg.set_final('end')

    # add arcs
    # initial word marker
    f_irreg.add_arc('start', 'marker', '#', ['#'])

    # be
    f_irreg.add_arc('marker', 'b', 'b', [])
    f_irreg.add_arc('b', 'i_b', 'i', [])
    f_irreg.add_arc('i_b', 'end', '#', ['ɪ', 'z', '#'])

    # k arc
    f_irreg.add_arc('marker', 'k', 'k', [])

    # can
    f_irreg.add_arc('k', 'æ_k', 'æ', [])
    f_irreg.add_arc('æ_k', 'n_kæ', 'n', [])
    f_irreg.add_arc('n_kæ', 'end', '#', ['k', 'æ', 'n', '#'])

    # could
    f_irreg.add_arc('k', 'ʊ_k', 'ʊ', [])
    f_irreg.add_arc('ʊ_k', 'd_kʊ', 'd', [])
    f_irreg.add_arc('d_kʊ', 'end', '#', ['k', 'ʊ', 'd', '#'])
    
    # do
    f_irreg.add_arc('marker', 'd', 'd', [])
    f_irreg.add_arc('d', 'u_d', 'u', [])
    f_irreg.add_arc('u_d', 'end', '#', ['d', 'ʌ', 'z', '#'])
    
    # have = has
    f_irreg.add_arc('marker', 'h', 'h', [])
    f_irreg.add_arc('h', 'æ_h', 'æ', [])
    f_irreg.add_arc('æ_h', 'v_hæ', 'v', [])
    f_irreg.add_arc('v_hæ', 'end', '#', ['h', 'æ', 'z', '#'])

    # m arc
    f_irreg.add_arc('marker', 'm', 'm', [])

    # may
    f_irreg.add_arc('m', 'e_m', 'e', [])
    f_irreg.add_arc('e_m', 'ɪ_me', 'ɪ', [])
    f_irreg.add_arc('ɪ_me', 'end', '#', ['m', 'e', 'ɪ', '#'])

    # might
    f_irreg.add_arc('m', 'a_m', 'a', [])
    f_irreg.add_arc('a_m', 'ɪ_ma', 'ɪ', [])
    f_irreg.add_arc('ɪ_ma', 't_maɪ', 't', [])
    f_irreg.add_arc('t_maɪ', 'end', '#', ['m', 'a', 'ɪ', 't', '#'])

    # must
    f_irreg.add_arc('m', 'ʌ_m', 'ʌ', [])
    f_irreg.add_arc('ʌ_m', 's_mʌ', 's', [])
    f_irreg.add_arc('s_mʌ', 't_mʌs', 't', [])
    f_irreg.add_arc('t_mʌs', 'end', '#', ['m', 'ʌ', 's', 't', '#'])

    # say
    f_irreg.add_arc('marker', 's', 's', [])
    f_irreg.add_arc('s', 'e_s', 'e', [])
    f_irreg.add_arc('e_s', 'ɪ_se', 'ɪ', [])
    f_irreg.add_arc('ɪ_se', 'end', '#', ['s', 'ɛ', 'z', '#'])

    # ʃ arc
    f_irreg.add_arc('marker', 'ʃ', 'ʃ', [])

    # shall 
    f_irreg.add_arc('ʃ', 'æ_ʃ', 'æ', [])
    f_irreg.add_arc('æ_ʃ', 'l_ʃæ', 'l', [])
    f_irreg.add_arc('l_ʃæ', 'end', '#', ['ʃ', 'æ', 'l', '#'])

    # should
    f_irreg.add_arc('ʃ', 'ʊ_ʃ', 'ʊ', [])
    f_irreg.add_arc('ʊ_ʃ', 'd_ʃʊ', 'd', [])
    f_irreg.add_arc('d_ʃʊ', 'end', '#', ['ʃ', 'ʊ', 'd', '#'])


    # w arc
    f_irreg.add_arc('marker', 'w', 'w', [])

    # will
    f_irreg.add_arc('w', 'ɪ_w', 'ɪ', [])
    f_irreg.add_arc('ɪ_w', 'l_wɪ', 'l', [])
    f_irreg.add_arc('l_wɪ', 'end', '#', ['w', 'ɪ', 'l', '#'])

    # would
    f_irreg.add_arc('w', 'ʊ_w', 'ʊ', [])
    f_irreg.add_arc('ʊ_w', 'd_wʊ', 'd', [])
    f_irreg.add_arc('d_wʊ', 'end', '#', ['w', 'ʊ', 'd', '#'])

    return f_irreg


def final_pres_fst(inp):
    f_irreg = pres_irreg()
    out = f_irreg.transduce(inp)

    if out:
        return out

    f_reg = pres_regular()
    return f_reg.transduce(inp)
