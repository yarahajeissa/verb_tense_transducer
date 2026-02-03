import sys
import csv
from fst import FST
from fsmutils import composewords

from ipa_dictionary import ipa_dictionary
from morphological_analyzer_fst import final_morph_analyzer_fst

IPA = ipa_dictionary()


def join_output(output):
    # Join FST output (list of symbols) into a string without modifying it.
    if output is None:
        return ''
    if isinstance(output, list):
        return ''.join(output)
    return str(output)


def parse_analysis(out_str):
    # split analyzer into predicted base and tag
    '''
    Example:
      input: '#sɪt#3SG-PRES' 
      base = '#sɪt#'
      tag  = '3SG-PRES'
    '''
    if not out_str:
        return "", ""

    # find final boundary marker
    last_hash = out_str.rfind("#")
    if last_hash == -1:
        return out_str, ""

    # base form up to and including final #
    base = out_str[: last_hash + 1] 

    # after that is tag
    tag = out_str[last_hash + 1 :].strip() 
    return base, tag

# expected tag substrings for each grammatical slot
EXPECTED_TAG_SUBSTR = {
    "pres3sg": "3SG-PRES",
    "prog": "PROG",
    "past": "PST",        
    "perfect": "PST"     
}

# evaluate accuracies
def test_fsts(write_csv=False):
    # counter
    totals  = {"Present 3rd Singular": 0, "Progressive": 0, "Past": 0, "Perfect": 0}
    correct = {"Present 3rd Singular": 0, "Progressive": 0, "Past": 0, "Perfect": 0}

    csv_rows = [] if write_csv else None

    print("\n====== ANALYZER ACCURACY REPORT ======\n")

    for verb, forms in IPA.items():
        if "bare" not in forms:
            continue
        bare_ipa = forms["bare"]         

        print(f"Verb: {verb}")
        print(f"  Bare IPA: {bare_ipa}")

        tense_tests = [
            ("Present 3rd Singular", "pres3sg"),
            ("Progressive",          "prog"),
            ("Past",                 "past"),
            ("Perfect",              "perfect"),
        ]

        # test for match to gold standard
        for tense_label, slot in tense_tests:
            if slot not in forms:
                continue

            ipa_form = forms[slot]
            ipa_tokens = list(ipa_form)

            totals[tense_label] += 1

            # Run the analyzer
            out = final_morph_analyzer_fst(ipa_tokens)
            out_str = join_output(out)
            base_ipa, tag = parse_analysis(out_str)

            expected_tag_piece = EXPECTED_TAG_SUBSTR[slot]

            # Check that base matches the dictionary bare form
            base_ok = (base_ipa == bare_ipa)

            # Check that tag matches expected tense
            tag_ok = expected_tag_piece in tag

            is_correct = base_ok and tag_ok

            if is_correct:
                correct[tense_label] += 1
                print(f"  + {tense_label:18}  input={ipa_form:12}  base={base_ipa:12}  tag={tag}")
            else:
                print(f"  - {tense_label:18}  input={ipa_form}")
                print(f"      Analyzer: base={base_ipa!r}, tag={tag!r}")
                print(f"      Expected: base={bare_ipa!r}, tag contains {expected_tag_piece!r}")
            
            if write_csv:
                csv_rows.append([
                    verb,
                    tense_label,
                    ipa_form,
                    base_ipa,
                    tag,
                    expected_tag_piece,
                    "Right" if is_correct else "Wrong"
                ])
        print()

    # Summary
    print("\n\n====== FINAL ANALYZER ACCURACY ======")
    for tense in totals:
        total = totals[tense]
        corr  = correct[tense]
        acc = 100 * corr / total if total else 0.0
        print(f"{tense:18}: {acc:.1f}% ({corr}/{total})")
    print("\n=====================================\n")

    # write csv file
    if write_csv:
        with open("analyzer_results.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "verb", "tense",
                "input_ipa", "predicted_base",
                "predicted_tag", "expected_tag_piece",
                "correct"
            ])
            writer.writerows(csv_rows)

            writer.writerow([])

            writer.writerow(["Tense", "Accuracy %", "Correct", "Total"])
            for tense in totals:
                tot = totals[tense]
                corr = correct[tense]
                if tot == 0:
                    writer.writerow([tense, "N/A", 0, 0])
                else:
                    acc = 100 * corr / tot
                    writer.writerow([tense, f"{acc:.1f}", corr, tot])

        print("Saved results to analyzer_results.csv")

if __name__ == "__main__":
    write_csv = "--csv" in sys.argv
    test_fsts(write_csv=write_csv)
