import sys
from fst import FST
from fsmutils import composewords, trace

all_ipa = ['b', 'm', 'ð', 'ɹ', 'l', 'j', 'v', 'g', 'ŋ', 'n', 'ɑ', 'ɝ',
           'ɛ', 'æ', 'ʌ', 'ʊ', 'ɒ', 'ə', 'e', 'a', 'ɔ', 'o', 'i', 'r',
           'ʒ', 'ʤ', 'p', 'f', 'θ', 'k', 'h', 'ʃ', 'ʧ', 'w', 'u', 'ɫ',
           'ɪ', 'z', 't', 'd', 's', 'ɡ']

suffixes = ['ɪ', 'z', 't', 'd', 's']

non_suffix = [x for x in all_ipa if x not in suffixes]

def morph_analyzer_regular():

    f = FST('regular morphological analyzer')

    f.add_state('start')
    f.add_state('word')
    f.add_state('s')
    f.add_state('z')
    f.add_state('t')
    f.add_state('d')
    f.add_state('ɪ')
    f.add_state('ɪz')
    f.add_state('ɪd')
    f.add_state('ɪŋ')
    f.add_state('PRES')
    f.add_state('PAST/ PAST PART')
    f.add_state('PROG')
    f.add_state('BARE')

    f.initial_state = 'start'
    f.set_final('PRES')
    f.set_final('PAST/ PAST PART')
    f.set_final('PROG')
    f.set_final('BARE')

    # start
    f.add_arc('start', 'word', '#', '#')

    # word
    for i in non_suffix:
        f.add_arc('word', 'word', i, i)

    # for i in markers:
    #     f.add_arc('word', 'word', i, i)

    f.add_arc('word', 's', 's', [])
    f.add_arc('word', 'z', 'z', [])
    f.add_arc('word', 't', 't', [])
    f.add_arc('word', 'd', 'd', [])
    f.add_arc('word', 'ɪ', 'ɪ', [])

    f.add_arc('word', 'BARE', '#', '# BARE')

    # s
    for i in non_suffix:
        f.add_arc('s', 'word', i, ['s', i])

    f.add_arc('s', 't', 't', 's')
    f.add_arc('s', 'ɪ', 'ɪ', 's')
    f.add_arc('s', 'z', 'z', 's')
    f.add_arc('s', 'd', 'd', 's')
    f.add_arc('s', 's', 's', 's')

    f.add_arc('s', 'PRES', '#', '# 3SG-PRES')

    # z
    for i in non_suffix:
        f.add_arc('z', 'word', i, ['z', i])

    f.add_arc('z', 't', 't', 'z')
    f.add_arc('z', 'ɪ', 'ɪ', 'z')
    f.add_arc('s', 'z', 'z', 's')
    f.add_arc('z', 'd', 'd', 'z')
    f.add_arc('z', 'z', 'z', 'z')

    f.add_arc('z', 'PRES', '#', '# 3SG-PRES')

    # t
    for i in non_suffix:
        f.add_arc('t', 'word', i, ['t', i])

    f.add_arc('t', 's', 's', 't')
    f.add_arc('t', 'ɪ', 'ɪ', 't')
    f.add_arc('t', 'z', 'z', 't')
    f.add_arc('t', 'd', 'd', 't')
    f.add_arc('t', 't', 't', 't')

    f.add_arc('t', 'PAST/ PAST PART', '#', '# PST/ PST.PTCP')

    # d
    for i in non_suffix:
        f.add_arc('d', 'word', i, ['d', i])

    f.add_arc('d', 't', 't', 'd')
    f.add_arc('d', 'ɪ', 'ɪ', 'd')
    f.add_arc('d', 'z', 'z', 'd')
    f.add_arc('d', 's', 's', 'd')
    f.add_arc('d', 'd', 'd', 'd')

    f.add_arc('d', 'PAST/ PAST PART', '#', '# PST/ PST.PTCP')

    # ɪ
    for i in non_suffix:
        f.add_arc('ɪ', 'word', i, ['ɪ', i])

    f.add_arc('ɪ', 'word', 't', ['ɪ', 't'])
    f.add_arc('ɪ', 'word', 's', ['ɪ', 's'])

    f.add_arc('ɪ', 't', 't', 'ɪ')
    f.add_arc('ɪ', 's', 's', 'ɪ')
    f.add_arc('ɪ', 'ɪ', 'ɪ', 'ɪ')

    f.add_arc('ɪ', 'ɪz', 'z', [])
    f.add_arc('ɪ', 'ɪd', 'd', [])
    f.add_arc('ɪ', 'ɪŋ', 'ŋ', [])

    # ɪd
    for i in non_suffix:
        f.add_arc('ɪd', 'word', i, ['ɪ', 'd', i])

    f.add_arc('ɪd', 'PAST/ PAST PART', '#', '# PST/ PST.PTCP')
    f.add_arc('ɪd', 'ɪ', 'ɪ', 'ɪd')
    f.add_arc('ɪd', 'z', 'z', 'ɪd')
    f.add_arc('ɪd', 's', 's', 'ɪd')
    f.add_arc('ɪd', 't', 't', 'ɪd')
    f.add_arc('ɪd', 'd', 'd', 'ɪd')

    # ɪz
    for i in non_suffix:
        f.add_arc('ɪz', 'word', i, ['ɪ', 'z', i])

    f.add_arc('ɪz', 'PRES', '#', '# 3SG-PRES')
    f.add_arc('ɪz', 'ɪ', 'ɪ', 'ɪz')
    f.add_arc('ɪz', 'ɪ', 'ɪ', 'ɪz')
    f.add_arc('ɪz', 'z', 'z', 'ɪz')
    f.add_arc('ɪz', 's', 's', 'ɪz')
    f.add_arc('ɪz', 't', 't', 'ɪz')
    f.add_arc('ɪz', 'd', 'd', 'ɪz')

    # ɪŋ
    for i in non_suffix:
        f.add_arc('ɪŋ', 'word', i, ['ɪ', 'ŋ', i])

    f.add_arc('ɪŋ', 'PROG', '#', '# PROG')
    f.add_arc('ɪŋ', 'ɪ', 'ɪ', 'ɪŋ')
    f.add_arc('ɪŋ', 'ɪ', 'ɪ', 'ɪŋ')
    f.add_arc('ɪŋ', 'z', 'z', 'ɪŋ')
    f.add_arc('ɪŋ', 's', 's', 'ɪŋ')
    f.add_arc('ɪŋ', 't', 't', 'ɪŋ')
    f.add_arc('ɪŋ', 'd', 'd', 'ɪŋ')

    return f


def morph_analyzer_irregular():

    f = FST('irregular morphological analyzer')

    f.add_state('start')
    f.add_state('marker')
    f.add_state('end')

    f.initial_state = 'start'
    f.set_final('end')

    f.add_arc('start', 'marker', '#', '#')

    #arisen --> arise PST.PTCP 
    f.add_state('ə')
    f.add_arc('marker', 'ə', 'ə', [])

    f.add_state('ɹ_əɹ')
    f.add_arc('ə', 'ɹ_əɹ', 'ɹ', [])

    f.add_state('ɪ_əɹɪ')
    f.add_arc('ɹ_əɹ', 'ɪ_əɹɪ', 'ɪ', [])

    f.add_state('z_əɹɪz')
    f.add_arc('ɪ_əɹɪ', 'z_əɹɪz', 'z', [])

    f.add_state('ə_əɹɪzə')
    f.add_arc('z_əɹɪz', 'ə_əɹɪzə', 'ə', [])

    f.add_state('n_əɹɪzən')
    f.add_arc('ə_əɹɪzə', 'n_əɹɪzən', 'n', [])

    f.add_state('əɹɪzən')
    f.add_arc('n_əɹɪzən', 'end', '#', 'əraɪz# PST.PTCP')

    #arose --> arise PST
    f.add_state('o_əɹo')
    f.add_arc('ɹ_əɹ', 'o_əɹo', 'o', [])

    f.add_state('ʊ_əɹoʊ')
    f.add_arc('o_əɹo', 'ʊ_əɹoʊ', 'ʊ', [])

    f.add_state('z_əɹoʊz')
    f.add_arc('ʊ_əɹoʊ', 'z_əɹoʊz', 'z', [])

    f.add_state('əɹoʊz')
    f.add_arc('z_əɹoʊz', 'end', '#', 'əraɪz# PST')

    #awoke --> awake PST 
    f.add_state('w_əw')
    f.add_arc('ə', 'w_əw', 'w', [])

    f.add_state('o_əwo')
    f.add_arc('w_əw', 'o_əwo', 'o', [])

    f.add_state('ʊ_əwoʊ')
    f.add_arc('o_əwo', 'ʊ_əwoʊ', 'ʊ', [])

    f.add_state('k_əwoʊk')
    f.add_arc('ʊ_əwoʊ', 'k_əwoʊk', 'k', [])

    f.add_arc('k_əwoʊk', 'end', '#', 'əweɪk# PST')

    #awoken --> awake PST.PTCP
    f.add_state('ə_əwoʊkə')
    f.add_arc('k_əwoʊk', 'ə_əwoʊkə', 'ə', [])

    f.add_state('n_əwoʊkən')
    f.add_arc('ə_əwoʊkə', 'n_əwoʊkən', 'n', [])

    f.add_arc('n_əwoʊkən', 'end', '#', 'əweɪk# PST.PTCP')

    #ate --> eat PST
    f.add_state('e_ate')
    f.add_arc('marker', 'e_ate', 'e', [])

    f.add_state('ɪ_eɪ')
    f.add_arc('e_ate', 'ɪ_eɪ', 'ɪ', [])

    f.add_state('t_eɪt')
    f.add_arc('ɪ_eɪ', 't_eɪt', 't', [])

    f.add_arc('t_eɪt', 'end', '#', 'it# PST')

    #understood --> understand PST/ PST.PTCP

    f.add_state('ʌ')
    f.add_arc('marker', 'ʌ', 'ʌ', [])

    f.add_state('n_ʌn')
    f.add_arc('ʌ', 'n_ʌn', 'n', [])

    f.add_state('d_ʌnd')
    f.add_arc('n_ʌn', 'd_ʌnd', 'd', [])

    f.add_state('ə_ʌndə')
    f.add_arc('d_ʌnd', 'ə_ʌndə', 'ə', [])

    f.add_state('ɹ_ʌndəɹ')
    f.add_arc('ə_ʌndə', 'ɹ_ʌndəɹ', 'ɹ', [])

    f.add_state('s_ʌndəɹs')
    f.add_arc('ɹ_ʌndəɹ', 's_ʌndəɹs', 's', [])

    f.add_state('t_ʌndəɹst')
    f.add_arc('s_ʌndəɹs', 't_ʌndəɹst', 't', [])

    f.add_state('ʊ_ʌndəɹstʊ')
    f.add_arc('t_ʌndəɹst', 'ʊ_ʌndəɹstʊ', 'ʊ', [])

    f.add_state('d_ʌndəɹstʊd')
    f.add_arc('ʊ_ʌndəɹstʊ', 'd_ʌndəɹstʊd', 'd', [])

    f.add_arc('d_ʌndəɹstʊd', 'end', '#', 'ʌndəɹstænd# PST/ PST.PTCP')

    #been --> is PST.PTCP
    f.add_state('b')
    f.add_arc('marker', 'b', 'b', [])

    f.add_state('ɪ_bɪ')
    f.add_arc('b', 'ɪ_bɪ', 'ɪ', [])

    f.add_state('n_bɪn')
    f.add_arc('ɪ_bɪ', 'n_bɪn', 'n', [])

    f.add_arc('n_bɪn', 'end', '#', 'bi# PST.PTCP')

    #bore --> bear PST
    f.add_state('ɔ_bɔ')
    f.add_arc('b', 'ɔ_bɔ', 'ɔ', [])

    f.add_state('ɹ_bɔɹ')
    f.add_arc('ɔ_bɔ', 'ɹ_bɔɹ', 'ɹ', [])

    f.add_arc('ɹ_bɔɹ', 'end', '#', 'bɛɹ# PST')

    #borne --> borne PST.PTCP
    f.add_state('n_bɔɹn')
    f.add_arc('ɹ_bɔɹ', 'n_bɔɹn', 'n', [])

    f.add_arc('n_bɔɹn', 'end', '#', 'bɛɹ# PST.PTCP')

    #beat --> beat PST
    f.add_state('i_bi')
    f.add_arc('b', 'i_bi', 'i', [])

    f.add_state('t_bit')
    f.add_arc('i_bi', 't_bit', 't', [])

    # beat (PST)
    f.add_arc('t_bit', 'end', '#', 'bit# PST')

    #beaten --> beat PST.PTCP
    f.add_state('ə_bitə')
    f.add_arc('t_bit', 'ə_bitə', 'ə', [])

    f.add_state('n_bitən')
    f.add_arc('ə_bitə', 'n_bitən', 'n', [])

    f.add_arc('n_bitən', 'end', '#', 'bit# PST.PTCP')

    #became --> become PST
    f.add_state('k_bɪk')
    f.add_arc('ɪ_bɪ', 'k_bɪk', 'k', [])

    f.add_state('e_bɪke')
    f.add_arc('k_bɪk', 'e_bɪke', 'e', [])

    f.add_state('ɪ_bɪkeɪ')
    f.add_arc('e_bɪke', 'ɪ_bɪkeɪ', 'ɪ', [])

    f.add_state('m_bɪkeɪm')
    f.add_arc('ɪ_bɪkeɪ', 'm_bɪkeɪm', 'm', [])

    f.add_arc('m_bɪkeɪm', 'end', '#', 'bɪkʌm# PST')

    #become --> become PST.PTCP
    f.add_state('ʌ_bɪkʌ')
    f.add_arc('k_bɪk', 'ʌ_bɪkʌ', 'ʌ', [])

    f.add_state('m_bɪkʌm')
    f.add_arc('ʌ_bɪkʌ', 'm_bɪkʌm', 'm', [])

    f.add_arc('m_bɪkʌm', 'end', '#', 'bɪkʌm# PST.PTCP')

    #began --> begin PST
    f.add_state('g_bɪg')
    f.add_arc('ɪ_bɪ', 'g_bɪg', 'g', [])

    f.add_state('æ_bɪgæ')
    f.add_arc('g_bɪg', 'æ_bɪgæ', 'æ', [])

    f.add_state('n_bɪgæn')
    f.add_arc('æ_bɪgæ', 'n_bɪgæn', 'n', [])

    f.add_arc('n_bɪgæn', 'end', '#', 'bɪgɪn# PST')

    #begun --> begin PST.PTCP
    f.add_state('ʌ_bɪgʌ')
    f.add_arc('g_bɪg', 'ʌ_bɪgʌ', 'ʌ', [])

    f.add_state('n_bɪgʌn')
    f.add_arc('ʌ_bɪgʌ', 'n_bɪgʌn', 'n', [])

    f.add_arc('n_bɪgʌn', 'end', '#', 'bɪgɪn# PST.PTCP')

    #bent --> bend PST/ PST.PTCP
    f.add_state('ɛ_bɛ')
    f.add_arc('b', 'ɛ_bɛ', 'ɛ', [])

    f.add_state('n_bɛn')
    f.add_arc('ɛ_bɛ', 'n_bɛn', 'n', [])

    f.add_state('t_bɛnt')
    f.add_arc('n_bɛn', 't_bɛnt', 't', [])

    f.add_arc('t_bɛnt', 'end', '#', 'bɛnd# PST/ PST.PTCP')

    #bet --> bet PST/ PST.PTCP
    f.add_state('t_bɛt')
    f.add_arc('ɛ_bɛ', 't_bɛt', 't', [])

    f.add_arc('t_bɛt', 'end', '#', 'bɛt# PST/ PST.PTCP')

    #bound --> bind PST/ PST.PTCP
    f.add_state('a_ba')
    f.add_arc('b', 'a_ba', 'a', [])

    f.add_state('ʊ_baʊ')
    f.add_arc('a_ba', 'ʊ_baʊ', 'ʊ', [])

    f.add_state('n_baʊn')
    f.add_arc('ʊ_baʊ', 'n_baʊn', 'n', [])

    f.add_state('d_baʊnd')
    f.add_arc('n_baʊn', 'd_baʊnd', 'd', [])

    f.add_arc('d_baʊnd', 'end', '#', 'baɪnd# PST/ PST.PTCP')

    #bit --> bite PST
    f.add_state('t_bɪt')
    f.add_arc('t_bɪt', 'end', '#', 'baɪt# PST')

    #bitten --> bite PST.PTCP
    f.add_state('ə_bɪtə')
    f.add_arc('t_bɪt', 'ə_bɪtə', 'ə', [])

    f.add_state('n_bɪtən')
    f.add_arc('ə_bɪtə', 'n_bɪtən', 'n', [])

    f.add_arc('n_bɪtən', 'end', '#', 'baɪt# PST.PTCP')

    #bled --> bleed PST/ PST.PTCP
    f.add_state('l_bl')
    f.add_arc('b', 'l_bl', 'l', [])

    f.add_state('ɛ_blɛ')
    f.add_arc('l_bl', 'ɛ_blɛ', 'ɛ', [])

    f.add_state('d_blɛd')
    f.add_arc('ɛ_blɛ', 'd_blɛd', 'd', [])

    f.add_arc('d_blɛd', 'end', '#', 'blid# PST/ PST.PTCP')

    #blew --> blow PST
    f.add_state('u_blu')
    f.add_arc('l_bl', 'u_blu', 'u', [])

    f.add_arc('u_blu', 'end', '#', 'bloʊ# PST')

    #blown --> blow PST.PTCP
    f.add_state('o_blo')
    f.add_arc('l_bl', 'o_blo', 'o', [])

    f.add_state('ʊ_bloʊ')
    f.add_arc('o_blo', 'ʊ_bloʊ', 'ʊ', [])

    f.add_state('n_bloʊn')
    f.add_arc('ʊ_bloʊ', 'n_bloʊn', 'n', [])

    f.add_arc('n_bloʊn', 'end', '#', 'bloʊ# PST.PTCP')

    #broke --> break PST
    f.add_state('ɹ_bɹ')
    f.add_arc('b', 'ɹ_bɹ', 'ɹ', [])

    f.add_state('o_bɹo')
    f.add_arc('ɹ_bɹ', 'o_bɹo', 'o', [])

    f.add_state('ʊ_bɹoʊ')
    f.add_arc('o_bɹo', 'ʊ_bɹoʊ', 'ʊ', [])

    f.add_state('k_bɹoʊk')
    f.add_arc('ʊ_bɹoʊ', 'k_bɹoʊk', 'k', [])

    f.add_arc('k_bɹoʊk', 'end', '#', 'bɹeɪk# PST')

    #broken --> break PTCP
    f.add_state('ə_bɹoʊkə')
    f.add_arc('k_bɹoʊk', 'ə_bɹoʊkə', 'ə', [])

    f.add_state('n_bɹoʊkən')
    f.add_arc('ə_bɹoʊkə', 'n_bɹoʊkən', 'n', [])

    f.add_arc('n_bɹoʊkən', 'end', '#', 'bɹeɪk# PST.PTCP')

    #brought --> bring PST.PTCP
    f.add_state('ɔ_bɹɔ')
    f.add_arc('ɹ_bɹ', 'ɔ_bɹɔ', 'ɔ', [])

    f.add_state('t_bɹɔt')
    f.add_arc('ɔ_bɹɔ', 't_bɹɔt', 't', [])

    f.add_arc('t_bɹɔt', 'end', '#', 'bɹɪŋ# PST.PTCP')

    #built --> build PST/ PST.PTCP
    f.add_state('l_bɪl')
    f.add_arc('ɪ_bɪ', 'l_bɪl', 'l', [])

    f.add_state('t_bɪlt')
    f.add_arc('l_bɪl', 't_bɪlt', 't', [])

    f.add_arc('t_bɪlt', 'end', '#', 'bɪld# PST/ PST.PTCP')

    #burst --> burst PST/ PST.PTCP
    f.add_state('ɝ_bɝ')
    f.add_arc('b', 'ɝ_bɝ', 'ɝ', [])

    f.add_state('s_bɝs')
    f.add_arc('ɝ_bɝ', 's_bɝs', 's', [])

    f.add_state('t_bɝst')
    f.add_arc('s_bɝs', 't_bɝst', 't', [])

    f.add_arc('t_bɝst', 'end', '#', 'bɝst# PST/ PST.PTCP')

    #bought --> buy PST/ PST.PTCP
    f.add_state('t_bɔt')
    f.add_arc('ɔ_bɔ', 't_bɔt', 't', [])

    f.add_arc('t_bɔt', 'end', '#', 'baɪ# PST/ PST.PTCP')

    #caught --> catch PST/ PST.PTCP
    f.add_state('k')
    f.add_arc('marker', 'k', 'k', [])

    f.add_state('ɔ_kɔ')
    f.add_arc('k', 'ɔ_kɔ', 'ɔ', [])

    f.add_state('t_kɔt')
    f.add_arc('ɔ_kɔ', 't_kɔt', 't', [])

    f.add_arc('t_kɔt', 'end', '#', 'kæʧ# PST/ PST.PTCP')

    #chose --> choose PST
    f.add_state('ʧ')
    f.add_arc('marker', 'ʧ', 'ʧ', [])

    f.add_state('o_ʧo')
    f.add_arc('ʧ', 'o_ʧo', 'o', [])

    f.add_state('ʊ_ʧoʊ')
    f.add_arc('o_ʧo', 'ʊ_ʧoʊ', 'ʊ', [])

    f.add_state('z_ʧoʊz')
    f.add_arc('ʊ_ʧoʊ', 'z_ʧoʊz', 'z', [])

    f.add_arc('z_ʧoʊz', 'end', '#', 'ʧuz# PST')

    #chosen --> choose PST.PTCP
    f.add_state('ə_ʧoʊzə')
    f.add_arc('z_ʧoʊz', 'ə_ʧoʊzə', 'ə', [])

    f.add_state('n_ʧoʊzən')
    f.add_arc('ə_ʧoʊzə', 'n_ʧoʊzən', 'n', [])

    f.add_arc('n_ʧoʊzən', 'end', '#', 'ʧuz# PST.PTCP')

    #came --> come PST
    f.add_state('e_ke')
    f.add_arc('k', 'e_ke', 'e', [])

    f.add_state('ɪ_keɪ')
    f.add_arc('e_ke', 'ɪ_keɪ', 'ɪ', [])

    f.add_state('m_keɪm')
    f.add_arc('ɪ_keɪ', 'm_keɪm', 'm', [])

    f.add_arc('m_keɪm', 'end', '#', 'kʌm# PST')

    #come --> come PST.PTCP
    f.add_state('ʌ_kʌ')
    f.add_arc('k', 'ʌ_kʌ', 'ʌ', [])

    f.add_state('m_kʌm')
    f.add_arc('ʌ_kʌ', 'm_kʌm', 'm', [])

    f.add_arc('m_kʌm', 'end', '#', 'kʌm# PST.PTCP')

    #cost --> cost PST/ PST.PTCP
    f.add_state('s_kɔs')
    f.add_arc('ɔ_kɔ', 's_kɔs', 's', [])

    f.add_state('t_kɔst')
    f.add_arc('s_kɔs', 't_kɔst', 't', [])

    f.add_arc('t_kɔst', 'end', '#', 'kɔst# PST/ PST.PTCP')

    #crept --> creep PST/ PST.PTCP
    f.add_state('ɹ_kɹ')
    f.add_arc('k', 'ɹ_kɹ', 'ɹ', [])

    f.add_state('ɛ_kɹɛ')
    f.add_arc('ɹ_kɹ', 'ɛ_kɹɛ', 'ɛ', [])

    f.add_state('p_kɹɛp')
    f.add_arc('ɛ_kɹɛ', 'p_kɹɛp', 'p', [])

    f.add_state('t_kɹɛpt')
    f.add_arc('p_kɹɛp', 't_kɹɛpt', 't', [])

    f.add_arc('t_kɹɛpt', 'end', '#', 'kɹip# PST/ PST.PTCP')

    #cut --> cut PST/ PST.PTCP
    f.add_state('t_kʌt')
    f.add_arc('ʌ_kʌ', 't_kʌt', 't', [])

    f.add_arc('t_kʌt', 'end', '#', 'kʌt# PST/ PST.PTCP')

    #dealt --> deal PST/ PST.PTCP
    f.add_state('d')
    f.add_arc('marker', 'd', 'd', [])

    f.add_state('ɛ_dɛ')
    f.add_arc('d', 'ɛ_dɛ', 'ɛ', [])

    f.add_state('l_dɛl')
    f.add_arc('ɛ_dɛ', 'l_dɛl', 'l', [])

    f.add_state('t_dɛlt')
    f.add_arc('l_dɛl', 't_dɛlt', 't', [])

    f.add_arc('t_dɛlt', 'end', '#', 'dil# PST/ PST.PTCP')

    #dug --> dig PST/ PST.PTCP
    f.add_state('ʌ_dʌ')
    f.add_arc('d', 'ʌ_dʌ', 'ʌ', [])

    f.add_state('g_dʌg')
    f.add_arc('ʌ_dʌ', 'g_dʌg', 'g', [])

    f.add_arc('g_dʌg', 'end', '#', 'dɪg# PST/ PST.PTCP')

    #does --> do PRES
    f.add_state('z_dʌz')
    f.add_arc('ʌ_dʌ', 'z_dʌz', 'z', [])

    f.add_arc('z_dʌz', 'end', '#', 'du# PRES')

    #dove --> dive PST
    f.add_state('o_do')
    f.add_arc('d', 'o_do', 'o', [])

    f.add_state('ʊ_doʊ')
    f.add_arc('o_do', 'ʊ_doʊ', 'ʊ', [])

    f.add_state('v_doʊv')
    f.add_arc('ʊ_doʊ', 'v_doʊv', 'v', [])

    f.add_arc('v_doʊv', 'end', '#', 'daɪv# PST')

    #did --> do PST
    f.add_state('ɪ_dɪ')
    f.add_arc('d', 'ɪ_dɪ', 'ɪ', [])

    f.add_state('d_dɪd')
    f.add_arc('ɪ_dɪ', 'd_dɪd', 'd', [])

    f.add_arc('d_dɪd', 'end', '#', 'du# PST')

    #done --> do PST.PTCP
    f.add_state('n_dʌn')
    f.add_arc('ʌ_dʌ', 'n_dʌn', 'n', [])

    f.add_arc('n_dʌn', 'end', '#', 'du# PST.PTCP')

    #drew --> draw PST
    f.add_state('ɹ_dɹ')
    f.add_arc('d', 'ɹ_dɹ', 'ɹ', [])

    f.add_state('u_dɹu')
    f.add_arc('ɹ_dɹ', 'u_dɹu', 'u', [])

    f.add_arc('u_dɹu', 'end', '#', 'dɹɔ# PST')

    #drawn --> draw PST.PTCP
    f.add_state('ɔ_dɹɔ')
    f.add_arc('ɹ_dɹ', 'ɔ_dɹɔ', 'ɔ', [])

    f.add_state('n_dɹɔn')
    f.add_arc('ɔ_dɹɔ', 'n_dɹɔn', 'n', [])

    f.add_arc('n_dɹɔn', 'end', '#', 'dɹɔ# PST.PTCP')

    #dreamt --> dream PST/ PST.PTCP
    f.add_state('ɛ_dɹɛ')
    f.add_arc('ɹ_dɹ', 'ɛ_dɹɛ', 'ɛ', [])

    f.add_state('m_dɹɛm')
    f.add_arc('ɛ_dɹɛ', 'm_dɹɛm', 'm', [])

    f.add_state('t_dɹɛmt')
    f.add_arc('m_dɹɛm', 't_dɹɛmt', 't', [])

    f.add_arc('t_dɹɛmt', 'end', '#', 'dɹim# PST/ PST.PTCP')

    #drank --> drink PST
    f.add_state('æ_dɹæ')
    f.add_arc('ɹ_dɹ', 'æ_dɹæ', 'æ', [])

    f.add_state('ŋ_dɹæŋ')
    f.add_arc('æ_dɹæ', 'ŋ_dɹæŋ', 'ŋ', [])

    f.add_state('k_dɹæŋk')
    f.add_arc('ŋ_dɹæŋ', 'k_dɹæŋk', 'k', [])

    f.add_arc('k_dɹæŋk', 'end', '#', 'dɹɪŋk# PST')

    #drunk --> drink PST.PTCP
    f.add_state('ʌ_dɹʌ')
    f.add_arc('ɹ_dɹ', 'ʌ_dɹʌ', 'ʌ', [])

    f.add_state('ŋ_dɹʌŋ')
    f.add_arc('ʌ_dɹʌ', 'ŋ_dɹʌŋ', 'ŋ', [])

    f.add_state('k_dɹʌŋk')
    f.add_arc('ŋ_dɹʌŋ', 'k_dɹʌŋk', 'k', [])

    f.add_arc('k_dɹʌŋk', 'end', '#', 'dɹɪŋk# PST.PTCP')

    #drove --> drive PST
    f.add_state('o_dɹo')
    f.add_arc('ɹ_dɹ', 'o_dɹo', 'o', [])

    f.add_state('ʊ_dɹoʊ')
    f.add_arc('o_dɹo', 'ʊ_dɹoʊ', 'ʊ', [])

    f.add_state('v_dɹoʊv')
    f.add_arc('ʊ_dɹoʊ', 'v_dɹoʊv', 'v', [])

    f.add_arc('v_dɹoʊv', 'end', '#', 'dɹaɪv# PST')

    #driven --> drive PST.PTCP
    f.add_state('ɪ_dɹɪ')
    f.add_arc('ɹ_dɹ', 'ɪ_dɹɪ', 'ɪ', [])

    f.add_state('v_dɹɪv')
    f.add_arc('ɪ_dɹɪ', 'v_dɹɪv', 'v', [])

    f.add_state('ə_dɹɪvə')
    f.add_arc('v_dɹɪv', 'ə_dɹɪvə', 'ə', [])

    f.add_state('n_dɹɪvən')
    f.add_arc('ə_dɹɪvə', 'n_dɹɪvən', 'n', [])

    f.add_arc('n_dɹɪvən', 'end', '#', 'dɹaɪv# PST.PTCP')

    #eaten --> eat PST.PTCP
    f.add_state('i')
    f.add_arc('marker', 'i', 'i', [])

    f.add_state('t_it')
    f.add_arc('i', 't_it', 't', [])

    f.add_state('ə_itə')
    f.add_arc('t_it', 'ə_itə', 'ə', [])

    f.add_state('n_itən')
    f.add_arc('ə_itə', 'n_itən', 'n', [])

    f.add_arc('n_itən', 'end', '#', 'it# PST.PTCP')

    #fell --> fall PST
    f.add_state('f')
    f.add_arc('marker', 'f', 'f', [])

    f.add_state('ɛ_fɛ')
    f.add_arc('f', 'ɛ_fɛ', 'ɛ', [])

    f.add_state('l_fɛl')
    f.add_arc('ɛ_fɛ', 'l_fɛl', 'l', [])

    f.add_arc('l_fɛl', 'end', '#', 'fɔl# PST')

    #fallen --> fall PST.PTCP
    f.add_state('ɔ_fɔ')
    f.add_arc('f', 'ɔ_fɔ', 'ɔ', [])

    f.add_state('l_fɔl')
    f.add_arc('ɔ_fɔ', 'l_fɔl', 'l', [])

    f.add_state('ə_fɔlə')
    f.add_arc('l_fɔl', 'ə_fɔlə', 'ə', [])

    f.add_state('n_fɔlən')
    f.add_arc('ə_fɔlə', 'n_fɔlən', 'n', [])

    f.add_arc('n_fɔlən', 'end', '#', 'fɔl# PST.PTCP')

    #fed --> feed PST/ PST.PTCP
    f.add_state('d_fɛd')
    f.add_arc('ɛ_fɛ', 'd_fɛd', 'd', [])

    f.add_arc('d_fɛd', 'end', '#', 'fid# PST/ PST.PTCP')

    #felt --> feel PST/ PST.PTCP
    f.add_state('t_fɛlt')
    f.add_arc('l_fɛl', 't_fɛlt', 't', [])

    f.add_arc('t_fɛlt', 'end', '#', 'fil# PST/ PST.PTCP')

    #fought --> fight PST/ PST.PTCP
    f.add_state('t_fɔt')
    f.add_arc('ɔ_fɔ', 't_fɔt', 't', [])

    f.add_arc('t_fɔt', 'end', '#', 'faɪt# PST/ PST.PTCP')

    #found --> find PST/ PST.PTCP
    f.add_state('a_fa')
    f.add_arc('f', 'a_fa', 'a', [])

    f.add_state('ʊ_faʊ')
    f.add_arc('a_fa', 'ʊ_faʊ', 'ʊ', [])

    f.add_state('n_faʊn')
    f.add_arc('ʊ_faʊ', 'n_faʊn', 'n', [])

    f.add_state('d_faʊnd')
    f.add_arc('n_faʊn', 'd_faʊnd', 'd', [])

    f.add_arc('d_faʊnd', 'end', '#', 'faɪnd# PST/ PST.PTCP')

    #fit --> fit PST.PTCP
    f.add_state('ɪ_fɪ')
    f.add_arc('f', 'ɪ_fɪ', 'ɪ', [])

    f.add_state('t_fɪt')
    f.add_arc('ɪ_fɪ', 't_fɪt', 't', [])

    f.add_arc('t_fɪt', 'end', '#', 'fɪt# PST/ PST.PTCP')

    #fled --> flee PST/ PST.PTCP
    f.add_state('l_fl')
    f.add_arc('f', 'l_fl', 'l', [])

    f.add_state('ɛ_flɛ')
    f.add_arc('l_fl', 'ɛ_flɛ', 'ɛ', [])

    f.add_state('d_flɛd')
    f.add_arc('ɛ_flɛ', 'd_flɛd', 'd', [])

    f.add_arc('d_flɛd', 'end', '#', 'fli# PST/ PST.PTCP')

    #flung --> fling PST/ PST.PTCP
    f.add_state('ʌ_flʌ')
    f.add_arc('l_fl', 'ʌ_flʌ', 'ʌ', [])

    f.add_state('ŋ_flʌŋ')
    f.add_arc('ʌ_flʌ', 'ŋ_flʌŋ', 'ŋ', [])

    f.add_arc('ŋ_flʌŋ', 'end', '#', 'flɪŋ# PST/ PST.PTCP')

    #flew --> fly PST
    f.add_state('u_flu')
    f.add_arc('l_fl', 'u_flu', 'u', [])

    f.add_arc('u_flu', 'end', '#', 'flaɪ# PST')

    #flown --> fly PST.PTCP
    f.add_state('o_flo')
    f.add_arc('l_fl', 'o_flo', 'o', [])

    f.add_state('ʊ_floʊ')
    f.add_arc('o_flo', 'ʊ_floʊ', 'ʊ', [])

    f.add_state('n_floʊn')
    f.add_arc('ʊ_floʊ', 'n_floʊn', 'n', [])

    f.add_arc('n_floʊn', 'end', '#', 'flaɪ# PST.PTCP')

    #forbade --> forbid PST
    f.add_state('ə_fə')
    f.add_arc('f', 'ə_fə', 'ə', [])

    f.add_state('ɹ_fər')
    f.add_arc('ə_fə', 'ɹ_fər', 'ɹ', [])

    f.add_state('b_fərb')
    f.add_arc('ɹ_fər', 'b_fərb', 'b', [])

    f.add_state('e_fərbe')
    f.add_arc('b_fərb', 'e_fərbe', 'e', [])

    f.add_state('ɪ_fərbeɪ')
    f.add_arc('e_fərbe', 'ɪ_fərbeɪ', 'ɪ', [])

    f.add_state('d_fərbeɪd')
    f.add_arc('ɪ_fərbeɪ', 'd_fərbeɪd', 'd', [])

    f.add_arc('d_fərbeɪd', 'end', '#', 'fəɹbɪd# PST')

    #forbidden --> forbid PST.PTCP
    f.add_state('ɪ_fərbɪ')
    f.add_arc('b_fərb', 'ɪ_fərbɪ', 'ɪ', [])

    f.add_state('d_fərbɪd')
    f.add_arc('ɪ_fərbɪ', 'd_fərbɪd', 'd', [])

    f.add_state('ə_fərbɪdə')
    f.add_arc('d_fərbɪd', 'ə_fərbɪdə', 'ə', [])

    f.add_state('n_fərbɪdən')
    f.add_arc('ə_fərbɪdə', 'n_fərbɪdən', 'n', [])

    f.add_arc('n_fərbɪdən', 'end', '#', 'fəɹbɪd# PST.PTCP')

    #forgot --> forget PST
    f.add_state('g_fərg')
    f.add_arc('ɹ_fər', 'g_fərg', 'g', [])

    f.add_state('ɑ_fərgɑ')
    f.add_arc('g_fərg', 'ɑ_fərgɑ', 'ɑ', [])

    f.add_state('t_fərgɑt')
    f.add_arc('ɑ_fərgɑ', 't_fərgɑt', 't', [])

    f.add_arc('t_fərgɑt', 'end', '#', 'fəɹgɛt# PST')

    #forgotten --> forget PST.PTCP
    f.add_state('ə_fərgɑtə')
    f.add_arc('t_fərgɑt', 'ə_fərgɑtə', 'ə', [])

    f.add_state('n_fərgɑtən')
    f.add_arc('ə_fərgɑtə', 'n_fərgɑtən', 'n', [])

    f.add_arc('n_fərgɑtən', 'end', '#', 'fəɹgɛt# PST.PTCP')

    #forgave --> forgive PST
    f.add_state('e_fərge')
    f.add_arc('g_fərg', 'e_fərge', 'e', [])

    f.add_state('ɪ_fərgeɪ')
    f.add_arc('e_fərge', 'ɪ_fərgeɪ', 'ɪ', [])

    f.add_state('v_fərgeɪv')
    f.add_arc('ɪ_fərgeɪ', 'v_fərgeɪv', 'v', [])

    f.add_arc('v_fərgeɪv', 'end', '#', 'fəɹgɪv# PST')

    #forgiven --> forgive PST.PTCP
    f.add_state('ɪ_fərgɪ')
    f.add_arc('g_fərg', 'ɪ_fərgɪ', 'ɪ', [])

    f.add_state('v_fərgɪv')
    f.add_arc('ɪ_fərgɪ', 'v_fərgɪv', 'v', [])

    f.add_state('ə_fərgɪvə')
    f.add_arc('v_fərgɪv', 'ə_fərgɪvə', 'ə', [])

    f.add_state('n_fərgɪvən')
    f.add_arc('ə_fərgɪvə', 'n_fərgɪvən', 'n', [])

    f.add_arc('n_fərgɪvən', 'end', '#', 'fəɹgɪv# PST.PTCP')

    #froze --> freeze PST
    f.add_state('ɹ_fɹ')
    f.add_arc('f', 'ɹ_fɹ', 'ɹ', [])

    f.add_state('o_fɹo')
    f.add_arc('ɹ_fɹ', 'o_fɹo', 'o', [])

    f.add_state('ʊ_fɹoʊ')
    f.add_arc('o_fɹo', 'ʊ_fɹoʊ', 'ʊ', [])

    f.add_state('z_fɹoʊz')
    f.add_arc('ʊ_fɹoʊ', 'z_fɹoʊz', 'z', [])

    f.add_arc('z_fɹoʊz', 'end', '#', 'friz# PST')

    #frozen --> freeze PST.PTCP
    f.add_state('ə_fɹoʊzə')
    f.add_arc('z_fɹoʊz', 'ə_fɹoʊzə', 'ə', [])

    f.add_state('n_fɹoʊzən')
    f.add_arc('ə_fɹoʊzə', 'n_fɹoʊzən', 'n', [])

    f.add_arc('n_fɹoʊzən', 'end', '#', 'friz# PST.PTCP')

    #got --> get PST
    f.add_state('g')
    f.add_arc('marker', 'g', 'g', [])

    f.add_state('ɑ_gɑ')
    f.add_arc('g', 'ɑ_gɑ', 'ɑ', [])

    f.add_state('t_gɑt')
    f.add_arc('ɑ_gɑ', 't_gɑt', 't', [])

    f.add_arc('t_gɑt', 'end', '#', 'gɛt# PST')

    #gotten --> get PST.PTCP
    f.add_state('n_gɑtn')
    f.add_arc('t_gɑt', 'n_gɑtn', 'n', [])

    f.add_arc('n_gɑtn', 'end', '#', 'gɛt# PST.PTCP')

    #gave --> give PST
    f.add_state('e_ge')
    f.add_arc('g', 'e_ge', 'e', [])

    f.add_state('ɪ_geɪ')
    f.add_arc('e_ge', 'ɪ_geɪ', 'ɪ', [])

    f.add_state('v_geɪv')
    f.add_arc('ɪ_geɪ', 'v_geɪv', 'v', [])

    f.add_arc('v_geɪv', 'end', '#', 'gɪv# PST')

    #given --> give PST.PTCP
    f.add_state('ɪ_gɪ')
    f.add_arc('g', 'ɪ_gɪ', 'ɪ', [])

    f.add_state('v_gɪv')
    f.add_arc('ɪ_gɪ', 'v_gɪv', 'v', [])

    f.add_state('ə_gɪvə')
    f.add_arc('v_gɪv', 'ə_gɪvə', 'ə', [])

    f.add_state('n_gɪvən')
    f.add_arc('ə_gɪvə', 'n_gɪvən', 'n', [])

    f.add_arc('n_gɪvən', 'end', '#', 'gɪv# PST.PTCP')

    #gone --> go PST.PTCP
    f.add_state('n_gɑn')
    f.add_arc('ɑ_gɑ', 'n_gɑn', 'n', [])

    f.add_arc('n_gɑn', 'end', '#', 'goʊ# PST.PTCP')

    #grew --> grow PST
    f.add_state('ɹ_gɹ')
    f.add_arc('g', 'ɹ_gɹ', 'ɹ', [])

    f.add_state('u_gɹu')
    f.add_arc('ɹ_gɹ', 'u_gɹu', 'u', [])

    f.add_arc('u_gɹu', 'end', '#', 'gɹoʊ# PST')

    #grown --> grow PST.PTCP
    f.add_state('o_gɹo')
    f.add_arc('ɹ_gɹ', 'o_gɹo', 'o', [])

    f.add_state('ʊ_gɹoʊ')
    f.add_arc('o_gɹo', 'ʊ_gɹoʊ', 'ʊ', [])

    f.add_state('n_gɹoʊn')
    f.add_arc('ʊ_gɹoʊ', 'n_gɹoʊn', 'n', [])

    f.add_arc('n_gɹoʊn', 'end', '#', 'gɹoʊ# PST.PTCP')

    #hung --> hang PST/ PST.PTCP
    f.add_state('h')
    f.add_arc('marker', 'h', 'h', [])

    f.add_state('ʌ_hʌ')
    f.add_arc('h', 'ʌ_hʌ', 'ʌ', [])

    f.add_state('ŋ_hʌŋ')
    f.add_arc('ʌ_hʌ', 'ŋ_hʌŋ', 'ŋ', [])

    f.add_arc('ŋ_hʌŋ', 'end', '#', 'hæŋ# PST/ PST.PTCP')

    #had --> have PST/ PST.PTCP
    f.add_state('æ_hæ')
    f.add_arc('h', 'æ_hæ', 'æ', [])

    f.add_state('d_hæd')
    f.add_arc('æ_hæ', 'd_hæd', 'd', [])

    f.add_arc('d_hæd', 'end', '#', 'hæv# PST/ PST.PTCP')

    #has --> have PRES
    f.add_state('s_hæs')
    f.add_arc('æ_hæ', 's_hæs', 's', [])

    f.add_arc('s_hæs', 'end', '#', 'hæv# PRES')

    #heard --> hear PST/ PST.PTCP
    f.add_state('ɝ_hɝ')
    f.add_arc('h', 'ɝ_hɝ', 'ɝ', [])

    f.add_state('d_hɝd')
    f.add_arc('ɝ_hɝ', 'd_hɝd', 'd', [])

    f.add_arc('d_hɝd', 'end', '#', 'hɪɹ# PST/ PST.PTCP')

    #hid --> hide PST
    f.add_state('ɪ_hɪ')
    f.add_arc('h', 'ɪ_hɪ', 'ɪ', [])

    f.add_state('d_hɪd')
    f.add_arc('ɪ_hɪ', 'd_hɪd', 'd', [])

    f.add_arc('d_hɪd', 'end', '#', 'haɪd# PST')

    #hidden --> hide PST.PTCP
    f.add_state('ə_hɪdə')
    f.add_arc('d_hɪd', 'ə_hɪdə', 'ə', [])

    f.add_state('n_hɪdən')
    f.add_arc('ə_hɪdə', 'n_hɪdən', 'n', [])

    f.add_arc('n_hɪdən', 'end', '#', 'haɪd# PST.PTCP')

    #hit --> hit PST/ PST.PTCP
    f.add_state('t_hɪt')
    f.add_arc('ɪ_hɪ', 't_hɪt', 't', [])

    f.add_arc('t_hɪt', 'end', '#', 'hɪt# PST/ PST.PTCP')

    #held --> hold PST/ PST.PTCP
    f.add_state('ɛ_hɛ')
    f.add_arc('h', 'ɛ_hɛ', 'ɛ', [])

    f.add_state('l_hɛl')
    f.add_arc('ɛ_hɛ', 'l_hɛl', 'l', [])

    f.add_state('d_hɛld')
    f.add_arc('l_hɛl', 'd_hɛld', 'd', [])

    f.add_arc('d_hɛld', 'end', '#', 'hoʊld# PST/ PST.PTCP')

    #hurt --> hurt PST/ PST.PTCP
    f.add_state('ɜ_hɜ')
    f.add_arc('h', 'ɜ_hɜ', 'ɜ', [])

    f.add_state('ɹ_hɜɹ')
    f.add_arc('ɜ_hɜ', 'ɹ_hɜɹ', 'ɹ', [])

    f.add_state('t_hɜɹt')
    f.add_arc('ɹ_hɜɹ', 't_hɜɹt', 't', [])

    f.add_arc('t_hɜɹt', 'end', '#', 'hɜɹt# PST/ PST.PTCP')

    #is --> be PRES
    f.add_state('ɪ')
    f.add_arc('marker', 'ɪ', 'ɪ', [])

    f.add_state('z_ɪz')
    f.add_arc('ɪ', 'z_ɪz', 'z', [])

    f.add_arc('z_ɪz', 'end', '#', 'bi# PRES')

    #kept --> keep PST/ PST.PTCP
    f.add_state('ɛ_kɛ')
    f.add_arc('k', 'ɛ_kɛ', 'ɛ', [])

    f.add_state('p_kɛp')
    f.add_arc('ɛ_kɛ', 'p_kɛp', 'p', [])

    f.add_state('t_kɛpt')
    f.add_arc('p_kɛp', 't_kɛpt', 't', [])

    f.add_arc('t_kɛpt', 'end', '#', 'kip# PST/ PST.PTCP')

    #quit --> quit PST/ PST.PTCP
    f.add_state('w_kw')
    f.add_arc('k', 'w_kw', 'w', [])

    f.add_state('ɪ_kwɪ')
    f.add_arc('w_kw', 'ɪ_kwɪ', 'ɪ', [])

    f.add_state('t_kwɪt')
    f.add_arc('ɪ_kwɪ', 't_kwɪt', 't', [])

    f.add_arc('t_kwɪt', 'end', '#', 'kwɪt# PST/ PST.PTCP')

    #led --> lead PST.PTCP
    f.add_state('l')
    f.add_arc('marker', 'l', 'l', [])

    f.add_state('ɛ_lɛ')
    f.add_arc('l', 'ɛ_lɛ', 'ɛ', [])

    f.add_state('d_lɛd')
    f.add_arc('ɛ_lɛ', 'd_lɛd', 'd', [])

    f.add_arc('d_lɛd', 'end', '#', 'lid# PST.PTCP')

    #left --> leave PST/ PST.PTCP
    f.add_state('f_lɛf')
    f.add_arc('ɛ_lɛ', 'f_lɛf', 'f', [])

    f.add_state('t_lɛft')
    f.add_arc('f_lɛf', 't_lɛft', 't', [])

    f.add_arc('t_lɛft', 'end', '#', 'liv# PST/ PST.PTCP')

    #lent --> lend PST/ PST.PTCP
    f.add_state('n_lɛn')
    f.add_arc('ɛ_lɛ', 'n_lɛn', 'n', [])

    f.add_state('t_lɛnt')
    f.add_arc('n_lɛn', 't_lɛnt', 't', [])

    f.add_arc('t_lɛnt', 'end', '#', 'lɛnd# PST/ PST.PTCP')

    #let --> let PST/ PST.PTCP
    f.add_state('t_lɛt')
    f.add_arc('ɛ_lɛ', 't_lɛt', 't', [])

    f.add_arc('t_lɛt', 'end', '#', 'lɛt# PST/ PST.PTCP')

    #lit --> light PST/ PST.PTCP
    f.add_state('ɪ_lɪ')
    f.add_arc('l', 'ɪ_lɪ', 'ɪ', [])

    f.add_state('t_lɪt')
    f.add_arc('ɪ_lɪ', 't_lɪt', 't', [])

    f.add_arc('t_lɪt', 'end', '#', 'laɪt# PST/ PST.PTCP')

    #lost --> lose PST/ PST.PTCP
    f.add_state('ɔ_lɔ')
    f.add_arc('l', 'ɔ_lɔ', 'ɔ', [])

    f.add_state('s_lɔs')
    f.add_arc('ɔ_lɔ', 's_lɔs', 's', [])

    f.add_state('t_lɔst')
    f.add_arc('s_lɔs', 't_lɔst', 't', [])

    f.add_arc('t_lɔst', 'end', '#', 'luz# PST/ PST.PTCP')

    #made --> make PST/ PST.PTCP
    f.add_state('m')
    f.add_arc('marker', 'm', 'm', [])

    f.add_state('e_me')
    f.add_arc('m', 'e_me', 'e', [])

    f.add_state('ɪ_meɪ')
    f.add_arc('e_me', 'ɪ_meɪ', 'ɪ', [])

    f.add_state('d_meɪd')
    f.add_arc('ɪ_meɪ', 'd_meɪd', 'd', [])

    f.add_arc('d_meɪd', 'end', '#', 'meɪk# PST/ PST.PTCP')

    #meant --> mean PST/ PST.PTCP
    f.add_state('ɛ_mɛ')
    f.add_arc('m', 'ɛ_mɛ', 'ɛ', [])

    f.add_state('n_mɛn')
    f.add_arc('ɛ_mɛ', 'n_mɛn', 'n', [])

    f.add_state('t_mɛnt')
    f.add_arc('n_mɛn', 't_mɛnt', 't', [])

    f.add_arc('t_mɛnt', 'end', '#', 'min# PST/ PST.PTCP')

    #met --> meet
    f.add_state('t_mɛt')
    f.add_arc('ɛ_mɛ', 't_mɛt', 't', [])

    f.add_arc('t_mɛt', 'end', '#', 'mit# PST/ PST.PTCP')

    #knelt --> kneel PST/ PST.PTCP
    f.add_state('n')
    f.add_arc('marker', 'n', 'n', [])

    f.add_state('ɛ_nɛ')
    f.add_arc('n', 'ɛ_nɛ', 'ɛ', [])

    f.add_state('l_nɛl')
    f.add_arc('ɛ_nɛ', 'l_nɛl', 'l', [])

    f.add_state('t_nɛlt')
    f.add_arc('l_nɛl', 't_nɛlt', 't', [])

    f.add_arc('t_nɛlt', 'end', '#', 'nil# PST/ PST.PTCP')

    #knew --> know PST
    f.add_state('u_nu')
    f.add_arc('n', 'u_nu', 'u', [])

    f.add_arc('u_nu', 'end', '#', 'noʊ# PST')

    #known --> know PST.PTCP
    f.add_state('o_no')
    f.add_arc('n', 'o_no', 'o', [])

    f.add_state('ʊ_noʊ')
    f.add_arc('o_no', 'ʊ_noʊ', 'ʊ', [])

    f.add_state('n_noʊn')
    f.add_arc('ʊ_noʊ', 'n_noʊn', 'n', [])

    f.add_arc('n_noʊn', 'end', '#', 'noʊ# PST.PTCP')

    #pled --> plead PST/ PST.PTCP
    f.add_state('p')
    f.add_arc('marker', 'p', 'p', [])

    f.add_state('l_pl')
    f.add_arc('p', 'l_pl', 'l', [])

    f.add_state('ɛ_plɛ')
    f.add_arc('l_pl', 'ɛ_plɛ', 'ɛ', [])

    f.add_state('d_plɛd')
    f.add_arc('ɛ_plɛ', 'd_plɛd', 'd', [])

    f.add_arc('d_plɛd', 'end', '#', 'plid# PST/ PST.PTCP')

    #proven --> prove PST.PTCP
    f.add_state('ɹ_pɹ')
    f.add_arc('p', 'ɹ_pɹ', 'ɹ', [])

    f.add_state('o_pɹo')
    f.add_arc('ɹ_pɹ', 'o_pɹo', 'o', [])

    f.add_state('ʊ_pɹoʊ')
    f.add_arc('o_pɹo', 'ʊ_pɹoʊ', 'ʊ', [])

    f.add_state('v_pɹoʊv')
    f.add_arc('ʊ_pɹoʊ', 'v_pɹoʊv', 'v', [])

    f.add_state('ə_pɹoʊvə')
    f.add_arc('v_pɹoʊv', 'ə_pɹoʊvə', 'ə', [])

    f.add_state('n_pɹoʊvən')
    f.add_arc('ə_pɹoʊvə', 'n_pɹoʊvən', 'n', [])

    f.add_arc('n_pɹoʊvən', 'end', '#', 'pɹuv# PST.PTCP')
    
    #put --> put PST/ PST.PTCP
    f.add_state('ʊ_pʊ')
    f.add_arc('p', 'ʊ_pʊ', 'ʊ', [])

    f.add_state('t_pʊt')
    f.add_arc('ʊ_pʊ', 't_pʊt', 't', [])

    f.add_arc('t_pʊt', 'end', '#', 'pʊt# PST/ PST.PTCP')

    #read --> reaf PST/ PST.PTCP
    f.add_state('ɹ')
    f.add_arc('marker', 'ɹ', 'ɹ', [])

    f.add_state('ɛ_ɹɛ')
    f.add_arc('ɹ', 'ɛ_ɹɛ', 'ɛ', [])

    f.add_state('d_ɹɛd')
    f.add_arc('ɛ_ɹɛ', 'd_ɹɛd', 'd', [])

    f.add_arc('d_ɹɛd', 'end', '#', 'ɹid# PST/ PST.PTCP')

    #rode --> ride PST
    f.add_state('o_ɹo')
    f.add_arc('ɹ', 'o_ɹo', 'o', [])

    f.add_state('ʊ_ɹoʊ')
    f.add_arc('o_ɹo', 'ʊ_ɹoʊ', 'ʊ', [])

    f.add_state('d_ɹoʊd')
    f.add_arc('ʊ_ɹoʊ', 'd_ɹoʊd', 'd', [])

    f.add_arc('d_ɹoʊd', 'end', '#', 'ɹaɪd# PST')

    #ridden --> ride PST.PTCP
    f.add_state('ɪ_ɹɪ')
    f.add_arc('ɹ', 'ɪ_ɹɪ', 'ɪ', [])

    f.add_state('d_ɹɪd')
    f.add_arc('ɪ_ɹɪ', 'd_ɹɪd', 'd', [])

    f.add_state('ə_ɹɪdə')
    f.add_arc('d_ɹɪd', 'ə_ɹɪdə', 'ə', [])

    f.add_state('n_ɹɪdən')
    f.add_arc('ə_ɹɪdə', 'n_ɹɪdən', 'n', [])

    f.add_arc('n_ɹɪdən', 'end', '#', 'ɹaɪd# PST.PTCP')

    #wrote --> write PST
    f.add_state('t_ɹoʊt')
    f.add_arc('ʊ_ɹoʊ', 't_ɹoʊt', 't', [])

    f.add_arc('t_ɹoʊt', 'end', '#', 'ɹaɪt# PST')

    #written --> write PST.PTCP
    f.add_state('t_ɹɪt')
    f.add_arc('ɪ_ɹɪ', 't_ɹɪt', 't', [])

    f.add_state('ə_ɹɪtə')
    f.add_arc('t_ɹɪt', 'ə_ɹɪtə', 'ə', [])

    f.add_state('n_ɹɪtən')
    f.add_arc('ə_ɹɪtə', 'n_ɹɪtən', 'n', [])

    f.add_arc('n_ɹɪtən', 'end', '#', 'ɹaɪt# PST.PTCP')

    #rang --> ring PST
    f.add_state('æ_ɹæ')
    f.add_arc('ɹ', 'æ_ɹæ', 'æ', [])

    f.add_state('ŋ_ɹæŋ')
    f.add_arc('æ_ɹæ', 'ŋ_ɹæŋ', 'ŋ', [])

    f.add_arc('ŋ_ɹæŋ', 'end', '#', 'ɹɪŋ# PST')

    #rung --> ring PST.PTCP
    f.add_state('ʌ_ɹʌ')
    f.add_arc('ɹ', 'ʌ_ɹʌ', 'ʌ', [])

    f.add_state('ŋ_ɹʌŋ')
    f.add_arc('ʌ_ɹʌ', 'ŋ_ɹʌŋ', 'ŋ', [])

    f.add_arc('ŋ_ɹʌŋ', 'end', '#', 'ɹɪŋ# PST.PTCP')

    #rose --> rise PST
    f.add_state('z_ɹoʊz')
    f.add_arc('ʊ_ɹoʊ', 'z_ɹoʊz', 'z', [])

    f.add_arc('z_ɹoʊz', 'end', '#', 'ɹaɪz# PST')

    #risen --> rise PST.PTCP
    f.add_state('z_ɹɪz')
    f.add_arc('ɪ_ɹɪ', 'z_ɹɪz', 'z', [])

    f.add_state('ə_ɹɪzə')
    f.add_arc('z_ɹɪz', 'ə_ɹɪzə', 'ə', [])

    f.add_state('n_ɹɪzən')
    f.add_arc('ə_ɹɪzə', 'n_ɹɪzən', 'n', [])

    f.add_arc('n_ɹɪzən', 'end', '#', 'ɹaɪz# PST.PTCP')

    #ran --> run PST
    f.add_state('n_ɹæn')
    f.add_arc('æ_ɹæ', 'n_ɹæn', 'n', [])

    f.add_arc('n_ɹæn', 'end', '#', 'ɹʌn# PST')

    #run --> run PST.PTCP
    f.add_state('n_ɹʌn')
    f.add_arc('ʌ_ɹʌ', 'n_ɹʌn', 'n', [])

    f.add_arc('n_ɹʌn', 'end', '#', 'ɹʌn# PST.PTCP')

    #shook --> shake PST
    f.add_state('ʃ')
    f.add_arc('marker', 'ʃ', 'ʃ', [])

    f.add_state('ʊ_ʃʊ')
    f.add_arc('ʃ', 'ʊ_ʃʊ', 'ʊ', [])

    f.add_state('k_ʃʊk')
    f.add_arc('ʊ_ʃʊ', 'k_ʃʊk', 'k', [])

    f.add_arc('k_ʃʊk', 'end', '#', 'ʃeɪk# PST')

    #shaken --> shake PST.PTCP
    f.add_state('e_ʃe')
    f.add_arc('ʃ', 'e_ʃe', 'e', [])

    f.add_state('ɪ_ʃeɪ')
    f.add_arc('e_ʃe', 'ɪ_ʃeɪ', 'ɪ', [])

    f.add_state('k_ʃeɪk')
    f.add_arc('ɪ_ʃeɪ', 'k_ʃeɪk', 'k', [])

    f.add_state('ə_ʃeɪkə')
    f.add_arc('k_ʃeɪk', 'ə_ʃeɪkə', 'ə', [])

    f.add_state('n_ʃeɪkən')
    f.add_arc('ə_ʃeɪkə', 'n_ʃeɪkən', 'n', [])

    f.add_arc('n_ʃeɪkən', 'end', '#', 'ʃeɪk# PST.PTCP')

    #shone --> shine PST/ PST.PTCP
    f.add_state('o_ʃo')
    f.add_arc('ʃ', 'o_ʃo', 'o', [])

    f.add_state('ʊ_ʃoʊ')
    f.add_arc('o_ʃo', 'ʊ_ʃoʊ', 'ʊ', [])

    f.add_state('n_ʃoʊn')
    f.add_arc('ʊ_ʃoʊ', 'n_ʃoʊn', 'n', [])

    f.add_arc('n_ʃoʊn', 'end', '#', 'ʃaɪn# PST/ PST.PTCP')

    #shot --> shoot PST/ PST.PTCP
    f.add_state('ɑ_ʃɑ')
    f.add_arc('ʃ', 'ɑ_ʃɑ', 'ɑ', [])

    f.add_state('t_ʃɑt')
    f.add_arc('ɑ_ʃɑ', 't_ʃɑt', 't', [])

    f.add_arc('t_ʃɑt', 'end', '#', 'ʃut# PST/ PST.PTCP')

    #shown --> show PST.PTCP
    f.add_arc('n_ʃoʊn', 'end', '#', 'ʃoʊ# PST.PTCP')

    #shrank --> shrink PST
    f.add_state('ɹ_ʃɹ')
    f.add_arc('ʃ', 'ɹ_ʃɹ', 'ɹ', [])

    f.add_state('æ_ʃɹæ')
    f.add_arc('ɹ_ʃɹ', 'æ_ʃɹæ', 'æ', [])

    f.add_state('ŋ_ʃɹæŋ')
    f.add_arc('æ_ʃɹæ', 'ŋ_ʃɹæŋ', 'ŋ', [])

    f.add_state('k_ʃɹæŋk')
    f.add_arc('ŋ_ʃɹæŋ', 'k_ʃɹæŋk', 'k', [])

    f.add_arc('k_ʃɹæŋk', 'end', '#', 'ʃɹɪŋk# PST')

    #shrunk --> shrunk PST.PTCP
    f.add_state('ʌ_ʃɹʌ')
    f.add_arc('ɹ_ʃɹ', 'ʌ_ʃɹʌ', 'ʌ', [])

    f.add_state('ŋ_ʃɹʌŋ')
    f.add_arc('ʌ_ʃɹʌ', 'ŋ_ʃɹʌŋ', 'ŋ', [])

    f.add_state('k_ʃɹʌŋk')
    f.add_arc('ŋ_ʃɹʌŋ', 'k_ʃɹʌŋk', 'k', [])

    f.add_arc('k_ʃɹʌŋk', 'end', '#', 'ʃɹɪŋk# PST.PTCP')

    #shut --> shut PST/ PST.PTCP
    f.add_state('ʌ_ʃʌ')
    f.add_arc('ʃ', 'ʌ_ʃʌ', 'ʌ', [])

    f.add_state('t_ʃʌt')
    f.add_arc('ʌ_ʃʌ', 't_ʃʌt', 't', [])

    f.add_arc('t_ʃʌt', 'end', '#', 'ʃʌt# PST/ PST.PTCP')

    #said --> say PST/ PST.PTCP
    f.add_state('s')
    f.add_arc('marker', 's', 's', [])

    f.add_state('ɛ_sɛ')
    f.add_arc('s', 'ɛ_sɛ', 'ɛ', [])

    f.add_state('d_sɛd')
    f.add_arc('ɛ_sɛ', 'd_sɛd', 'd', [])

    f.add_arc('d_sɛd', 'end', '#', 'seɪ# PST/ PST.PTCP')

    #says --> say PRES
    f.add_state('z_sɛz')
    f.add_arc('ɛ_sɛ', 'z_sɛz', 'z', [])

    f.add_arc('z_sɛz', 'end', '#', 'seɪ# PRES')

    #saw --> see PST
    f.add_state('ɔ_sɔ')
    f.add_arc('s', 'ɔ_sɔ', 'ɔ', [])

    f.add_arc('ɔ_sɔ', 'end', '#', 'si# PST')

    #seen --> see PST.PTCP
    f.add_state('i_si')
    f.add_arc('s', 'i_si', 'i', [])

    f.add_state('n_sin')
    f.add_arc('i_si', 'n_sin', 'n', [])

    f.add_arc('n_sin', 'end', '#', 'si# PST.PTCP')

    #sought --> seek PST/ PST.PTCP
    f.add_state('t_sɔt')
    f.add_arc('ɔ_sɔ', 't_sɔt', 't', [])

    f.add_arc('t_sɔt', 'end', '#', 'sik# PST/ PST.PTCP')

    #sold --> sell PST/ PST.PTCP
    f.add_state('o_so')
    f.add_arc('s', 'o_so', 'o', [])

    f.add_state('ʊ_soʊ')
    f.add_arc('o_so', 'ʊ_soʊ', 'ʊ', [])

    f.add_state('l_soʊl')
    f.add_arc('ʊ_soʊ', 'l_soʊl', 'l', [])

    f.add_state('d_soʊld')
    f.add_arc('l_soʊl', 'd_soʊld', 'd', [])

    f.add_arc('d_soʊld', 'end', '#', 'sɛl# PST/ PST.PTCP')

    #sent --> send PST/ PST.PTCP
    f.add_state('n_sɛn')
    f.add_arc('ɛ_sɛ', 'n_sɛn', 'n', [])

    f.add_state('t_sɛnt')
    f.add_arc('n_sɛn', 't_sɛnt', 't', [])

    f.add_arc('t_sɛnt', 'end', '#', 'sɛnd# PST/ PST.PTCP')

    #set --> set PST/ PST.PTCP
    f.add_state('t_sɛt')
    f.add_arc('ɛ_sɛ', 't_sɛt', 't', [])

    f.add_arc('t_sɛt', 'end', '#', 'sɛt# PST/ PST.PTCP')

    #sang --> sing PST
    f.add_state('æ_sæ')
    f.add_arc('s', 'æ_sæ', 'æ', [])

    f.add_state('ŋ_sæŋ')
    f.add_arc('æ_sæ', 'ŋ_sæŋ', 'ŋ', [])

    f.add_arc('ŋ_sæŋ', 'end', '#', 'sɪŋ# PST')

    #sung --> sung PST.PTCP
    f.add_state('ʌ_sʌ')
    f.add_arc('s', 'ʌ_sʌ', 'ʌ', [])

    f.add_state('ŋ_sʌŋ')
    f.add_arc('ʌ_sʌ', 'ŋ_sʌŋ', 'ŋ', [])

    f.add_arc('ŋ_sʌŋ', 'end', '#', 'sɪŋ# PST.PTCP')

    #sank --> sink PST
    f.add_state('k_sæŋk')
    f.add_arc('ŋ_sæŋ', 'k_sæŋk', 'k', [])

    f.add_arc('k_sæŋk', 'end', '#', 'sɪŋk# PST')

    #sunk --> sink PST.PTCP
    f.add_state('k_sʌŋk')
    f.add_arc('ŋ_sʌŋ', 'k_sʌŋk', 'k', [])

    f.add_arc('k_sʌŋk', 'end', '#', 'sɪŋk# PST.PTCP')

    #sat --> sit PST/ PST.PTCP
    f.add_state('t_sæt')
    f.add_arc('æ_sæ', 't_sæt', 't', [])

    f.add_arc('t_sæt', 'end', '#', 'sɪt# PST/ PST.PTCP')

    #slain --> slay PST.PTCP
    f.add_state('l_sl')
    f.add_arc('s', 'l_sl', 'l', [])

    f.add_state('e_sle')
    f.add_arc('l_sl', 'e_sle', 'e', [])

    f.add_state('ɪ_sleɪ')
    f.add_arc('e_sle', 'ɪ_sleɪ', 'ɪ', [])

    f.add_state('n_sleɪn')
    f.add_arc('ɪ_sleɪ', 'n_sleɪn', 'n', [])

    f.add_arc('n_sleɪn', 'end', '#', 'sleɪ# PST.PTCP')

    #slept --> sleep PST/ PST.PTCP
    f.add_state('ɛ_slɛ')
    f.add_arc('l_sl', 'ɛ_slɛ', 'ɛ', [])

    f.add_state('p_slɛp')
    f.add_arc('ɛ_slɛ', 'p_slɛp', 'p', [])

    f.add_state('t_slɛpt')
    f.add_arc('p_slɛp', 't_slɛpt', 't', [])

    f.add_arc('t_slɛpt', 'end', '#', 'slip# PST/ PST.PTCP')

    #slid --> slide PST/ PST.PTCP
    f.add_state('ɪ_slɪ')
    f.add_arc('l_sl', 'ɪ_slɪ', 'ɪ', [])

    f.add_state('d_slɪd')
    f.add_arc('ɪ_slɪ', 'd_slɪd', 'd', [])

    f.add_arc('d_slɪd', 'end', '#', 'slaɪd# PST/ PST.PTCP')

    #slit --> slit PST/ PST.PTCP
    f.add_state('t_slɪt')
    f.add_arc('ɪ_slɪ', 't_slɪt', 't', [])

    f.add_arc('t_slɪt', 'end', '#', 'slɪt# PST/ PST.PTCP')

    #spoke --> speak PST
    f.add_state('p_sp')
    f.add_arc('s', 'p_sp', 'p', [])

    f.add_state('o_spo')
    f.add_arc('p_sp', 'o_spo', 'o', [])

    f.add_state('ʊ_spoʊ')
    f.add_arc('o_spo', 'ʊ_spoʊ', 'ʊ', [])

    f.add_state('k_spoʊk')
    f.add_arc('ʊ_spoʊ', 'k_spoʊk', 'k', [])

    f.add_arc('k_spoʊk', 'end', '#', 'spik# PST')

    #spoken --> speak PST.PTCP
    f.add_state('ə_spoʊkə')
    f.add_arc('k_spoʊk', 'ə_spoʊkə', 'ə', [])

    f.add_state('n_spoʊkən')
    f.add_arc('ə_spoʊkə', 'n_spoʊkən', 'n', [])

    f.add_arc('n_spoʊkən', 'end', '#', 'spik# PST.PTCP')

    #spent --> spend PST/ PST.PTCP
    f.add_state('ɛ_spɛ')
    f.add_arc('p_sp', 'ɛ_spɛ', 'ɛ', [])

    f.add_state('n_spɛn')
    f.add_arc('ɛ_spɛ', 'n_spɛn', 'n', [])

    f.add_state('t_spɛnt')
    f.add_arc('n_spɛn', 't_spɛnt', 't', [])

    f.add_arc('t_spɛnt', 'end', '#', 'spɛnd# PST/ PST.PTCP')

    #spun --> spin PST/ PST.PTCP
    f.add_state('ʌ_spʌ')
    f.add_arc('p_sp', 'ʌ_spʌ', 'ʌ', [])

    f.add_state('n_spʌn')
    f.add_arc('ʌ_spʌ', 'n_spʌn', 'n', [])

    f.add_arc('n_spʌn', 'end', '#', 'spɪn# PST/ PST.PTCP')

    #spat --> spit PST/ PST.PTCP
    f.add_state('æ_spæ')
    f.add_arc('p_sp', 'æ_spæ', 'æ', [])

    f.add_state('t_spæt')
    f.add_arc('æ_spæ', 't_spæt', 't', [])

    f.add_arc('t_spæt', 'end', '#', 'spɪt# PST/ PST.PTCP')

    #spit --> spit PST/ PST.PTCP
    f.add_state('ɪ_spɪ')
    f.add_arc('p_sp', 'ɪ_spɪ', 'ɪ', [])

    f.add_state('t_spɪt')
    f.add_arc('ɪ_spɪ', 't_spɪt', 't', [])

    f.add_arc('t_spɪt', 'end', '#', 'spɪt# PST/ PST.PTCP')

    #spread --> spread PST/ PST.PTCP
    f.add_state('ɹ_spɹ')
    f.add_arc('p_sp', 'ɹ_spɹ', 'ɹ', [])

    f.add_state('ɛ_spɹɛ')
    f.add_arc('ɹ_spɹ', 'ɛ_spɹɛ', 'ɛ', [])

    f.add_state('d_spɹɛd')
    f.add_arc('ɛ_spɹɛ', 'd_spɹɛd', 'd', [])

    f.add_arc('d_spɹɛd', 'end', '#', 'spɹɛd# PST/ PST.PTCP')

    #sprang --> spring PST
    f.add_state('æ_spɹæ')
    f.add_arc('ɹ_spɹ', 'æ_spɹæ', 'æ', [])

    f.add_state('ŋ_spɹæŋ')
    f.add_arc('æ_spɹæ', 'ŋ_spɹæŋ', 'ŋ', [])

    f.add_arc('ŋ_spɹæŋ', 'end', '#', 'spɹɪŋ# PST')

    #sprung --> spring PST.PTCP
    f.add_state('ʌ_spɹʌ')
    f.add_arc('ɹ_spɹ', 'ʌ_spɹʌ', 'ʌ', [])

    f.add_state('ŋ_spɹʌŋ')
    f.add_arc('ʌ_spɹʌ', 'ŋ_spɹʌŋ', 'ŋ', [])

    f.add_arc('ŋ_spɹʌŋ', 'end', '#', 'spɹɪŋ# PST.PTCP')

    #stood --> stand PST/ PST.PTCP
    f.add_state('t_st')
    f.add_arc('s', 't_st', 't', [])

    f.add_state('ʊ_stʊ')
    f.add_arc('t_st', 'ʊ_stʊ', 'ʊ', [])

    f.add_state('d_stʊd')
    f.add_arc('ʊ_stʊ', 'd_stʊd', 'd', [])

    f.add_arc('d_stʊd', 'end', '#', 'stænd# PST/ PST.PTCP')

    #stole --> steal PST
    f.add_state('o_sto')
    f.add_arc('t_st', 'o_sto', 'o', [])

    f.add_state('ʊ_stoʊ')
    f.add_arc('o_sto', 'ʊ_stoʊ', 'ʊ', [])

    f.add_state('l_stoʊl')
    f.add_arc('ʊ_stoʊ', 'l_stoʊl', 'l', [])

    f.add_arc('l_stoʊl', 'end', '#', 'stil# PST')

    #stolen --> steal PST.PTCP
    f.add_state('ə_stoʊlə')
    f.add_arc('l_stoʊl', 'ə_stoʊlə', 'ə', [])

    f.add_state('n_stoʊlən')
    f.add_arc('ə_stoʊlə', 'n_stoʊlən', 'n', [])

    f.add_arc('n_stoʊlən', 'end', '#', 'stil# PST.PTCP')

    #stuck --> stick PST/ PST.PTCP
    f.add_state('ʌ_stʌ')
    f.add_arc('t_st', 'ʌ_stʌ', 'ʌ', [])

    f.add_state('k_stʌk')
    f.add_arc('ʌ_stʌ', 'k_stʌk', 'k', [])

    f.add_arc('k_stʌk', 'end', '#', 'stɪk# PST/ PST.PTCP')

    #stung --> sting PST/ PST.PTCP
    f.add_state('ŋ_stʌŋ')
    f.add_arc('ʌ_stʌ', 'ŋ_stʌŋ', 'ŋ', [])

    f.add_arc('ŋ_stʌŋ', 'end', '#', 'stɪŋ# PST/ PST.PTCP')

    #stank --> stink PST
    f.add_state('æ_stæ')
    f.add_arc('t_st', 'æ_stæ', 'æ', [])

    f.add_state('ŋ_stæŋ')
    f.add_arc('æ_stæ', 'ŋ_stæŋ', 'ŋ', [])

    f.add_state('k_stæŋk')
    f.add_arc('ŋ_stæŋ', 'k_stæŋk', 'k', [])

    f.add_arc('k_stæŋk', 'end', '#', 'stɪŋk# PST')

    #stunk --> stink PST.PTCP
    f.add_state('k_stʌŋk')
    f.add_arc('ŋ_stʌŋ', 'k_stʌŋk', 'k', [])

    f.add_arc('k_stʌŋk', 'end', '#', 'stɪŋk# PST.PTCP')

    #strode --> stride PST
    f.add_state('ɹ_str')
    f.add_arc('t_st', 'ɹ_str', 'ɹ', [])

    f.add_state('o_stɹo')
    f.add_arc('ɹ_str', 'o_stɹo', 'o', [])

    f.add_state('ʊ_stɹoʊ')
    f.add_arc('o_stɹo', 'ʊ_stɹoʊ', 'ʊ', [])

    f.add_state('d_stɹoʊd')
    f.add_arc('ʊ_stɹoʊ', 'd_stɹoʊd', 'd', [])

    f.add_arc('d_stɹoʊd', 'end', '#', 'stɹaɪd# PST')

    #stridden --> stride PST.PTCP
    f.add_state('ɪ_stɹɪ')
    f.add_arc('ɹ_str', 'ɪ_stɹɪ', 'ɪ', [])

    f.add_state('d_stɹɪd')
    f.add_arc('ɪ_stɹɪ', 'd_stɹɪd', 'd', [])

    f.add_state('ə_stɹɪdə')
    f.add_arc('d_stɹɪd', 'ə_stɹɪdə', 'ə', [])

    f.add_state('n_stɹɪdən')
    f.add_arc('ə_stɹɪdə', 'n_stɹɪdən', 'n', [])

    f.add_arc('n_stɹɪdən', 'end', '#', 'stɹaɪd# PST.PTCP')

    #struck --> strike PST/ PST.PTCP
    f.add_state('ʌ_stɹʌ')
    f.add_arc('ɹ_str', 'ʌ_stɹʌ', 'ʌ', [])

    f.add_state('k_stɹʌk')
    f.add_arc('ʌ_stɹʌ', 'k_stɹʌk', 'k', [])

    f.add_arc('k_stɹʌk', 'end', '#', 'stɹaɪk# PST/ PST.PTCP')

    #strung --> string PST/ PST.PTCP
    f.add_state('ŋ_stɹʌŋ')
    f.add_arc('ʌ_stɹʌ', 'ŋ_stɹʌŋ', 'ŋ', [])

    f.add_arc('ŋ_stɹʌŋ', 'end', '#', 'stɹɪŋ# PST/ PST.PTCP')

    #swore --> swear PST
    f.add_state('w_sw')
    f.add_arc('s', 'w_sw', 'w', [])

    f.add_state('ɔ_swɔ')
    f.add_arc('w_sw', 'ɔ_swɔ', 'ɔ', [])

    f.add_state('ɹ_swɔɹ')
    f.add_arc('ɔ_swɔ', 'ɹ_swɔɹ', 'ɹ', [])

    f.add_arc('ɹ_swɔɹ', 'end', '#', 'swɛɹ# PST')

    #sworn --> swear PST.PTCP
    f.add_state('n_swɔɹn')
    f.add_arc('ɹ_swɔɹ', 'n_swɔɹn', 'n', [])

    f.add_arc('n_swɔɹn', 'end', '#', 'swɛɹ# PST.PTCP')

    #swept --> sweep PST/ PST.PTCP
    f.add_state('ɛ_swɛ')
    f.add_arc('w_sw', 'ɛ_swɛ', 'ɛ', [])

    f.add_state('p_swɛp')
    f.add_arc('ɛ_swɛ', 'p_swɛp', 'p', [])

    f.add_state('t_swɛpt')
    f.add_arc('p_swɛp', 't_swɛpt', 't', [])

    f.add_arc('t_swɛpt', 'end', '#', 'swip# PST/ PST.PTCP')

    #swelled --> swell PST
    f.add_state('l_swɛl')
    f.add_arc('ɛ_swɛ', 'l_swɛl', 'l', [])

    f.add_state('d_swɛld')
    f.add_arc('l_swɛl', 'd_swɛld', 'd', [])

    f.add_arc('d_swɛld', 'end', '#', 'swɛl# PST')

    #swollen --> swell PST.PTCP
    f.add_state('o_swo')
    f.add_arc('w_sw', 'o_swo', 'o', [])

    f.add_state('ʊ_swoʊ')
    f.add_arc('o_swo', 'ʊ_swoʊ', 'ʊ', [])

    f.add_state('l_swoʊl')
    f.add_arc('ʊ_swoʊ', 'l_swoʊl', 'l', [])

    f.add_state('ə_swoʊlə')
    f.add_arc('l_swoʊl', 'ə_swoʊlə', 'ə', [])

    f.add_state('n_swoʊlən')
    f.add_arc('ə_swoʊlə', 'n_swoʊlən', 'n', [])

    f.add_arc('n_swoʊlən', 'end', '#', 'swɛl# PST.PTCP')

    #swam --> swim PST
    f.add_state('æ_swæ')
    f.add_arc('w_sw', 'æ_swæ', 'æ', [])

    f.add_state('m_swæm')
    f.add_arc('æ_swæ', 'm_swæm', 'm', [])

    f.add_arc('m_swæm', 'end', '#', 'swɪm# PST')

    #swum --> swum PST
    f.add_state('ʌ_swʌ')
    f.add_arc('w_sw', 'ʌ_swʌ', 'ʌ', [])

    f.add_state('m_swʌm')
    f.add_arc('ʌ_swʌ', 'm_swʌm', 'm', [])

    f.add_arc('m_swʌm', 'end', '#', 'swɪm# PST.PTCP')

    #swang --> swing PST
    f.add_state('ŋ_swæŋ')
    f.add_arc('æ_swæ', 'ŋ_swæŋ', 'ŋ', [])

    f.add_arc('ŋ_swæŋ', 'end', '#', 'swɪŋ# PST')

    #swung --> swing PST.PTCP
    f.add_state('ŋ_swʌŋ')
    f.add_arc('ʌ_swʌ', 'ŋ_swʌŋ', 'ŋ', [])

    f.add_arc('ŋ_swʌŋ', 'end', '#', 'swɪŋ# PST.PTCP')

    #took --> take PST
    f.add_state('t')
    f.add_arc('marker', 't', 't', [])

    f.add_state('ʊ_tʊ')
    f.add_arc('t', 'ʊ_tʊ', 'ʊ', [])

    f.add_state('k_tʊk')
    f.add_arc('ʊ_tʊ', 'k_tʊk', 'k', [])

    f.add_arc('k_tʊk', 'end', '#', 'teɪk# PST')

    #taken --> take PST.PTCP
    f.add_state('e_te')
    f.add_arc('t', 'e_te', 'e', [])

    f.add_state('ɪ_teɪ')
    f.add_arc('e_te', 'ɪ_teɪ', 'ɪ', [])

    f.add_state('k_teɪk')
    f.add_arc('ɪ_teɪ', 'k_teɪk', 'k', [])

    f.add_state('ə_teɪkə')
    f.add_arc('k_teɪk', 'ə_teɪkə', 'ə', [])

    f.add_state('n_teɪkən')
    f.add_arc('ə_teɪkə', 'n_teɪkən', 'n', [])

    f.add_arc('n_teɪkən', 'end', '#', 'teɪk# PST.PTCP')

    #taught --> teach PST/ PST.PTCP
    f.add_state('ɔ_tɔ')
    f.add_arc('t', 'ɔ_tɔ', 'ɔ', [])

    f.add_state('t_tɔt')
    f.add_arc('ɔ_tɔ', 't_tɔt', 't', [])

    f.add_arc('t_tɔt', 'end', '#', 'titʃ# PST/ PST.PTCP')

    #tore --> tear PST
    f.add_state('ɹ_tɔɹ')
    f.add_arc('ɔ_tɔ', 'ɹ_tɔɹ', 'ɹ', [])

    f.add_arc('ɹ_tɔɹ', 'end', '#', 'tɛɹ# PST')

    #torn --> tear PST.PTCP
    f.add_state('n_tɔɹn')
    f.add_arc('ɹ_tɔɹ', 'n_tɔɹn', 'n', [])

    f.add_arc('n_tɔɹn', 'end', '#', 'tɛɹ# PST.PTCP')

    #told --> tell PST/ PST.PTCP
    f.add_state('o_to')
    f.add_arc('t', 'o_to', 'o', [])

    f.add_state('ʊ_toʊ')
    f.add_arc('o_to', 'ʊ_toʊ', 'ʊ', [])

    f.add_state('l_toʊl')
    f.add_arc('ʊ_toʊ', 'l_toʊl', 'l', [])

    f.add_state('d_toʊld')
    f.add_arc('l_toʊl', 'd_toʊld', 'd', [])

    f.add_arc('d_toʊld', 'end', '#', 'tɛl# PST/ PST.PTCP')

    #thought --> think PST/ PST.PTCP
    f.add_state('θ')
    f.add_arc('marker', 'θ', 'θ', [])

    f.add_state('ɔ_θɔ')
    f.add_arc('θ', 'ɔ_θɔ', 'ɔ', [])

    f.add_state('t_θɔt')
    f.add_arc('ɔ_θɔ', 't_θɔt', 't', [])

    f.add_arc('t_θɔt', 'end', '#', 'θɪŋk# PST/ PST.PTCP')

    #threw --> throw PST
    f.add_state('ɹ_θɹ')
    f.add_arc('θ', 'ɹ_θɹ', 'ɹ', [])

    f.add_state('u_θɹu')
    f.add_arc('ɹ_θɹ', 'u_θɹu', 'u', [])

    f.add_arc('u_θɹu', 'end', '#', 'θɹoʊ# PST')

    #thrown --> throw PST.PTCP
    f.add_state('o_θɹo')
    f.add_arc('ɹ_θɹ', 'o_θɹo', 'o', [])

    f.add_state('ʊ_θɹoʊ')
    f.add_arc('o_θɹo', 'ʊ_θɹoʊ', 'ʊ', [])

    f.add_state('n_θɹoʊn')
    f.add_arc('ʊ_θɹoʊ', 'n_θɹoʊn', 'ʊ', [])

    f.add_arc('n_θɹoʊn', 'end', '#', 'θɹoʊ# PST.PTCP')

    #woke --> wake PST
    f.add_state('w')
    f.add_arc('marker', 'w', 'w', [])

    f.add_state('o_wo')
    f.add_arc('w', 'o_wo', 'o', [])

    f.add_state('ʊ_woʊ')
    f.add_arc('o_wo', 'ʊ_woʊ', 'ʊ', [])

    f.add_state('k_woʊk')
    f.add_arc('ʊ_woʊ', 'k_woʊk', 'k', [])

    f.add_arc('k_woʊk', 'end', '#', 'weɪk# PST')

    #woken --> wake PST.PTCP
    f.add_state('ə_woʊkə')
    f.add_arc('k_woʊk', 'ə_woʊkə', 'ə', [])

    f.add_state('n_woʊkən')
    f.add_arc('ə_woʊkə', 'n_woʊkən', 'n', [])

    f.add_arc('n_woʊkən', 'end', '#', 'weɪk# PST.PTCP')

    #wore --> wear PST
    f.add_state('ɔ_wɔ')
    f.add_arc('w', 'ɔ_wɔ', 'ɔ', [])

    f.add_state('ɹ_wɔɹ')
    f.add_arc('ɔ_wɔ', 'ɹ_wɔɹ', 'ɹ', [])

    f.add_arc('ɹ_wɔɹ', 'end', '#', 'wɛɹ# PST')

    #worn --> wear PST.PTCP
    f.add_state('n_wɔɹn')
    f.add_arc('ɹ_wɔɹ', 'n_wɔɹn', 'n', [])

    f.add_arc('n_wɔɹn', 'end', '#', 'wɛɹ# PST.PTCP')

    #wed --> wed PST/ PST.PTCP
    f.add_state('ɛ_wɛ')
    f.add_arc('w', 'ɛ_wɛ', 'ɛ', [])

    f.add_state('d_wɛd')
    f.add_arc('ɛ_wɛ', 'd_wɛd', 'd', [])

    f.add_arc('d_wɛd', 'end', '#', 'wɛd# PST/ PST.PTCP')

    #wet --> wet PST/ PST.PTCP
    f.add_state('t_wɛt')
    f.add_arc('ɛ_wɛ', 't_wɛt', 't', [])

    f.add_arc('t_wɛt', 'end', '#', 'wɛt# PST/ PST.PTCP')

    #went --> go PST
    f.add_state('n_wɛn')
    f.add_arc('ɛ_wɛ', 'n_wɛn', 'n', [])

    f.add_state('t_wɛnt')
    f.add_arc('n_wɛn', 't_wɛnt', 't', [])

    f.add_arc('t_wɛnt', 'end', '#', 'goʊ# PST')

    #was --> is PST
    f.add_state('ɑ_wɑ')
    f.add_arc('w', 'ɑ_wɑ', 'ɑ', [])

    f.add_state('z_wɑz')
    f.add_arc('ɑ_wɑ', 'z_wɑz', 'z', [])

    f.add_arc('z_wɑz', 'end', '#', 'bi# PST')

    #wept --> weep PST/ PST.PTCP
    f.add_state('p_wɛp')
    f.add_arc('ɛ_wɛ', 'p_wɛp', 'p', [])

    f.add_state('t_wɛpt')
    f.add_arc('p_wɛp', 't_wɛpt', 't', [])

    f.add_arc('t_wɛpt', 'end', '#', 'wip# PST/ PST.PTCP')

    #won --> win PST / PST.PTCP
    f.add_state('ʌ_wʌ')
    f.add_arc('w', 'ʌ_wʌ', 'ʌ', [])

    f.add_state('n_wʌn')
    f.add_arc('ʌ_wʌ', 'n_wʌn', 'n', [])

    f.add_arc('n_wʌn', 'end', '#', 'wɪn# PST/ PST.PTCP')

    return f


def final_morph_analyzer_fst(inp):
    f_irreg = morph_analyzer_irregular()
    out = f_irreg.transduce(inp)

    if out:
        return out

    f_reg = morph_analyzer_regular()
    return f_reg.transduce(inp)