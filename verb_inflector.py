import sys
from fst import FST
from fsmutils import composewords,composechars,trace

from present_3sg_fst import final_pres_fst
from progressive_fst import progressive
from past_fst import final_past_fst
from participle_fst import final_participle_fst
from ipa_dictionary import ipa_dictionary

IPA_DICT = ipa_dictionary() 


def ipa_to_tokens(ipa_bare):
    return [ch for ch in ipa_bare]


def strip_and_join(output):
        """Removes markers and joins IPA tokens."""
        if output is None:
            return ''

        # for list of tokens
        if isinstance(output, list):
            tokens = [t for t in output if t != '#']
        # for string
        else:
            tokens = [t for t in output.split() if t != '#']
        return ''.join(tokens)

    
if __name__ == "__main__":
    f_prog = progressive()

    print("Multi-Tense Verb Inflecter")
    print("Enter a verb in English orthography (e.g. say, sit).")
    print("Or enter IPA *with boundaries* (e.g.  #sɪt#  or  #seɪ#)")
    print("Press ENTER to quit.\n")

    while True:
        raw = input("Verb to convert: ").strip()
        if not raw:
            print("Goodbye!")
            break

        # IPA input (# on both ends)
        if raw.startswith("#") and raw.endswith("#") and len(raw) > 2:
            ipa_bare = raw
            ipa_tokens = ipa_to_tokens(ipa_bare)

        # Orthography input
        else:
            orth_verb = raw.lower()

            if orth_verb not in IPA_DICT:
                print("Sorry, that verb is not in the dictionary.")
                print("Try another verb or enter your verb in IPA, using #...# form.")
                print("Try again.\n")
                continue

            ipa_bare = IPA_DICT[orth_verb]["bare"]
            ipa_tokens = ipa_to_tokens(ipa_bare)

        # Run through FSTs
        pres_output = final_pres_fst(ipa_tokens)
        prog_output = f_prog.transduce(ipa_tokens)
        past_output = final_past_fst(ipa_tokens)
        participle_output = final_participle_fst(ipa_tokens)

        # Cleanup
        bare_ipa = strip_and_join(ipa_to_tokens(ipa_bare))
        pres_ipa = strip_and_join(pres_output)
        prog_ipa = strip_and_join(prog_output)
        past_ipa = strip_and_join(past_output)
        participle_ipa = strip_and_join(participle_output)

        # Output
        print(f"\nBase IPA:     {bare_ipa}")
        print(f"Present:      {pres_ipa}")
        print(f"Progressive:  {prog_ipa}")
        print(f"Past:         {past_ipa}")
        print(f"Participle:   {participle_ipa}\n")