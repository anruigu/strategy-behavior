#!/usr/bin/env python
"""Compare TRAIT profiles across arms.

Scores are % preference for the HIGH pole of each trait, from TRAIT's own
likelihood-based methodology with both option orders counterbalanced.

Only trust a row when `unscored` is small: an arm whose vllm engine dropped out
mid-run still writes a complete-looking JSON, and an earlier pass produced a
plausible dark-triad profile from 78% of its items with a dying server.
"""
import json
import os

R = os.path.dirname(os.path.abspath(__file__)) + "/results"
TRAITS = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness",
          "Neuroticism", "Machiavellianism", "Narcissism", "Psychopathy"]
ARMS = [("base", "trait-base"), ("kuhn-400", "trait-kuhn400"),
        ("mathRL-64", "trait-mathrl064"), ("pigDice-192", "trait-pig192")]


def main():
    data = {}
    for label, arm in ARMS:
        p = f"{R}/{arm}.json"
        if os.path.exists(p):
            data[label] = json.load(open(p))

    header = f"{'trait':22s}" + "".join(f"{l:>11s}" for l, _ in ARMS)
    header += f"{'d(kuhn)':>10s}{'d(math)':>10s}"
    print(header)
    print("-" * len(header))
    for t in TRAITS:
        vals = {l: data.get(l, {}).get("scores", {}).get(t) for l, _ in ARMS}
        row = f"{t:22s}"
        for l, _ in ARMS:
            v = vals[l]
            row += f"{('%.1f' % v if v is not None else '--'):>11s}"
        b = vals.get("base")
        for l in ("kuhn-400", "mathRL-64"):
            v = vals.get(l)
            d = ("%+.1f" % (v - b)) if (v is not None and b is not None) else "--"
            row += f"{d:>10s}"
        print(row)
    print()
    for label, _ in ARMS:
        d = data.get(label)
        if not d:
            print(f"  {label:10s} MISSING")
            continue
        pct = 100 * d["unscored"] / d["n_items"]
        flag = "" if pct < 5 else "   <-- TOO HIGH, do not trust this row"
        print(f"  {label:10s} unscored={d['unscored']:4d}/{d['n_items']} ({pct:.1f}%){flag}")


if __name__ == "__main__":
    main()
