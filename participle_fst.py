import sys
from fst import FST
from fsmutils import composewords, trace

voiced = ['b', 'm', 'ð', 'ɹ', 'l', 'j', 'v', 'ɡ', 'ɫ', 'g',
          'ŋ', 'ɪ', 'ɛ', 'æ', 'ʌ', 'ʊ', 'ɒ', 'ə', 'e', 'z',
          'a', 'ɔ', 'o', 'w', 'n', 'i', 'u', 'ɑ', 'r', 'ɝ',
          'ʤ', 'ʒ']
voiceless = ['p', 'f', 'θ', 'k', 'h', 's', 'ʃ', 'ʧ']
alveolar = ['t', 'd']
markers = ['\'', '#', '.', '_', '-']


def participle_regular():

    f = FST('past_reg')

    f.add_state('start')
    f.add_state('voiced')
    f.add_state('voiceless')
    f.add_state('alveolar')
    f.add_state('marker')
    f.add_state('end')

    f.initial_state = 'start'
    f.set_final('end')

    # starting arcs
    """
    for char in voiced: 
        f.add_arc('start', 'voiced', char, char)
    
    for char in voiceless:
        f.add_arc('start', 'voiceless', char, char)
    
    for char in alveolar:
        f.add_arc('start', 'alveolar', char, char)
        """
    
    for char in markers:
        f.add_arc('start', 'marker', char, char)

    # voiced arcs
    for char in voiced:
        f.add_arc('voiced', 'voiced', char, char)
    
    for char in voiceless:
        f.add_arc('voiced', 'voiceless', char, char)
    
    for char in alveolar:
        f.add_arc('voiced', 'alveolar', char, char)

    for char in markers:
        f.add_arc('voiced', 'marker', char, char)

    # voiceless arcs
    for char in voiceless:
        f.add_arc('voiceless', 'voiceless', char, char)
    
    for char in voiced:
        f.add_arc('voiceless', 'voiced', char, char)
    
    for char in alveolar:
        f.add_arc('voiceless', 'alveolar', char, char)
    
    for char in markers: 
        f.add_arc('voiceless', 'marker', char, char)

    # alveolar arcs
    for char in alveolar:
        f.add_arc('alveolar', 'alveolar', char, char)
    
    for char in voiced:
        f.add_arc('alveolar', 'voiced', char, char)

    for char in voiceless:
        f.add_arc('alveolar', 'voiceless', char, char)

    for char in markers:
        f.add_arc('alveolar', 'marker', char, char)

    # marker arcs
    for char in markers:
        f.add_arc('marker', 'marker', char, char)

    for char in voiced:
        f.add_arc('marker', 'voiced', char, char)
   
    for char in voiceless:
        f.add_arc('marker', 'voiceless', char, char)
    
    for char in alveolar:
        f.add_arc('marker', 'alveolar', char, char)

    # ending arcs
    f.add_arc('voiced', 'end', '#', 'd#')
    f.add_arc('voiceless', 'end', '#', 't#')
    f.add_arc('alveolar', 'end', '#', 'ɪd#')

    return f

    # IRREGULAR

def participle_irreg():

    f_irreg = FST('participle_irreg')

    # initialize states
    f_irreg.add_state('start')
    f_irreg.add_state('marker')

    # ə state
    f_irreg.add_state('ə')
    
    # arise
    f_irreg.add_state('ɹ_ə')
    f_irreg.add_state('a_ər')
    f_irreg.add_state('ɪ_əra')
    f_irreg.add_state('z_əraɪ')

    # awake
    f_irreg.add_state('w_ə')
    f_irreg.add_state('e_əw')
    f_irreg.add_state('ɪ_əwe')
    f_irreg.add_state('k_əweɪ')

    # b state
    f_irreg.add_state('b')

    # bi state
    f_irreg.add_state('i_b')

    # bɛ state 
    f_irreg.add_state('ɛ_b')
                      
    # bear
    f_irreg.add_state('ɹ_bɛ')

    # beat
    f_irreg.add_state('t_bi')

    # bɪ state
    f_irreg.add_state('ɪ_b')
    
    # become    
    f_irreg.add_state('k_bɪ')
    f_irreg.add_state('ʌ_bɪk')
    f_irreg.add_state('m_bɪkʌ')

    # begin
    f_irreg.add_state('g_bɪ')
    f_irreg.add_state('ɪ_bɪg')
    f_irreg.add_state('n_bɪgɪ')

    # bend
    f_irreg.add_state('n_bɛ')
    f_irreg.add_state('d_bɛn')

    # bet
    f_irreg.add_state('t_bɛ')

    # ba state
    f_irreg.add_state('a_b')

    # baɪ state
    f_irreg.add_state('ɪ_ba')

    # bind
    f_irreg.add_state('n_baɪ')
    f_irreg.add_state('d_baɪn')

    # bite
    f_irreg.add_state('t_baɪ')
    
    # bl state
    f_irreg.add_state('l_b')  

    # bleed 
    f_irreg.add_state('i_bl')     
    f_irreg.add_state('d_bli')

    # blow
    f_irreg.add_state('o_bl')
    f_irreg.add_state('ʊ_blo') 
    
    # bɹ state
    f_irreg.add_state('ɹ_b')

    # break
    f_irreg.add_state('e_bɹ')
    f_irreg.add_state('ɪ_bɹe')
    f_irreg.add_state('k_bɹeɪ')

    # bring 
    f_irreg.add_state('ɪ_bɹ')
    f_irreg.add_state('ŋ_bɹɪ')

    # build
    f_irreg.add_state('l_bɪ')
    f_irreg.add_state('d_bɪl')

    # burst
    f_irreg.add_state('ɝ_b')
    f_irreg.add_state('s_bɝ')
    f_irreg.add_state('t_bɝs')

    # k state
    f_irreg.add_state('k')

    # catch
    f_irreg.add_state('æ_k')
    f_irreg.add_state('ʧ_kæ')

    # kʌ STATE
    f_irreg.add_state('ʌ_k')

    # come
    f_irreg.add_state('m_kʌ')

    # cost
    f_irreg.add_state('ɔ_k')
    f_irreg.add_state('s_kɔ')
    f_irreg.add_state('t_kɔs')

    # choose
    f_irreg.add_state('ʧ')
    f_irreg.add_state('u_ʧ')
    f_irreg.add_state('z_ʧu')

    # creep 
    f_irreg.add_state('ɹ_k')
    f_irreg.add_state('i_kɹ')
    f_irreg.add_state('p_kɹi')

    # cut
    f_irreg.add_state('t_kʌ')

    # d state
    f_irreg.add_state('d')

    # deal
    f_irreg.add_state('i_d')
    f_irreg.add_state('l_di')

    # dig
    f_irreg.add_state('ɪ_d')
    f_irreg.add_state('g_dɪ')

    # dive 
    f_irreg.add_state('a_d')
    f_irreg.add_state('ɪ_da')
    f_irreg.add_state('v_daɪ')

    # do 
    f_irreg.add_state('u_d')

    # dɹ state
    f_irreg.add_state('ɹ_d')

    # draw
    f_irreg.add_state('ɔ_dɹ')

    # dream
    f_irreg.add_state('i_dɹ')
    f_irreg.add_state('m_dɹi')

    # drink
    f_irreg.add_state('ɪ_dɹ')
    f_irreg.add_state('ŋ_dɹɪ')
    f_irreg.add_state('k_dɹɪŋ')

    # drive
    f_irreg.add_state('a_dɹ')
    f_irreg.add_state('ɪ_dɹa')
    f_irreg.add_state('v_dɹaɪ')

    # eat
    f_irreg.add_state('i')
    f_irreg.add_state('t_i')

    # f state
    f_irreg.add_state('f')

    # fall
    f_irreg.add_state('ɔ_f')
    f_irreg.add_state('l_fɔ')

    # fi state
    f_irreg.add_state('i_f')

    # feed
    f_irreg.add_state('d_fi')

    # feel
    f_irreg.add_state('l_fi')

    # fa state
    f_irreg.add_state('a_f')

    # faɪ state
    f_irreg.add_state('ɪ_fa')

    # fight
    f_irreg.add_state('t_faɪ')

    # find
    f_irreg.add_state('n_faɪ')
    f_irreg.add_state('d_faɪn')

    # fit
    f_irreg.add_state('ɪ_f')
    f_irreg.add_state('t_fɪ')
    
    # fl state
    f_irreg.add_state('l_f')

    # fli state
    f_irreg.add_state('i_fl')

    # fling
    f_irreg.add_state('ɪ_fl')
    f_irreg.add_state('ŋ_flɪ')

    # fly 
    f_irreg.add_state('a_fl')
    f_irreg.add_state('ɪ_fla')

     # fə state
    f_irreg.add_state('ə_f')

    # fəɹ state
    f_irreg.add_state('ɹ_fə')

    # fəɹg
    f_irreg.add_state('g_fəɹ')

    # forbid
    f_irreg.add_state('b_fəɹ')
    f_irreg.add_state('ɪ_fəɹb')
    f_irreg.add_state('d_fəɹbɪ')

    # forget
    f_irreg.add_state('ɛ_fəɹg')
    f_irreg.add_state('t_fəɹgɛ')

    # forgive
    f_irreg.add_state('ɪ_fəɹg')
    f_irreg.add_state('v_fəɹgɪ')
    
    # freeze
    f_irreg.add_state('ɹ_f')       
    f_irreg.add_state('i_fɹ')
    f_irreg.add_state('z_fɹi')

    # g state
    f_irreg.add_state('g')

    # get
    f_irreg.add_state('ɛ_g')
    f_irreg.add_state('t_gɛ')

    # give
    f_irreg.add_state('ɪ_g')
    f_irreg.add_state('v_gɪ')

    # go
    f_irreg.add_state('o_g')
    f_irreg.add_state('ʊ_go')

    # grow
    f_irreg.add_state('ɹ_g')
    f_irreg.add_state('o_gɹ')
    f_irreg.add_state('ʊ_gɹo')

    # h state
    f_irreg.add_state('h')

    # hæ
    f_irreg.add_state('æ_h')

    # hang
    f_irreg.add_state('ŋ_hæ')

    # have
    f_irreg.add_state('v_hæ')

    # hɪ state
    f_irreg.add_state('ɪ_h')

    # hear
    f_irreg.add_state('ɹ_hɪ')

    # hide
    f_irreg.add_state('a_h')
    f_irreg.add_state('ɪ_ha')
    f_irreg.add_state('d_haɪ')

    # hit
    f_irreg.add_state('t_hɪ')

    # hold
    f_irreg.add_state('o_h')
    f_irreg.add_state('ʊ_ho')
    f_irreg.add_state('l_hoʊ')
    f_irreg.add_state('d_hoʊl')

    # hurt
    f_irreg.add_state('ɜ_h')
    f_irreg.add_state('ɹ_hɜ')
    f_irreg.add_state('t_hɜɹ')

    # keep
    f_irreg.add_state('i_k')
    f_irreg.add_state('p_ki')

    # n (kn) state
    f_irreg.add_state('n')

    # kneel
    f_irreg.add_state('i_n')
    f_irreg.add_state('l_ni')

    # knit
    f_irreg.add_state('ɪ_n')
    f_irreg.add_state('t_nɪ')

    # know
    f_irreg.add_state('o_n')
    f_irreg.add_state('ʊ_no')

    # l state
    f_irreg.add_state('l')

    # lay
    f_irreg.add_state('e_l')
    f_irreg.add_state('ɪ_le')

    # li state
    f_irreg.add_state('i_l')

    # lead
    f_irreg.add_state('d_li')

    # leave
    f_irreg.add_state('v_li')

    # lɛ state
    f_irreg.add_state('ɛ_l')

    # lend
    f_irreg.add_state('n_lɛ')
    f_irreg.add_state('d_lɛn')

    # let
    f_irreg.add_state('t_lɛ')

    # la state
    f_irreg.add_state('a_l')

    # lai state
    f_irreg.add_state('ɪ_la')

    # light
    f_irreg.add_state('t_laɪ')

    # lose
    f_irreg.add_state('u_l')
    f_irreg.add_state('z_lu')

    # m state
    f_irreg.add_state('m')

    # make
    f_irreg.add_state('e_m')
    f_irreg.add_state('ɪ_me')
    f_irreg.add_state('k_meɪ')

    # i_m
    f_irreg.add_state('i_m')

    # mean
    f_irreg.add_state('n_mi')

    # meet
    f_irreg.add_state('t_mi')

    # p state
    f_irreg.add_state('p')

    # pay
    f_irreg.add_state('e_p')
    f_irreg.add_state('ɪ_pe')

    # plead
    f_irreg.add_state('l_p')
    f_irreg.add_state('i_pl')
    f_irreg.add_state('d_pli')

    # prove
    f_irreg.add_state('ɹ_p')
    f_irreg.add_state('u_pɹ')
    f_irreg.add_state('v_pɹu')

    # put
    f_irreg.add_state('ʊ_p')
    f_irreg.add_state('t_pʊ')

    # quit
    f_irreg.add_state('w_k')
    f_irreg.add_state('ɪ_kw')
    f_irreg.add_state('t_kwɪ')

    # ɹ state
    f_irreg.add_state('ɹ')

    # read
    f_irreg.add_state('i_ɹ')
    f_irreg.add_state('d_ɹi')

    # ɹa state
    f_irreg.add_state('a_ɹ')

    # ɹaɪ state
    f_irreg.add_state('ɪ_ɹa')

    # ride
    f_irreg.add_state('d_ɹaɪ')

    # ring
    f_irreg.add_state('ɪ_ɹ')
    f_irreg.add_state('ŋ_ɹɪ')

    # rise
    f_irreg.add_state('z_ɹaɪ')

    # run
    f_irreg.add_state('ʌ_ɹ')
    f_irreg.add_state('n_ɹʌ')

    # s arc
    f_irreg.add_state('s')
    
    # say
    f_irreg.add_state('e_s')
    f_irreg.add_state('ɪ_se')

    # si state 
    f_irreg.add_state('i_s')

    # seek
    f_irreg.add_state('k_si')

    # sɛ
    f_irreg.add_state('ɛ_s')

    # sell
    f_irreg.add_state('l_sɛ')

    #send
    f_irreg.add_state('n_sɛ')
    f_irreg.add_state('d_sɛn')

    # set
    f_irreg.add_state('t_sɛ')

    # sew
    f_irreg.add_state('o_s')
    f_irreg.add_state('ʊ_so')

    # ʃ state
    f_irreg.add_state('ʃ')

    # shake
    f_irreg.add_state('e_ʃ')
    f_irreg.add_state('ɪ_ʃe')
    f_irreg.add_state('k_ʃeɪ')

    # shine
    f_irreg.add_state('a_ʃ')
    f_irreg.add_state('ɪ_ʃa')
    f_irreg.add_state('n_ʃaɪ')

    # shoot
    f_irreg.add_state('u_ʃ')
    f_irreg.add_state('t_ʃu')

    # shrink
    f_irreg.add_state('ɹ_ʃ')
    f_irreg.add_state('ɪ_ʃɹ')
    f_irreg.add_state('ŋ_ʃɹɪ')
    f_irreg.add_state('k_ʃɹɪŋ')

    # shut
    f_irreg.add_state('ʌ_ʃ')
    f_irreg.add_state('t_ʃʌ')

    # sɪ
    f_irreg.add_state('ɪ_s')

    # sɪŋ
    f_irreg.add_state('ŋ_sɪ')

    # sink
    f_irreg.add_state('k_sɪŋ')

    # sit
    f_irreg.add_state('t_sɪ')

    # sl state
    f_irreg.add_state('l_s')

    # slay
    f_irreg.add_state('e_sl')
    f_irreg.add_state('ɪ_sle')

    # sleep
    f_irreg.add_state('i_sl')
    f_irreg.add_state('p_sli')

    # slide
    f_irreg.add_state('a_sl')
    f_irreg.add_state('ɪ_sla')
    f_irreg.add_state('d_slaɪ')

    # slit
    f_irreg.add_state('ɪ_sl')
    f_irreg.add_state('t_slɪ')

    # sp state
    f_irreg.add_state('p_s')

    # speak
    f_irreg.add_state('i_sp')
    f_irreg.add_state('k_spi')

    # spend
    f_irreg.add_state('ɛ_sp')
    f_irreg.add_state('n_spɛ')
    f_irreg.add_state('d_spɛn')

    # spɪ state
    f_irreg.add_state('ɪ_sp')

    # spin
    f_irreg.add_state('n_spɪ')

    # spit 
    f_irreg.add_state('t_spɪ')

    # spl state
    f_irreg.add_state('l_sp')

    # split
    f_irreg.add_state('ɪ_spl')
    f_irreg.add_state('t_splɪ')

    # spɹ state
    f_irreg.add_state('ɹ_sp')

    # spread
    f_irreg.add_state('ɛ_spɹ')
    f_irreg.add_state('d_spɹɛ')

    # spring
    f_irreg.add_state('ɪ_spɹ')
    f_irreg.add_state('ŋ_spɹɪ')

    # st state
    f_irreg.add_state('t_s')

    # stand
    f_irreg.add_state('æ_st')
    f_irreg.add_state('n_stæ')
    f_irreg.add_state('d_stæn')

    # steal 
    f_irreg.add_state('i_st')
    f_irreg.add_state('l_sti')

    # stɪ state
    f_irreg.add_state('ɪ_st')

    # stick
    f_irreg.add_state('k_stɪ')

    # stɪŋ state
    f_irreg.add_state('ŋ_stɪ')

    # stink
    f_irreg.add_state('k_stɪŋ')

    # str state
    f_irreg.add_state('ɹ_st')

    # stɹa state
    f_irreg.add_state('a_stɹ')

    # stɹaɪ state
    f_irreg.add_state('ɪ_stɹa')

    # stride
    f_irreg.add_state('d_stɹaɪ')

    # strike
    f_irreg.add_state('k_stɹaɪ')

    # string
    f_irreg.add_state('ɪ_stɹ')
    f_irreg.add_state('ŋ_stɹɪ')

    # sw state
    f_irreg.add_state('w_s')

    # swɛ state
    f_irreg.add_state('ɛ_sw')

    # swear
    f_irreg.add_state('ɹ_swɛ')

    # sweep
    f_irreg.add_state('i_sw')
    f_irreg.add_state('p_swi')

    # swell
    f_irreg.add_state('l_swɛ')
    
    # swɪ state
    f_irreg.add_state('ɪ_sw')

    # swim
    f_irreg.add_state('m_swɪ')

    # swing
    f_irreg.add_state('ŋ_swɪ')

    # t state
    f_irreg.add_state('t')

    # take 
    f_irreg.add_state('e_t')
    f_irreg.add_state('ɪ_te')
    f_irreg.add_state('k_teɪ')

    # teach
    f_irreg.add_state('i_t')
    f_irreg.add_state('t_ti')
    f_irreg.add_state('ʃ_tit')

    # tɛ state
    f_irreg.add_state('ɛ_t')

    # tear
    f_irreg.add_state('ɹ_tɛ')

    # tell
    f_irreg.add_state('l_tɛ')

    # θ state
    f_irreg.add_state('θ')

    # think
    f_irreg.add_state('ɪ_θ')
    f_irreg.add_state('ŋ_θɪ')
    f_irreg.add_state('k_θɪŋ')

    # throw
    f_irreg.add_state('ɹ_θ')
    f_irreg.add_state('o_θɹ')
    f_irreg.add_state('ʊ_θɹo')

    # understand
    f_irreg.add_state('ʌ')
    f_irreg.add_state('n_ʌ')
    f_irreg.add_state('d_ʌn')
    f_irreg.add_state('ə_ʌnd')
    f_irreg.add_state('ɹ_ʌndə')
    f_irreg.add_state('s_ʌndəɹ')
    f_irreg.add_state('t_ʌndəɹs')
    f_irreg.add_state('æ_ʌndəɹst')
    f_irreg.add_state('n_ʌndəɹstæ')
    f_irreg.add_state('d_ʌndəɹstæn')
    
    # w state
    f_irreg.add_state('w')

    # we state 
    f_irreg.add_state('e_w')

    # wake 
    f_irreg.add_state('ɪ_we')
    f_irreg.add_state('k_weɪ')

    # wɛ state
    f_irreg.add_state('ɛ_w')

    # wear
    f_irreg.add_state('ɹ_wɛ')

    # wed
    f_irreg.add_state('d_wɛ')

    # weep
    f_irreg.add_state('i_w')
    f_irreg.add_state('p_wi')

    # wet
    f_irreg.add_state('t_wɛ')

    # win 
    f_irreg.add_state('ɪ_w')
    f_irreg.add_state('n_wɪ')

    # wring
    f_irreg.add_state('ɹ_w')
    f_irreg.add_state('ɪ_ɹ_w')
    f_irreg.add_state('ŋ_ɹɪ_w')
    f_irreg.add_state('__ɹɪŋ_w')
    f_irreg.add_state('w__ɹɪŋ_w')

    # write
    f_irreg.add_state('t_ɹaɪ')

    f_irreg.add_state('end')

    f_irreg.initial_state = 'start'
    f_irreg.set_final('end')

    # ADD ARCS
    f_irreg.add_arc('start', 'marker', '#', ['#'])
    
    # ə arc 
    f_irreg.add_arc('marker', 'ə', 'ə', [])

    # arise = arisen
    f_irreg.add_arc('ə', 'ɹ_ə', 'ɹ', [])
    f_irreg.add_arc('ɹ_ə', 'a_ər', 'a', [])
    f_irreg.add_arc('a_ər', 'ɪ_əra', 'ɪ', [])
    f_irreg.add_arc('ɪ_əra', 'z_əraɪ', 'z', [])
    f_irreg.add_arc('z_əraɪ', 'end', '#', ['ə', 'ɹ', 'ɪ', 'z', 'ə', 'n', '#'])

    # awake = awoken
    f_irreg.add_arc('ə', 'w_ə', 'w', [])
    f_irreg.add_arc('w_ə', 'e_əw', 'e', [])
    f_irreg.add_arc('e_əw', 'ɪ_əwe', 'ɪ', [])
    f_irreg.add_arc('ɪ_əwe', 'k_əweɪ', 'k', [])
    f_irreg.add_arc('k_əweɪ', 'end', '#', ['ə', 'w', 'o', 'ʊ', 'k', 'ə', 'n', '#'])

    # b arc
    f_irreg.add_arc('marker', 'b', 'b', [])

    # bi arc
    f_irreg.add_arc('b', 'i_b', 'i', [])

    # bɪ arc
    f_irreg.add_arc('b', 'ɪ_b', 'ɪ', [])

    # bɛ arc
    f_irreg.add_arc('b', 'ɛ_b', 'ɛ', [])

    # ba arc
    f_irreg.add_arc('b', 'a_b', 'a', [])

    # baɪ arc
    f_irreg.add_arc('a_b', 'ɪ_ba', 'ɪ', [])

    # be = been
    f_irreg.add_arc('i_b', 'end', '#', ['b', 'ɪ', 'n', '#'])

    # bear = borne
    f_irreg.add_arc('ɛ_b', 'ɹ_bɛ', 'ɹ', [])
    f_irreg.add_arc('ɹ_bɛ', 'end', '#', ['b', 'ɔ', 'ɹ', 'n', '#'])

    # beat = beaten
    f_irreg.add_arc('i_b', 't_bi', 't', [])
    f_irreg.add_arc('t_bi', 'end', '#', ['b', 'i', 't', 'ə', 'n', '#'])

    # become = become
    f_irreg.add_arc('ɪ_b', 'k_bɪ', 'k', [])
    f_irreg.add_arc('k_bɪ', 'ʌ_bɪk', 'ʌ', [])
    f_irreg.add_arc('ʌ_bɪk', 'm_bɪkʌ', 'm', [])
    f_irreg.add_arc('m_bɪkʌ', 'end', '#', ['b', 'ɪ', 'k', 'ʌ', 'm', '#'])

    # begin = begun
    f_irreg.add_arc('ɪ_b', 'g_bɪ', 'g', [])
    f_irreg.add_arc('g_bɪ', 'ɪ_bɪg', 'ɪ', [])
    f_irreg.add_arc('ɪ_bɪg', 'n_bɪgɪ', 'n', [])
    f_irreg.add_arc('n_bɪgɪ', 'end', '#', ['b', 'ɪ', 'g', 'ʌ', 'n', '#'])

    # bend = bent
    f_irreg.add_arc('ɛ_b', 'n_bɛ', 'n', [])
    f_irreg.add_arc('n_bɛ', 'd_bɛn', 'd', [])
    f_irreg.add_arc('d_bɛn', 'end', '#', ['b', 'ɛ', 'n', 't', '#'])

    # bet = bet
    f_irreg.add_arc('ɛ_b', 't_bɛ', 't', [])
    f_irreg.add_arc('t_bɛ', 'end', '#', ['b', 'ɛ', 't', '#'])
    
    # bind = bound
    f_irreg.add_arc('ɪ_ba', 'n_baɪ', 'n', [])
    f_irreg.add_arc('n_baɪ', 'd_baɪn', 'd', [])
    f_irreg.add_arc('d_baɪn', 'end', '#', ['b', 'a', 'ʊ', 'n', 'd', '#'])

    # bite = bitten
    f_irreg.add_arc('ɪ_ba', 't_baɪ', 't', [])
    f_irreg.add_arc('t_baɪ', 'end', '#', ['b', 'ɪ', 't', 'ə', 'n', '#'])

    # bl arc
    f_irreg.add_arc('b', 'l_b', 'l', [])

    # bleed = bled
    f_irreg.add_arc('l_b', 'i_bl', 'i', [])
    f_irreg.add_arc('i_bl', 'd_bli', 'd', [])
    f_irreg.add_arc('d_bli', 'end', '#', ['b', 'l', 'ɛ', 'd', '#'])


    # blow = blown
    f_irreg.add_arc('l_b', 'o_bl', 'o', [])
    f_irreg.add_arc('o_bl', 'ʊ_blo', 'ʊ', [])
    f_irreg.add_arc('ʊ_blo', 'end', '#', ['b', 'l', 'o', 'ʊ', 'n', '#'])

    # bɹ arc
    f_irreg.add_arc('b', 'ɹ_b', 'ɹ', [])

    # break = broken
    f_irreg.add_arc('ɹ_b', 'e_bɹ', 'e', [])
    f_irreg.add_arc('e_bɹ', 'ɪ_bɹe', 'ɪ', [])  
    f_irreg.add_arc('ɪ_bɹe', 'k_bɹeɪ', 'k', [])
    f_irreg.add_arc('k_bɹeɪ', 'end', '#', ['b', 'ɹ', 'o', 'ʊ', 'k', 'ə', 'n', '#'])

    # bring = brought
    f_irreg.add_arc('ɹ_b', 'ɪ_bɹ', 'ɪ', [])
    f_irreg.add_arc('ɪ_bɹ', 'ŋ_bɹɪ', 'ŋ', [])
    f_irreg.add_arc('ŋ_bɹɪ', 'end', '#', ['b', 'ɹ', 'ɔ', 't', '#'])

    # build = built
    f_irreg.add_arc('ɪ_b', 'l_bɪ', 'l', [])
    f_irreg.add_arc('l_bɪ', 'd_bɪl', 'd', [])
    f_irreg.add_arc('d_bɪl', 'end', '#', ['b', 'ɪ', 'l', 't', '#'])

    # burst = burst
    f_irreg.add_arc('b', 'ɝ_b', 'ɝ', [])
    f_irreg.add_arc('ɝ_b', 's_bɝ', 's', [])
    f_irreg.add_arc('s_bɝ', 't_bɝs', 't', [])
    f_irreg.add_arc('t_bɝs', 'end', '#', ['b', 'ɝ', 's', 't', '#'])

    # buy = bought
    f_irreg.add_arc('ɪ_ba', 'end', '#', ['b', 'ɔ', 't', '#'])

    # k arc
    f_irreg.add_arc('marker', 'k', 'k', [])

    # ʧ arc 
    f_irreg.add_arc('marker', 'ʧ', 'ʧ', [])

    # catch = caught
    f_irreg.add_arc('k', 'æ_k', 'æ', [])
    f_irreg.add_arc('æ_k', 'ʧ_kæ', 'ʧ', [])
    f_irreg.add_arc('ʧ_kæ', 'end', '#', ['k', 'ɔ', 't', '#'])

    # choose = chosen
    f_irreg.add_arc('ʧ', 'u_ʧ', 'u', [])
    f_irreg.add_arc('u_ʧ', 'z_ʧu', 'z', [])
    f_irreg.add_arc('z_ʧu', 'end', '#', ['ʧ', 'o', 'ʊ', 'z', 'ə', 'n', '#'])

    # kʌ arc
    f_irreg.add_arc('k', 'ʌ_k', 'ʌ', [])

    # come = come
    f_irreg.add_arc('ʌ_k', 'm_kʌ', 'm', [])
    f_irreg.add_arc('m_kʌ', 'end', '#', ['k', 'ʌ', 'm', '#'])
    
    # cost
    f_irreg.add_arc('k', 'ɔ_k', 'ɔ', [])
    f_irreg.add_arc('ɔ_k', 's_kɔ', 's', [])
    f_irreg.add_arc('s_kɔ', 't_kɔs', 't', [])
    f_irreg.add_arc('t_kɔs', 'end', '#', ['k', 'ɔ', 's', 't', '#'])

    # creep = crept
    f_irreg.add_arc('k', 'ɹ_k', 'ɹ', [])
    f_irreg.add_arc('ɹ_k', 'i_kɹ', 'i', [])
    f_irreg.add_arc('i_kɹ', 'p_kɹi', 'p', [])
    f_irreg.add_arc('p_kɹi', 'end', '#', ['k', 'ɹ', 'ɛ', 'p', 't', '#'])

    # cut = cut
    f_irreg.add_arc('ʌ_k', 't_kʌ', 't', [])
    f_irreg.add_arc('t_kʌ', 'end', '#', ['k', 'ʌ', 't', '#'])

    # d arc
    f_irreg.add_arc('marker', 'd', 'd', [])

    # deal = dealt
    f_irreg.add_arc('d', 'i_d', 'i', [])
    f_irreg.add_arc('i_d', 'l_di', 'l', [])
    f_irreg.add_arc('l_di', 'end', '#', ['d', 'ɛ', 'l', 't', '#'])

    # dig = dug
    f_irreg.add_arc('d', 'ɪ_d', 'ɪ', [])
    f_irreg.add_arc('ɪ_d', 'g_dɪ', 'g', [])
    f_irreg.add_arc('g_dɪ', 'end', '#', ['d', 'ʌ', 'g', '#'])

    # dive = dove
    f_irreg.add_arc('d', 'a_d', 'a', [])
    f_irreg.add_arc('a_d', 'ɪ_da', 'ɪ', [])
    f_irreg.add_arc('ɪ_da', 'v_daɪ', 'v', [])
    f_irreg.add_arc('v_daɪ', 'end', '#', ['d', 'o', 'ʊ', 'v', '#'])
    
    # do = done
    f_irreg.add_arc('d', 'u_d', 'u', [])
    f_irreg.add_arc('u_d', 'end', '#', ['d', 'ʌ', 'n', '#'])

    # dɹ arc
    f_irreg.add_arc('d', 'ɹ_d', 'ɹ', [])

    # draw = drawn
    f_irreg.add_arc('ɹ_d', 'ɔ_dɹ', 'ɔ', [])
    f_irreg.add_arc('ɔ_dɹ', 'end', '#', ['d', 'ɹ', 'ɔ', 'n', '#'])

    # dream = dreamt
    f_irreg.add_arc('ɹ_d', 'i_dɹ', 'i', [])
    f_irreg.add_arc('i_dɹ', 'm_dɹi', 'm', [])
    f_irreg.add_arc('m_dɹi', 'end', '#', ['d', 'ɹ', 'ɛ', 'm', 't', '#'])

    # drink = drunk
    f_irreg.add_arc('ɹ_d', 'ɪ_dɹ', 'ɪ', [])
    f_irreg.add_arc('ɪ_dɹ', 'ŋ_dɹɪ', 'ŋ', [])
    f_irreg.add_arc('ŋ_dɹɪ', 'k_dɹɪŋ', 'k', [])
    f_irreg.add_arc('k_dɹɪŋ', 'end', '#', ['d', 'ɹ', 'ʌ', 'ŋ', 'k', '#'])

    # drive = driven
    f_irreg.add_arc('ɹ_d', 'a_dɹ', 'a', [])
    f_irreg.add_arc('a_dɹ', 'ɪ_dɹa', 'ɪ', [])
    f_irreg.add_arc('ɪ_dɹa', 'v_dɹaɪ', 'v', [])
    f_irreg.add_arc('v_dɹaɪ', 'end', '#', ['d', 'ɹ', 'ɪ', 'v', 'ə', 'n', '#'])

    # eat = eaten
    f_irreg.add_arc('marker', 'i', 'i', [])
    f_irreg.add_arc('i', 't_i', 't', [])
    f_irreg.add_arc('t_i', 'end', '#', ['i', 't', 'ə', 'n', '#'])

    # f arc
    f_irreg.add_arc('marker', 'f', 'f', [])

    # fall = fallen
    f_irreg.add_arc('f', 'ɔ_f', 'ɔ', [])
    f_irreg.add_arc('ɔ_f', 'l_fɔ', 'l', [])
    f_irreg.add_arc('l_fɔ', 'end', '#', ['f', 'ɔ', 'l', 'ə', 'n','#'])

    # fi arc
    f_irreg.add_arc('f', 'i_f', 'i', [])

    # feed = fed
    f_irreg.add_arc('i_f', 'd_fi', 'd', [])
    f_irreg.add_arc('d_fi', 'end', '#', ['f', 'ɛ', 'd', '#'])

    # feel = felt
    f_irreg.add_arc('i_f', 'l_fi', 'l', [])
    f_irreg.add_arc('l_fi', 'end', '#', ['f', 'ɛ', 'l', 't', '#'])

    # fa arc
    f_irreg.add_arc('f', 'a_f', 'a', [])

    # faɪ arc
    f_irreg.add_arc('a_f', 'ɪ_fa', 'ɪ', [])

    # fight = fought
    f_irreg.add_arc('ɪ_fa', 't_faɪ', 't', [])
    f_irreg.add_arc('t_faɪ', 'end', '#', ['f', 'ɔ', 't', '#'])

    # find = found
    f_irreg.add_arc('ɪ_fa', 'n_faɪ', 'n', [])
    f_irreg.add_arc('n_faɪ', 'd_faɪn', 'd', [])
    f_irreg.add_arc('d_faɪn', 'end', '#', ['f', 'a', 'ʊ', 'n', 'd', '#'])

    # fit = fitted
    f_irreg.add_arc('f', 'ɪ_f', 'ɪ', [])
    f_irreg.add_arc('ɪ_f', 't_fɪ', 't', [])
    f_irreg.add_arc('t_fɪ', 'end', '#', ['f', 'ɪ', 't', '#'])


    # fl arc
    f_irreg.add_arc('f', 'l_f', 'l', [])

    # fli arc
    f_irreg.add_arc('l_f', 'i_fl', 'i', [])

    # flee = fled
    f_irreg.add_arc('i_fl', 'end', '#', ['f', 'l', 'ɛ', 'd', '#'])

    # fling = flung
    f_irreg.add_arc('l_f', 'ɪ_fl', 'ɪ', [])
    f_irreg.add_arc('ɪ_fl', 'ŋ_flɪ', 'ŋ', [])
    f_irreg.add_arc('ŋ_flɪ', 'end', '#', ['f', 'l', 'ʌ', 'ŋ', '#'])
    
    # fly = flown
    f_irreg.add_arc('l_f', 'a_fl', 'a', [])
    f_irreg.add_arc('a_fl', 'ɪ_fla', 'ɪ', [])
    f_irreg.add_arc('ɪ_fla', 'end', '#', ['f', 'l', 'o', 'ʊ', 'n', '#'])

    # fə arc
    f_irreg.add_arc('f', 'ə_f', 'ə', [])

    # fəɹ arc
    f_irreg.add_arc('ə_f', 'ɹ_fə', 'ɹ', [])

    # fəɹg arc
    f_irreg.add_arc('ɹ_fə', 'g_fəɹ', 'g', [])

    # forbid = forbidden
    f_irreg.add_arc('ɹ_fə', 'b_fəɹ', 'b', [])
    f_irreg.add_arc('b_fəɹ', 'ɪ_fəɹb', 'ɪ', [])
    f_irreg.add_arc('ɪ_fəɹb', 'd_fəɹbɪ', 'd', [])
    f_irreg.add_arc('d_fəɹbɪ', 'end', '#', ['f', 'ə', 'ɹ', 'b', 'ɪ', 'd', 'ə', 'n', '#'])

    # forget = forgotten
    f_irreg.add_arc('g_fəɹ', 'ɛ_fəɹg', 'ɛ', [])
    f_irreg.add_arc('ɛ_fəɹg', 't_fəɹgɛ', 't', [])
    f_irreg.add_arc('t_fəɹgɛ', 'end', '#', ['f', 'ə', 'ɹ', 'g', 'ɑ', 't', 'ə', 'n', '#'])

    # forgive = forgiven
    f_irreg.add_arc('g_fəɹ', 'ɪ_fəɹg', 'ɪ', [])
    f_irreg.add_arc('ɪ_fəɹg', 'v_fəɹgɪ', 'v', [])
    f_irreg.add_arc('v_fəɹgɪ', 'end', '#', ['f', 'ə', 'ɹ', 'g', 'ɪ', 'v', 'ə', 'n','#'])

    # freeze = frozen
    f_irreg.add_arc('f', 'ɹ_f', 'ɹ', [])
    f_irreg.add_arc('ɹ_f', 'i_fɹ', 'i', [])
    f_irreg.add_arc('i_fɹ', 'z_fɹi', 'z', [])
    f_irreg.add_arc('z_fɹi', 'end', '#', ['f', 'ɹ', 'o', 'ʊ', 'z', 'ə', 'n', '#'])

    # g arc
    f_irreg.add_arc('marker', 'g', 'g', [])

    # get = gotten
    f_irreg.add_arc('g', 'ɛ_g', 'ɛ', [])
    f_irreg.add_arc('ɛ_g', 't_gɛ', 't', [])
    f_irreg.add_arc('t_gɛ', 'end', '#', ['g', 'ɑ', 't', 'n', '#'])

    # give = given
    f_irreg.add_arc('g', 'ɪ_g', 'ɪ', [])
    f_irreg.add_arc('ɪ_g', 'v_gɪ', 'v', [])
    f_irreg.add_arc('v_gɪ', 'end', '#', ['g', 'ɪ', 'v', 'ə','n','#'])

    # go = gone
    f_irreg.add_arc('g', 'o_g', 'o', [])
    f_irreg.add_arc('o_g', 'ʊ_go', 'ʊ', [])
    f_irreg.add_arc('ʊ_go', 'end', '#', ['g', 'ɑ', 'n', '#'])

    # grow = grown
    f_irreg.add_arc('g', 'ɹ_g', 'ɹ', [])
    f_irreg.add_arc('ɹ_g', 'o_gɹ', 'o', [])
    f_irreg.add_arc('o_gɹ', 'ʊ_gɹo', 'ʊ', [])
    f_irreg.add_arc('ʊ_gɹo', 'end', '#', ['g', 'ɹ', 'o', 'ʊ', 'n', '#'])

    # h arc
    f_irreg.add_arc('marker', 'h', 'h', [])

    # hæ arc
    f_irreg.add_arc('h', 'æ_h', 'æ', [])

    # hang = hung
    f_irreg.add_arc('æ_h', 'ŋ_hæ', 'ŋ', [])
    f_irreg.add_arc('ŋ_hæ', 'end', '#', ['h', 'ʌ', 'ŋ', '#'])

    # have = had
    f_irreg.add_arc('æ_h', 'v_hæ', 'v', [])
    f_irreg.add_arc('v_hæ', 'end', '#', ['h', 'æ', 'd', '#'])

    # hɪ arc
    f_irreg.add_arc('h', 'ɪ_h', 'ɪ', [])

    # hear = heard
    f_irreg.add_arc('ɪ_h', 'ɹ_hɪ', 'ɹ', [])
    f_irreg.add_arc('ɹ_hɪ', 'end', '#', ['h', 'ɜ', 'ɹ', 'd', '#'])

    # hide = hidden
    f_irreg.add_arc('h', 'a_h', 'a', [])
    f_irreg.add_arc('a_h', 'ɪ_ha', 'ɪ', [])
    f_irreg.add_arc('ɪ_ha', 'd_haɪ', 'd', [])
    f_irreg.add_arc('d_haɪ', 'end', '#', ['h', 'ɪ', 'd', 'ə', 'n', '#'])

    # hit = hit
    f_irreg.add_arc('ɪ_h', 't_hɪ', 't', [])
    f_irreg.add_arc('t_hɪ', 'end', '#', ['h', 'ɪ', 't', '#'])

    # hold = held
    f_irreg.add_arc('h', 'o_h', 'o', [])
    f_irreg.add_arc('o_h', 'ʊ_ho', 'ʊ', [])
    f_irreg.add_arc('ʊ_ho', 'l_hoʊ', 'l', [])
    f_irreg.add_arc('l_hoʊ', 'd_hoʊl', 'd', [])
    f_irreg.add_arc('d_hoʊl', 'end', '#', ['h', 'ɛ', 'l', 'd', '#'])

    # hurt = hurt
    f_irreg.add_arc('h', 'ɜ_h', 'ɜ', [])
    f_irreg.add_arc('ɜ_h', 'ɹ_hɜ', 'ɹ', [])
    f_irreg.add_arc('ɹ_hɜ', 't_hɜɹ', 't', [])
    f_irreg.add_arc('t_hɜɹ', 'end', '#', ['h', 'ɜ', 'ɹ', 't', '#'])

    # k arc
    f_irreg.add_arc('marker', 'k', 'k', [])

    # keep = kept
    f_irreg.add_arc('k', 'i_k', 'i', [])
    f_irreg.add_arc('i_k', 'p_ki', 'p', [])
    f_irreg.add_arc('p_ki', 'end', '#', ['k', 'ɛ', 'p', 't', '#'])

    # n (kn) arc
    f_irreg.add_arc('marker', 'n', 'n', [])

    '''
    # kneel = knelt
    f_irreg.add_arc('n', 'i_n', 'i', [])
    f_irreg.add_arc('i_n', 'l_ni', 'l', [])
    f_irreg.add_arc('l_ni', 'end', '#', ['n', 'ɛ', 'l', 't', '#'])
    '''
    
    '''
    # knit = knitted
    f_irreg.add_arc('n', 'ɪ_n', 'ɪ', [])
    f_irreg.add_arc('ɪ_n', 't_nɪ', 't', [])
    f_irreg.add_arc('t_nɪ', 'end', '#', ['n', 'ɪ', 't', 'ɪ', 'd', '#'])
    '''

    # know = known
    f_irreg.add_arc('n', 'o_n', 'o', [])
    f_irreg.add_arc('o_n', 'ʊ_no', 'ʊ', [])
    f_irreg.add_arc('ʊ_no', 'end', '#', ['n', 'o', 'ʊ', 'n', '#'])

    # l marker
    f_irreg.add_arc('marker', 'l', 'l', [])

    '''
    # lay = laid
    f_irreg.add_arc('l', 'e_l', 'e', [])
    f_irreg.add_arc('e_l', 'ɪ_le', 'ɪ', [])
    f_irreg.add_arc('ɪ_le', 'end', '#', ['l', 'e', 'ɪ', 'd', '#'])
    '''

    # li arc
    f_irreg.add_arc('l', 'i_l', 'i', [])

    # lead = led
    f_irreg.add_arc('i_l', 'd_li', 'd', [])
    f_irreg.add_arc('d_li', 'end', '#', ['l', 'ɛ', 'd', '#'])

    # leave = left
    f_irreg.add_arc('i_l', 'v_li', 'v', [])
    f_irreg.add_arc('v_li', 'end', '#', ['l', 'ɛ', 'f', 't', '#']) 

    # lɛ arc
    f_irreg.add_arc('l', 'ɛ_l', 'ɛ', [])
    
    # lend = lent
    f_irreg.add_arc('ɛ_l', 'n_lɛ', 'n', [])
    f_irreg.add_arc('n_lɛ', 'd_lɛn', 'd', [])
    f_irreg.add_arc('d_lɛn', 'end', '#', ['l', 'ɛ', 'n', 't', '#'])

    # let = let
    f_irreg.add_arc('ɛ_l', 't_lɛ', 't', [])
    f_irreg.add_arc('t_lɛ', 'end', '#', ['l', 'ɛ', 't', '#'])

    # la
    f_irreg.add_arc('l', 'a_l', 'a', [])
    
    # laɪ
    f_irreg.add_arc('a_l', 'ɪ_la', 'ɪ', [])

    '''
    lie = lied
    f_irreg.add_arc('ɪ_la', 'end', '#', ['l', 'a', 'ɪ', 'd', '#'])
    '''

    # light = lit
    f_irreg.add_arc('ɪ_la', 't_laɪ', 't', [])
    f_irreg.add_arc('t_laɪ', 'end', '#', ['l', 'ɪ', 't', '#'])

    # lose = lost
    f_irreg.add_arc('l', 'u_l', 'u', [])
    f_irreg.add_arc('u_l', 'z_lu', 'z', [])
    f_irreg.add_arc('z_lu', 'end', '#', ['l', 'ɔ', 's', 't', '#'])

    # m arc
    f_irreg.add_arc('marker', 'm', 'm', [])

    # make = made
    f_irreg.add_arc('m', 'e_m', 'e', [])
    f_irreg.add_arc('e_m', 'ɪ_me', 'ɪ', [])
    f_irreg.add_arc('ɪ_me', 'k_meɪ', 'k', [])
    f_irreg.add_arc('k_meɪ', 'end', '#', ['m', 'e', 'ɪ', 'd', '#'])

    # mi arc
    f_irreg.add_arc('m', 'i_m', 'i', [])

    # mean = meant
    f_irreg.add_arc('i_m', 'n_mi', 'n', [])
    f_irreg.add_arc('n_mi', 'end', '#', ['m', 'ɛ', 'n', 't', '#'])

    # meet = met
    f_irreg.add_arc('i_m', 't_mi', 't', [])
    f_irreg.add_arc('t_mi', 'end', '#', ['m', 'ɛ', 't', '#'])

    # p arc
    f_irreg.add_arc('marker', 'p', 'p', [])

    '''
    # pay = paid
    f_irreg.add_arc('p', 'e_p', 'e', [])
    f_irreg.add_arc('e_p', 'ɪ_pe', 'ɪ', [])
    f_irreg.add_arc('ɪ_pe', 'end', '#', ['p', 'e', 'ɪ', 'd', '#'])
    '''

    # plead = pled
    f_irreg.add_arc('p', 'l_p', 'l', [])
    f_irreg.add_arc('l_p', 'i_pl', 'i', [])
    f_irreg.add_arc('i_pl', 'd_pli', 'd', [])
    f_irreg.add_arc('d_pli', 'end', '#', ['p', 'l', 'ɛ', 'd', '#'])

    # prove = proven
    f_irreg.add_arc('p', 'ɹ_p', 'ɹ', [])
    f_irreg.add_arc('ɹ_p', 'u_pɹ', 'u', [])
    f_irreg.add_arc('u_pɹ', 'v_pɹu', 'v', [])
    f_irreg.add_arc('v_pɹu', 'end', '#', ['p', 'ɹ', 'u', 'v', 'ə', 'n', '#'])

    # put = put
    f_irreg.add_arc('p', 'ʊ_p', 'ʊ', [])
    f_irreg.add_arc('ʊ_p', 't_pʊ', 't', [])
    f_irreg.add_arc('t_pʊ', 'end', '#', ['p', 'ʊ', 't', '#'])

    # quit = quit
    f_irreg.add_arc('k', 'w_k', 'w', [])
    f_irreg.add_arc('w_k', 'ɪ_kw', 'ɪ', [])
    f_irreg.add_arc('ɪ_kw', 't_kwɪ', 't', [])
    f_irreg.add_arc('t_kwɪ', 'end', '#', ['k', 'w', 'ɪ', 't', '#'])

    # ɹ arc
    f_irreg.add_arc('marker', 'ɹ', 'ɹ', [])

    # read = read
    f_irreg.add_arc('ɹ', 'i_ɹ', 'i', [])
    f_irreg.add_arc('i_ɹ', 'd_ɹi', 'd', [])
    f_irreg.add_arc('d_ɹi', 'end', '#', ['ɹ', 'ɛ', 'd', '#'])

    # a_ɹ arc
    f_irreg.add_arc('ɹ', 'a_ɹ', 'a', [])

    # ɪ_ɹa arc
    f_irreg.add_arc('a_ɹ', 'ɪ_ɹa', 'ɪ', [])

    # ride = ridden
    f_irreg.add_arc('ɪ_ɹa', 'd_ɹaɪ', 'd', [])
    f_irreg.add_arc('d_ɹaɪ', 'end', '#', ['ɹ', 'ɪ', 'd', 'ə', 'n', '#'])

    # ring = rung
    f_irreg.add_arc('ɹ', 'ɪ_ɹ', 'ɪ', [])
    f_irreg.add_arc('ɪ_ɹ', 'ŋ_ɹɪ', 'ŋ', [])
    f_irreg.add_arc('ŋ_ɹɪ', 'end', '#', ['ɹ', 'ʌ', 'ŋ', '#'])

    # rise = risen
    f_irreg.add_arc('ɪ_ɹa', 'z_ɹaɪ', 'z', [])
    f_irreg.add_arc('z_ɹaɪ', 'end', '#', ['ɹ', 'ɪ', 'z', 'ə', 'n', '#'])

    # run = run
    f_irreg.add_arc('ɹ', 'ʌ_ɹ', 'ʌ', [])
    f_irreg.add_arc('ʌ_ɹ', 'n_ɹʌ', 'n', [])
    f_irreg.add_arc('n_ɹʌ', 'end', '#', ['ɹ', 'ʌ', 'n', '#'])

    # s arc
    f_irreg.add_arc('marker', 's', 's', [])

    # ʃ arc (for shake)
    f_irreg.add_arc('marker', 'ʃ', 'ʃ', [])

    # say = said
    f_irreg.add_arc('s', 'e_s', 'e', [])
    f_irreg.add_arc('e_s', 'ɪ_se', 'ɪ', [])
    f_irreg.add_arc('ɪ_se', 'end', '#', ['s', 'ɛ', 'd', '#'])

    # si arc
    f_irreg.add_arc('s', 'i_s', 'i', [])
    
    # see = seen
    f_irreg.add_arc('i_s', 'end', '#', ['s', 'i', 'n', '#'])

    # seek = sought
    f_irreg.add_arc('i_s', 'k_si', 'k', [])
    f_irreg.add_arc('k_si', 'end', '#', ['s', 'ɔ', 't', '#'])

    # sɛ arc
    f_irreg.add_arc('s', 'ɛ_s', 'ɛ', [])

    # sell = sold
    f_irreg.add_arc('ɛ_s', 'l_sɛ', 'l', [])
    f_irreg.add_arc('l_sɛ', 'end', '#', ['s', 'o', 'ʊ', 'l', 'd', '#'])

    # send = sent
    f_irreg.add_arc('ɛ_s', 'n_sɛ', 'n', [])
    f_irreg.add_arc('n_sɛ', 'd_sɛn', 'd', [])
    f_irreg.add_arc('d_sɛn', 'end', '#', ['s', 'ɛ', 'n', 't', '#'])

    # set = set
    f_irreg.add_arc('ɛ_s', 't_sɛ', 't', [])
    f_irreg.add_arc('t_sɛ', 'end', '#', ['s', 'ɛ', 't', '#'])

    # sew = sewn
    f_irreg.add_arc('s', 'o_s', 'o', [])
    f_irreg.add_arc('o_s', 'ʊ_so', 'ʊ', [])
    f_irreg.add_arc('ʊ_so', 'end', '#', ['s', 'o', 'ʊ', 'n', '#'])

    # shake = shaken
    f_irreg.add_arc('ʃ', 'e_ʃ', 'e', [])
    f_irreg.add_arc('e_ʃ', 'ɪ_ʃe', 'ɪ', [])
    f_irreg.add_arc('ɪ_ʃe', 'k_ʃeɪ', 'k', [])
    f_irreg.add_arc('k_ʃeɪ', 'end', '#', ['ʃ', 'e', 'ɪ','k', 'ə', 'n', '#'])

    # shine = shone
    f_irreg.add_arc('ʃ', 'a_ʃ', 'a', [])
    f_irreg.add_arc('a_ʃ', 'ɪ_ʃa', 'ɪ', [])
    f_irreg.add_arc('ɪ_ʃa', 'n_ʃaɪ', 'n', [])
    f_irreg.add_arc('n_ʃaɪ', 'end', '#', ['ʃ', 'o', 'ʊ', 'n', '#'])

    # shoot = shot
    f_irreg.add_arc('ʃ', 'u_ʃ', 'u', [])
    f_irreg.add_arc('u_ʃ', 't_ʃu', 't', [])
    f_irreg.add_arc('t_ʃu', 'end', '#', ['ʃ', 'ɑ', 't', '#'])

    # shrink = shrunk
    f_irreg.add_arc('ʃ', 'ɹ_ʃ', 'ɹ', [])
    f_irreg.add_arc('ɹ_ʃ', 'ɪ_ʃɹ', 'ɪ', [])
    f_irreg.add_arc('ɪ_ʃɹ', 'ŋ_ʃɹɪ', 'ŋ', [])
    f_irreg.add_arc('ŋ_ʃɹɪ', 'k_ʃɹɪŋ', 'k', [])
    f_irreg.add_arc('k_ʃɹɪŋ', 'end', '#', ['ʃ', 'ɹ', 'ʌ', 'ŋ', 'k', '#'])

    # shut = shut
    f_irreg.add_arc('ʃ', 'ʌ_ʃ', 'ʌ', [])
    f_irreg.add_arc('ʌ_ʃ', 't_ʃʌ', 't', [])
    f_irreg.add_arc('t_ʃʌ', 'end', '#', ['ʃ', 'ʌ', 't', '#'])

    # sɪ arc
    f_irreg.add_arc('s', 'ɪ_s', 'ɪ', [])

    # sɪŋ arc
    f_irreg.add_arc('ɪ_s', 'ŋ_sɪ', 'ŋ', [])

    # sing = sung
    f_irreg.add_arc('ŋ_sɪ', 'end', '#', ['s', 'ʌ', 'ŋ', '#'])

    # sink = sunk
    f_irreg.add_arc('ŋ_sɪ', 'k_sɪŋ', 'k', [])
    f_irreg.add_arc('k_sɪŋ', 'end', '#', ['s', 'ʌ', 'ŋ', 'k', '#'])

    # sit = sat
    f_irreg.add_arc('ɪ_s', 't_sɪ', 't', [])
    f_irreg.add_arc('t_sɪ', 'end', '#', ['s', 'æ', 't', '#'])

    # sl arc
    f_irreg.add_arc('s', 'l_s', 'l', [])

    # slay
    f_irreg.add_arc('l_s', 'e_sl', 'e', [])
    f_irreg.add_arc('e_sl', 'ɪ_sle', 'ɪ', [])
    f_irreg.add_arc('ɪ_sle', 'end', '#', ['s', 'l', 'e', 'ɪ', 'n','#'])

    # sleep = slept
    f_irreg.add_arc('l_s', 'i_sl', 'i', [])
    f_irreg.add_arc('i_sl', 'p_sli', 'p', [])
    f_irreg.add_arc('p_sli', 'end', '#', ['s', 'l', 'ɛ', 'p', 't', '#'])

    # slide = slid
    f_irreg.add_arc('l_s', 'a_sl', 'a', [])
    f_irreg.add_arc('a_sl', 'ɪ_sla', 'ɪ', [])
    f_irreg.add_arc('ɪ_sla', 'd_slaɪ', 'd', [])
    f_irreg.add_arc('d_slaɪ', 'end', '#', ['s', 'l', 'ɪ', 'd', '#'])

    # slit = slit
    f_irreg.add_arc('l_s', 'ɪ_sl', 'ɪ', [])
    f_irreg.add_arc('ɪ_sl', 't_slɪ', 't', [])
    f_irreg.add_arc('t_slɪ', 'end', '#', ['s', 'l', 'ɪ', 't', '#'])

    # sp arc
    f_irreg.add_arc('s', 'p_s', 'p', [])

    # speak = spoken
    f_irreg.add_arc('p_s', 'i_sp', 'i', [])
    f_irreg.add_arc('i_sp', 'k_spi', 'k', [])
    f_irreg.add_arc('k_spi', 'end', '#', ['s', 'p', 'o', 'ʊ', 'k', 'ə', 'n','#'])

    # spend = spent
    f_irreg.add_arc('p_s', 'ɛ_sp', 'ɛ', [])
    f_irreg.add_arc('ɛ_sp', 'n_spɛ', 'n', [])
    f_irreg.add_arc('n_spɛ', 'd_spɛn', 'd', [])
    f_irreg.add_arc('d_spɛn', 'end', '#', ['s', 'p', 'ɛ', 'n', 't', '#'])

    # spɪ arc
    f_irreg.add_arc('p_s', 'ɪ_sp', 'ɪ', [])

    # spin = spun
    f_irreg.add_arc('ɪ_sp', 'n_spɪ', 'n', [])
    f_irreg.add_arc('n_spɪ', 'end', '#', ['s', 'p', 'ʌ', 'n', '#'])

    # spit = spat
    f_irreg.add_arc('ɪ_sp', 't_spɪ', 't', [])
    f_irreg.add_arc('t_spɪ', 'end', '#', ['s', 'p', 'æ', 't', '#'])

    # split = split
    f_irreg.add_arc('p_s', 'l_sp', 'l', [])
    f_irreg.add_arc('l_sp', 'ɪ_spl', 'ɪ', [])
    f_irreg.add_arc('ɪ_spl', 't_splɪ', 't', [])
    f_irreg.add_arc('t_splɪ', 'end', '#', ['s', 'p', 'l', 'ɪ', 't', '#'])

    # spɹ arc
    f_irreg.add_arc('p_s', 'ɹ_sp', 'ɹ', [])

    # spread = spread
    f_irreg.add_arc('ɹ_sp', 'ɛ_spɹ', 'ɛ', [])
    f_irreg.add_arc('ɛ_spɹ', 'd_spɹɛ', 'd', [])
    f_irreg.add_arc('d_spɹɛ', 'end', '#', ['s', 'p', 'ɹ', 'ɛ', 'd', '#'])

    # spring = sprung
    f_irreg.add_arc('ɹ_sp', 'ɪ_spɹ', 'ɪ', [])
    f_irreg.add_arc('ɪ_spɹ', 'ŋ_spɹɪ', 'ŋ', [])
    f_irreg.add_arc('ŋ_spɹɪ', 'end', '#', ['s', 'p', 'ɹ', 'ʌ', 'ŋ', '#'])

    # st arc
    f_irreg.add_arc('s', 't_s', 't', [])

    # stand = stood
    f_irreg.add_arc('t_s', 'æ_st', 'æ', [])
    f_irreg.add_arc('æ_st', 'n_stæ', 'n', [])
    f_irreg.add_arc('n_stæ', 'd_stæn', 'd', [])
    f_irreg.add_arc('d_stæn', 'end', '#', ['s','t','ʊ','d','#'])

    # steal = stolen
    f_irreg.add_arc('t_s', 'i_st', 'i', [])
    f_irreg.add_arc('i_st', 'l_sti', 'l', [])
    f_irreg.add_arc('l_sti', 'end', '#', ['s','t','o','ʊ','l','ə', 'n','#'])

    # stɪ arc
    f_irreg.add_arc('t_s', 'ɪ_st', 'ɪ', [])

    # stick = stuck
    f_irreg.add_arc('t_s', 'ɪ_st', 'ɪ', [])
    f_irreg.add_arc('ɪ_st', 'k_stɪ', 'k', [])
    f_irreg.add_arc('k_stɪ', 'end', '#', ['s','t','ʌ','k','#'])

    # stɪŋ arc
    f_irreg.add_arc('ɪ_st', 'ŋ_stɪ', 'ŋ', [])

    # sting = stung
    f_irreg.add_arc('ŋ_stɪ', 'end', '#', ['s','t','ʌ','ŋ','#'])

    # stink = stunk
    f_irreg.add_arc('ŋ_stɪ', 'k_stɪŋ', 'k', [])
    f_irreg.add_arc('k_stɪŋ', 'end', '#', ['s','t','ʌ','ŋ','k','#'])

    # str arc
    f_irreg.add_arc('t_s', 'ɹ_st', 'ɹ', [])

    # stɹa arc
    f_irreg.add_arc('ɹ_st', 'a_stɹ', 'a', [])

    # stɹaɪ
    f_irreg.add_arc('a_stɹ', 'ɪ_stɹa', 'ɪ', [])

    # stride = stridden
    f_irreg.add_arc('ɪ_stɹa', 'd_stɹaɪ', 'd', [])
    f_irreg.add_arc('d_stɹaɪ', 'end', '#', ['s','t','ɹ','ɪ','d', 'ə', 'n', '#'])

    # strike = struck
    f_irreg.add_arc('ɪ_stɹa', 'k_stɹaɪ', 'k', [])
    f_irreg.add_arc('k_stɹaɪ', 'end', '#', ['s','t','ɹ','ʌ','k','#'])
     
    # string = strung
    f_irreg.add_arc('ɹ_st', 'ɪ_stɹ', 'ɪ', [])
    f_irreg.add_arc('ɪ_stɹ', 'ŋ_stɹɪ', 'ŋ', [])
    f_irreg.add_arc('ŋ_stɹɪ', 'end', '#', ['s','t','ɹ','ʌ','ŋ','#'])

    # sw arc
    f_irreg.add_arc('s', 'w_s', 'w', [])

    # swɛ arc
    f_irreg.add_arc('w_s', 'ɛ_sw', 'ɛ', [])

    # swear = sworn
    f_irreg.add_arc('ɛ_sw', 'ɹ_swɛ', 'ɹ', [])
    f_irreg.add_arc('ɹ_swɛ', 'end', '#', ['s','w','ɔ','ɹ', 'n', '#'])

    # sweep = swept
    f_irreg.add_arc('w_s', 'i_sw', 'i', [])
    f_irreg.add_arc('i_sw', 'p_swi', 'p', [])
    f_irreg.add_arc('p_swi', 'end', '#', ['s','w','ɛ','p','t','#'])

    # swell = swollen
    f_irreg.add_arc('ɛ_sw', 'l_swɛ', 'l', [])
    f_irreg.add_arc('l_swɛ', 'end', '#', ['s', 'w', 'o', 'ʊ', 'l','ə', 'n','#'])

    # swɪ arc
    f_irreg.add_arc('w_s', 'ɪ_sw', 'ɪ', [])

    # swim = swum
    f_irreg.add_arc('ɪ_sw', 'm_swɪ', 'm', [])
    f_irreg.add_arc('m_swɪ', 'end', '#', ['s','w','ʌ','m','#'])

    # swing = swung
    f_irreg.add_arc('ɪ_sw', 'ŋ_swɪ', 'ŋ', [])
    f_irreg.add_arc('ŋ_swɪ', 'end', '#', ['s','w','ʌ','ŋ','#'])

    # t state
    f_irreg.add_arc('marker', 't', 't', [])

    # take = taken
    f_irreg.add_arc('t', 'e_t', 'e', [])
    f_irreg.add_arc('e_t', 'ɪ_te', 'ɪ', [])
    f_irreg.add_arc('ɪ_te', 'k_teɪ', 'k', [])
    f_irreg.add_arc('k_teɪ', 'end', '#', ['t', 'e', 'ɪ', 'k', 'ə', 'n', '#'])

    # teach = taught
    f_irreg.add_arc('t', 'i_t', 'i', [])
    f_irreg.add_arc('i_t', 't_ti', 't', [])
    f_irreg.add_arc('t_ti', 'ʃ_tit', 'ʃ', [])
    f_irreg.add_arc('ʃ_tit', 'end', '#', ['t', 'ɔ', 't', '#'])

    # tɛ arc
    f_irreg.add_arc('t', 'ɛ_t', 'ɛ', [])
    
    # tear = torn        
    f_irreg.add_arc('ɛ_t', 'ɹ_tɛ', 'ɹ', [])
    f_irreg.add_arc('ɹ_tɛ', 'end', '#', ['t','ɔ','ɹ','n', '#'])

    # tell = told
    f_irreg.add_arc('ɛ_t', 'l_tɛ', 'l', [])
    f_irreg.add_arc('l_tɛ', 'end', '#', ['t','o','ʊ','l','d','#'])

    # θ arc
    f_irreg.add_arc('marker', 'θ', 'θ', [])

    # think = thought
    f_irreg.add_arc('θ', 'ɪ_θ', 'ɪ', [])
    f_irreg.add_arc('ɪ_θ', 'ŋ_θɪ', 'ŋ', [])
    f_irreg.add_arc('ŋ_θɪ', 'k_θɪŋ', 'k', [])
    f_irreg.add_arc('k_θɪŋ', 'end', '#', ['θ','ɔ','t','#'])

    # throw = thrown
    f_irreg.add_arc('θ', 'ɹ_θ', 'ɹ', [])
    f_irreg.add_arc('ɹ_θ', 'o_θɹ', 'o', [])
    f_irreg.add_arc('o_θɹ', 'ʊ_θɹo', 'ʊ', [])
    f_irreg.add_arc('ʊ_θɹo', 'end', '#', ['θ','ɹ','o', 'ʊ', 'n', '#'])

    # understand = understood
    f_irreg.add_arc('marker', 'ʌ', 'ʌ', [])
    f_irreg.add_arc('ʌ', 'n_ʌ', 'n', [])
    f_irreg.add_arc('n_ʌ', 'd_ʌn', 'd', [])
    f_irreg.add_arc('d_ʌn', 'ə_ʌnd', 'ə', [])
    f_irreg.add_arc('ə_ʌnd', 'ɹ_ʌndə', 'ɹ', [])
    f_irreg.add_arc('ɹ_ʌndə', 's_ʌndəɹ', 's', [])
    f_irreg.add_arc('s_ʌndəɹ', 't_ʌndəɹs', 't', [])
    f_irreg.add_arc('t_ʌndəɹs', 'æ_ʌndəɹst', 'æ', [])
    f_irreg.add_arc('æ_ʌndəɹst', 'n_ʌndəɹstæ', 'n', [])
    f_irreg.add_arc('n_ʌndəɹstæ', 'd_ʌndəɹstæn', 'd', [])
    f_irreg.add_arc('d_ʌndəɹstæn', 'end', '#', ['ʌ', 'n', 'd', 'ə', 'ɹ', 's', 't', 'ʊ', 'd', '#'])

    # w arc
    f_irreg.add_arc('marker', 'w', 'w', [])

    # we arc
    f_irreg.add_arc('w', 'e_w', 'e', [])

    # wake = woken
    f_irreg.add_arc('e_w', 'ɪ_we', 'ɪ', [])
    f_irreg.add_arc('ɪ_we', 'k_weɪ', 'k', [])
    f_irreg.add_arc('k_weɪ', 'end', '#', ['w','o','ʊ','k', 'ə', 'n', '#'])

    # wɛ arc
    f_irreg.add_arc('w', 'ɛ_w', 'ɛ', [])

    # wear = worn
    f_irreg.add_arc('ɛ_w', 'ɹ_wɛ', 'ɹ', [])
    f_irreg.add_arc('ɹ_wɛ', 'end', '#', ['w','ɔ','ɹ', 'n','#'])

    # wed = wed
    f_irreg.add_arc('ɛ_w', 'd_wɛ', 'd', [])
    f_irreg.add_arc('d_wɛ', 'end', '#', ['w','ɛ','d','#'])

    # weep = wept
    f_irreg.add_arc('w', 'i_w', 'i', [])
    f_irreg.add_arc('i_w', 'p_wi', 'p', [])
    f_irreg.add_arc('p_wi', 'end', '#', ['w','ɛ','p','t','#'])

    # wet = wet
    f_irreg.add_arc('ɛ_w', 't_wɛ', 't', [])
    f_irreg.add_arc('t_wɛ', 'end', '#', ['w','ɛ','t','#'])

    # win = won
    f_irreg.add_arc('w', 'ɪ_w', 'ɪ', [])
    f_irreg.add_arc('ɪ_w', 'n_wɪ', 'n', [])
    f_irreg.add_arc('n_wɪ', 'end', '#', ['w', 'ʌ', 'n', '#'])

    # wring = wrung
    f_irreg.add_arc('ɹ_w', 'ɪ_ɹ_w', 'ɪ', [])
    f_irreg.add_arc('ɪ_ɹ_w', 'ŋ_ɹɪ_w', 'ŋ', [])
    f_irreg.add_arc('ŋ_ɹɪ_w', '__ɹɪŋ_w', '_', [])
    f_irreg.add_arc('__ɹɪŋ_w', 'w__ɹɪŋ_w', 'w', [])
    f_irreg.add_arc('w__ɹɪŋ_w', 'end', '#', ['w', '_', 'ɹ', 'ʌ', 'ŋ', '#'])

    # write = written
    f_irreg.add_arc('ɪ_ɹa', 't_ɹaɪ', 't', [])
    f_irreg.add_arc('t_ɹaɪ', 'end', '#', ['ɹ', 'ɪ', 't', 'ə', 'n', '#'])

    return f_irreg


def final_participle_fst(inp):
    f_irreg = participle_irreg()
    out = f_irreg.transduce(inp)

    if out:
        return out

    f_reg = participle_regular()
    return f_reg.transduce(inp)
