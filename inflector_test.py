import sys
import csv
from fst import FST
from fsmutils import composewords

# Import your FST constructors
from present_3sg_fst import final_pres_fst
from progressive_fst import progressive
from past_fst import final_past_fst
from participle_fst import final_participle_fst
from ipa_dictionary import ipa_dictionary
#from compiler import strip_and_join


IPA = ipa_dictionary()

def strip_and_join(output):
    # remove markers and join IPA tokens
    if not output:
        return ''
    
    # If output is nested list (common for FSTs)
    if isinstance(output, list) and all(isinstance(i, list) for i in output):
        # Take first path for simplicity
        tokens = output[0]
    else:
        tokens = output
    
    # Remove markers if nested
    if isinstance(tokens, list):
        tokens = [t for t in tokens if t != '#']
    else:
        tokens = [t for t in str(tokens) if t != '#']
    
    return ''.join(tokens)

def test_fsts(write_csv=False):
    f_prog = progressive()

    # counters
    totals = {"Present 3rd Singular": 0, "Progressive": 0, "Past": 0, "Perfect": 0}
    correct = {"Present 3rd Singular": 0, "Progressive": 0, "Past": 0, "Perfect": 0}

    csv_rows = [] if write_csv else None

    print("\n====== FST ACCURACY REPORT ======\n")

    # Calculate Accuracy
    for verb, forms in IPA.items():
        ipa_bare = forms["bare"]
        ipa_tokens = list(ipa_bare)

        # RUN FSTs (predict)

        predicted_fst_pres  = strip_and_join(final_pres_fst(ipa_tokens))
        predicted_fst_prog  = strip_and_join(f_prog.transduce(ipa_tokens))
        predicted_fst_past  = strip_and_join(final_past_fst(ipa_tokens))
        predicted_fst_perf  = strip_and_join(final_participle_fst(ipa_tokens))

        # Expected IPA form
        gold_pres = strip_and_join(forms["pres3sg"])
        gold_prog = strip_and_join(forms["prog"])
        gold_past = strip_and_join(forms["past"])
        gold_perf = strip_and_join(forms["perfect"])

        # Evaluate
        tests = [
            ("Present 3rd Singular", predicted_fst_pres, gold_pres),
            ("Progressive",      predicted_fst_prog, gold_prog),
            ("Past",      predicted_fst_past, gold_past),
            ("Perfect",   predicted_fst_perf, gold_perf)
        ]

        for tense, pred, gold in tests:
            totals[tense] += 1
            is_correct = (pred == gold)

            if is_correct:
                correct[tense] += 1
                print(f"  + {tense:8}  {pred}")
            else:
                print(f"  - {tense:8}  predicted={pred}   expected={gold}")

            if write_csv:
                csv_rows.append([verb, tense, pred, gold, "+" if is_correct else "-"])


        print(f"Verb: {verb}")
        print(f"IPA tokens: {ipa_tokens}")
        out = final_pres_fst(ipa_tokens)
        print(f"Output raw: {out}")

    # Summary
    print("\n\n====== FINAL ACCURACY ======")
    for tense in totals:
        acc = 100 * correct[tense] / totals[tense] if totals[tense] else 0
        print(f"{tense:8}: {acc:.1f}% ({correct[tense]}/{totals[tense]})")

    print("\n=============================\n")

    # write csv file
    if write_csv:
        with open("total_fst_results.csv", "w", newline='', encoding="utf-8") as f:
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
        
        print("Saved results to total_fst_results.csv")

if __name__ == "__main__":
    write_csv = "--csv" in sys.argv
    test_fsts(write_csv=write_csv)