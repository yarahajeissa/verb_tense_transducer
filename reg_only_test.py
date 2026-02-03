import sys
import csv
from fst import FST
from fsmutils import composewords

from present_3sg_fst import pres_regular
from progressive_fst import progressive
from past_fst import past_regular
from participle_fst import participle_regular
from ipa_dictionary import ipa_dictionary

IPA = ipa_dictionary()

# convert FST output into IPA string, join characters remove boundary markers
def strip_and_join(output):
    if not output:
        return ''

    if isinstance(output, list) and all(isinstance(i, list) for i in output):
        tokens = output[0]
    else:
        tokens = output

    # remove boundary markers
    if isinstance(tokens, list):
        tokens = [t for t in tokens if t != '#']
    else:
        tokens = [t for t in str(tokens) if t != '#']

    return ''.join(tokens)

# evaluate regular verb fst ONLY
def test_regular_fsts(write_csv=False):
    # initilaize all regular fsts
    f_pres = pres_regular()
    f_prog = progressive()
    f_past = past_regular()
    f_participle = participle_regular()

    # counters
    totals = {"Present 3rd Singular": 0, "Progressive": 0, "Past": 0, "Perfect": 0}
    correct = {"Present 3rd Singular": 0, "Progressive": 0, "Past": 0, "Perfect": 0}
    
    csv_rows = [] if write_csv else None

    print("\n====== REGULAR FST ACCURACY REPORT ======\n")

    for verb, forms in IPA.items():
    

        # skip irregulars
        if forms.get("irregular", False):
            continue

        ipa_bare = forms["bare"]
        ipa_tokens = list(ipa_bare)

        # Run only reg fsts
        predicted_pres = strip_and_join(f_pres.transduce(ipa_tokens))
        predicted_prog = strip_and_join(f_prog.transduce(ipa_tokens))
        predicted_past = strip_and_join(f_past.transduce(ipa_tokens))
        predicted_perf = strip_and_join(f_participle.transduce(ipa_tokens))

        # Gold standard
        gold_pres = strip_and_join(forms["pres3sg"])
        gold_prog = strip_and_join(forms["prog"])
        gold_past = strip_and_join(forms["past"])
        gold_perf = strip_and_join(forms["perfect"])

        tests = [
            ("Present 3rd Singular", predicted_pres, gold_pres),
            ("Progressive", predicted_prog, gold_prog),
            ("Past", predicted_past, gold_past),
            ("Perfect", predicted_perf, gold_perf),
        ]

        print(f"Verb: {verb}")
        print(f"IPA input: {ipa_tokens}")

        # eval predictions for each tense
        for tense, pred, gold in tests:

            totals[tense] += 1
            is_correct = (pred == gold)

            if is_correct:
                correct[tense] += 1
                print(f"  + {tense:12}  {pred}")
            else:
                print(f"  - {tense:12}  predicted={pred} expected={gold}")

            
            if write_csv:
                csv_rows.append([verb, tense, pred, gold, "+" if is_correct else "-"])


    print("\n====== FINAL REGULAR FST ACCURACY ======")
    for tense in totals:
        acc = 100 * correct[tense] / totals[tense]
        print(f"{tense:12}: {acc:.1f}% ({correct[tense]}/{totals[tense]})")

    print("\n=========================================\n")

    if write_csv:
        with open("regular_fst_results.csv", "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["verb", "tense", "predicted", "gold", "correct"])
            writer.writerows(csv_rows)

            writer.writerow([])

            writer.writerow(["Tense", "Accuracy %", "Correct", "Total"])
            for tense in totals:
                if totals[tense] == 0:
                    writer.writerow([tense, "no data", correct[tense], totals[tense]])
                else:
                    acc = 100 * correct[tense] / totals[tense]
                    writer.writerow([tense, f"{acc:.1f}", correct[tense], totals[tense]])


        print("Saved results to regular_fst_results.csv")

if __name__ == "__main__":

    write_csv = "--csv" in sys.argv
    test_regular_fsts(write_csv=write_csv)
