English Verb Inflector and Reverse Inflector

This project contains a bidirectional morphological system of English verbs through the implementation 
of Finite State Transducers (FSTs). 

verb_inflector.py takes in a bare English verb and returns the verb in the bare form, 3rd person singular present tense, progressive tense, past tense, and participle form. English spelling input (eg. abide) is
allowed as long as the verb is included in the dictionary eng_dictionary.py. If the verb is not included
in the dictionary, use the IPA transcription of that verb surrounded by word boundaries # (eg. #əbaɪd#) 
so that the model can distinguish between orthography and IPA (note the distinction between sit and #sit#). The input goes through the irregular tense inflector first, and if there is no output, the input goes through the regular tense inflector analyzer. 

Example output:

Verb to convert: say

Base IPA:     seɪ
Present:      sɛz
Progressive:  seɪɪŋ
Past:         sɛd
Participle:   sɛd

reverse_inflector.py takes in an English verb of any tense and returns the verb in its bare form followed
by its tense marker. English spelling input (eg. abided) is allowed as long as the verb is included in the dictionary eng_dictionary.py. If the verb is not included in the dictionary, use the IPA transcription of that verb surrounded by word boundaries # (eg. #əbaɪd#) so that the model can distinguish between orthography and IPA (note the distinction between sit and #sit#). The input goes through the irregular morphological analyzer first, and if there is no output, the input goes through the regular morphological analyzer. 

Example output:

Form to analyze: says

Input (IPA): #sɛz#
Analysis:            #seɪ# PRES


Usage Instructions
 
We have 5 main scripts that you can run (sample outputs mentioned above). The following lists the instructions to run these files.

verb_inflector.py:
In your terminal run python verb_inflector.py

reverse_inflector.py:
In your terminal run python reverse_inflector.py

reg_only_test.py:
In your terminal run python reg_only_test.py to have the results pasted in your terminal. If you wish to print out a CSV of the results run python reg_only_test.py --csv

inflector_test.py:
In your terminal run python inflector_test.py to have the results pasted in your terminal. If you wish to print out a CSV of the results run python inflector_test.py --csv

morph_analyzer_test.py
In your terminal run morph_analyzer_test.py to have the results pasted in your terminal. If you wish to print out a CSV of the results run python morph_analyzer_test.py --csv

Dictionaries:

ipa_dictionary.py includes 269 English verbs inflected into 5 forms: bare, past, 3rd person singular present, progressive, and past participle. The entry is the orthographic representation while the 5 definitions are IPA representations. These dictionaries outline what verbs are acceptable inputs as English orthography. 

Example entry:

"say": { 
            "bare": "#seɪ#", 
            "past": "#sɛd#", 
            "prog": "#seɪɪŋ#",
            "pres3sg": "#sɛz#", 
            "perfect": "#sɛd#" 
        }

English_dictionary.py includes the same 269 English verbs and 5 inflections as ipa_dictionary.py: bare, past, 3rd person singular present, progressive, and past participle. All entries and definitions are represented in English orthography. These dictionaries outline what verbs are acceptable inputs as English orthography.


Example entry:

"say":        { 
            "bare":"say",        
            "past":"said",      
            "prog":"saying",    
            "pres3sg":"says",      
            "perfect":"said" 
        },


Results:

reg_only_test.py returns the accuracy of our regular verb inflector model alone on all verbs outlined in the dictionary. 

Sample correct output:

Verb: zoom
IPA input: ['#', 'z', 'u', 'm', '#']
  + Present 3rd Singular  zumz
  + Progressive   zumɪŋ
  + Past          zumd
  + Perfect       zumd


Sample incorrect output:

Verb: win
IPA input: ['#', 'w', 'ɪ', 'n', '#']
  + Present 3rd Singular  wɪnz
  + Progressive   wɪnɪŋ
  - Past          predicted=wɪnd expected=wʌn
  - Perfect       predicted=wɪnd expected=wʌn

Overall results:

====== FINAL REGULAR FST ACCURACY ======
Present 3rd Singular: 91.8% (247/269)
Progressive : 94.8% (255/269)
Past        : 56.9% (153/269)
Perfect     : 56.9% (153/269)

=========================================


inflector_test.py returns the accuracy of our comprehensive verb inflector model on all verbs outlined in the dictionary. 

Sample correct output:

  + Present 3rd Singular  zumz
  + Progressive  zumɪŋ
  + Past      zumd
  + Perfect   zumd
Verb: zoom
IPA tokens: ['#', 'z', 'u', 'm', '#']
Output raw: ['#', 'z', 'u', 'm', 'z', '#']



Sample incorrect output:

  + Present 3rd Singular  wɪl
  - Progressive  predicted=wɪlɪŋ   expected=No Progresive
  - Past      predicted=wɪld   expected=wʊd
  - Perfect   predicted=wɪld   expected=No Perfect Participle
Verb: will
IPA tokens: ['#', 'w', 'ɪ', 'l', '#']
Output raw: ['#', 'w', 'ɪ', 'l', '#']

Overall results:

====== FINAL ACCURACY ======
Present 3rd Singular: 96.3% (259/269)
Progressive: 94.8% (255/269)
Past    : 94.1% (253/269)
Perfect : 94.1% (253/269)

=============================



morph_analyzer_test.py returns the accuracy of our comprehensive reverse inflector model on all verbs outlined in the dictionary. 

Sample correct output:

Verb: win
  Bare IPA: #wɪn#
  + Present 3rd Singular  input=#wɪnz#        base=#wɪn#         tag=3SG-PRES
  + Progressive         input=#wɪnɪŋ#       base=#wɪn#         tag=PROG
  + Past                input=#wʌn#         base=#wɪn#         tag=PST/ PST.PTCP
  + Perfect             input=#wʌn#         base=#wɪn#         tag=PST/ PST.PTCP


Sample incorrect output:

Verb: would
  Bare IPA: #wʊd#
  - Present 3rd Singular  input=#wʊd#
      Analyzer: base='#wʊ#', tag='PST/ PST.PTCP'
      Expected: base='#wʊd#', tag contains '3SG-PRES'
  - Progressive         input=No Progresive
      Analyzer: base='', tag=''
      Expected: base='#wʊd#', tag contains 'PROG'
  - Past                input=#wʊd#
      Analyzer: base='#wʊ#', tag='PST/ PST.PTCP'
      Expected: base='#wʊd#', tag contains 'PST'
  - Perfect             input=No Perfect Participle
      Analyzer: base='', tag=''
      Expected: base='#wʊd#', tag contains 'PST'

Overall results:

====== FINAL ANALYZER ACCURACY ======
Present 3rd Singular: 90.3% (243/269)
Progressive       : 94.8% (255/269)
Past              : 88.1% (237/269)
Perfect           : 88.1% (237/269)

=====================================
