import sys
from fst import FST
from morphological_analyzer_fst import final_morph_analyzer_fst 
from eng_dictionary import eng_dictionary
from ipa_dictionary import ipa_dictionary

# load dictionaries
ENG_DICT = eng_dictionary()
IPA_DICT = ipa_dictionary()


def ipa_to_tokens(ipa_str):
    """
    Convert an IPA string into a list of symbols suitable for the FST.

    Examples:
      '#sɪts#'     → ['#', 's', 'ɪ', 't', 's', '#']
      '# s ɪ t s #' → ['#', 's', 'ɪ', 't', 's', '#']
    """
    ipa_str = ipa_str.strip()

    # If user gives space-separated symbols, just split:
    if " " in ipa_str:
        return ipa_str.split()

    # Otherwise treat each character as one symbol:
    return list(ipa_str)


def join_output(output):
    """
    Convert the FST output into a printable string.

    The output may be a list of symbols or a string.
    Boundary markers (#) and grammatical tags are preserved.
    """
    if output is None:
        return ""

    if isinstance(output, list):
        return "".join(output)
    return str(output)


def analyze(tokens):
    """
    Run the combined (irregular + regular) morphological analyzer.
    """
    return final_morph_analyzer_fst(tokens)


def orth_to_ipa_form(orth_word):
    """
    Given an English spelling such as 'abided' or 'abides',
    search the English dictionary to find:
      - the base verb entry
      - the grammatical slot (past, present, etc.)
      - the corresponding IPA form

    Returns:
      (base_entry, slot, ipa_form)

    Returns (None, None, None) if the word is not found
    or if there is a mismatch between dictionaries.
    """
    
    # Loop through all base verb entries in the English dictionary
    for lemma, forms in ENG_DICT.items():
        for slot, eng_form in forms.items():
            if eng_form == orth_word:
                # Found the matching lemma + slot
                if lemma not in IPA_DICT:
                    # Mismatch between ENG_DICT and IPA_DICT, treat as not-found
                    return None, None, None
                if slot not in IPA_DICT[lemma]:
                    return None, None, None

                ipa_form = IPA_DICT[lemma][slot]  # e.g. "#əbaɪdɪd#"
                return lemma, slot, ipa_form

    # No match in ENG_DICT
    return None, None, None


if __name__ == "__main__":
    print("Morphological Analyzer (irregular + regular)")
    print("Enter a verb in English orthography (e.g.  says)")
    print("Or enter IPA *with boundaries* (e.g.  #sɛz#)")
    print("Press ENTER to quit.\n")

    while True:
        raw = input("Verb to analyze: ").strip()
        if not raw:
            print("Goodbye!")
            break

        # Case 1: IPA with #...#
        if raw.startswith("#") and raw.endswith("#"):
            ipa_str = raw
            tokens = ipa_to_tokens(ipa_str)

        # Case 2: English orthography
        else:
            lemma, slot, ipa_str = orth_to_ipa_form(raw)

            if ipa_str is None:
                print("Sorry, that verb is not in the dictionary.")
                print("Try another verb or enter your verb in IPA, using #...# form.")
                print("Try again.\n")
                continue

            tokens = ipa_to_tokens(ipa_str)

        # Run through the FST analyzer
        output = analyze(tokens)

        if not output:
            print("No analysis found by the reverse inflector.\n")
            continue

        out_str = join_output(output)

        print("\nInput (IPA):", "".join(tokens))
        print("Analysis:           ", out_str)
        print()

