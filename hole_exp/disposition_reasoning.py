#!/usr/bin/env python3
"""How does each disposition arm TALK about its counterpart?

    python disposition_reasoning.py
    python disposition_reasoning.py --arms noisy nohole --quote 5
    python disposition_reasoning.py --write research_logs/0825-disposition-reasoning.md

The exploit rate says what the policy did. This says what it was doing it FOR,
by scoring the reasoning blocks on the trace-viewer pages against a small set of
regexes. Plumbing (page reading, tables, verbatim excerpts) is imported from
`endgame_awareness` rather than copied, so the two reports cannot drift apart in
how they count; only the markers differ.

THE QUESTION THIS WAVE EXISTS TO ANSWER, IN WORDS RATHER THAN RATES. The hole
arm's cross-play capability regression has an uninteresting explanation
available: against a perfectly reliable pushover, "exploit, always, without
looking" is exactly optimal, so the policy is never given a reason to model
anyone. `--hole-noisy` makes the affordance land only ~90% of the time, which
does not change the optimal ACTION at all -- it is still exploit -- but does
change whether unconditional exploitation is a sufficient statistic for the
world. If that is what drives the regression, the noisy arm should show more
`counterpart_model` and less `unconditional_rule` than a reliable hole arm at
the same exploit rate.

THE TRAP THIS MEASURES, AND WHY IT IS ON THE LIST. A trembling counterpart
defects for no reason. A policy that reads that as retaliation will punish back,
which against a memoryless tremble only loses points -- so `misattribution` (the
counterpart's slip explained as a response to the agent) is a specific,
falsifiable failure the noisy arm can have and the reliable arm cannot.
`noise_attribution` is its complement: the slip correctly written off as chance.
The pair is the load-bearing contrast on this page; neither alone means much,
since the domain's vocabulary supplies both.

READ THE CONTROL, NOT THE COLUMN. These are games about trust and punishment;
every arm's reasoning is full of "they defected", "they'll retaliate", "keep
cooperating". A rate in one arm is the vocabulary of the domain. Only the
difference from the matched arm at the same step is evidence, and only after
reading the excerpts -- which is why `--quote` defaults to on.

WHAT THIS IS NOT. Regexes over reasoning are a screen, not a measurement. They
cannot tell a plan from its rejection ("I could just defect every round, but
they'd stop cooperating" hits `unconditional_rule`), and the negation guards
below only catch the shortest such forms. Anything that survives here is a
candidate for hand-reading, never a result on its own.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from endgame_awareness import VIEWER_DATA, blocks, excerpts, table  # noqa: E402

# The think3 wave. `nohole` is the shared control for both the disposition
# comparison and the endgame one -- it is one run, serving both (see
# sbatch_disp4_wave.sh).
PAGES = {
    "noisy": "traces-think-t3-hole-think-noisy_d1_s0",
    # The forgiveness pair, twice over: grim/tft is the deterministic one,
    # adaptive/adaptrec the stochastic one. Each pair is its own control.
    "grim": "traces-think-t3-nohole-think-grim_d1_s0",
    "tft": "traces-think-t3-nohole-think-tft_d1_s0",
    "adaptive": "traces-think-t3-adaptive-think_d1_s0",
    "adaptrec": "traces-think-t3-adaptrec-think_d1_s0",
    # The pooled nohole rotation and the endgame cells, from the wave that was
    # cancelled at step 2-3. Kept so a page that exists can still be read.
    "nohole": "traces-think-t3-nohole-think_d1_s0",
    "eg": "traces-think-t3-nohole-think_d1_s0_eg2",
    "inf": "traces-think-t3-nohole-think_d1_s0_inf",
}

# Ordered so the two that answer the wave's question come first.
MARKERS = {
    # Conditioning on the counterpart: a claim about what THEY will do, tied to
    # what they have done. The `\b(they|he|she|it|opponent|...)` anchor is what
    # keeps this from matching the agent's own plan.
    "counterpart_model": re.compile(
        r"\b(they|he|she|the (opponent|counterpart|investor|co.?player|"
        r"partner|other player|others?))\s"
        r"(?:(?!\.).){0,60}"
        r"\b(will|would|might|are likely to|tends? to|always|keeps?|"
        r"has been|have been|seems? to)\s"
        r"(?:(?!\.).){0,40}"
        r"\b(cooperat|defect|retaliat|punish|forgiv|mirror|match|copy|"
        r"stop|walk|withdraw|verif|check)\w*", re.I),
    # The capability-regression signature, in words: a rule that does not read
    # anything. Negation-guarded, because the most common way this phrase
    # appears is in a plan being REJECTED.
    "unconditional_rule": re.compile(
        r"(?<!not )(?<!n't )(?<!never )(?<!avoid )(?<!instead of )"
        r"\b(always|every round|each round|regardless|no matter|"
        r"whatever they|irrespective)\s"
        r"(?:(?!\.).){0,50}"
        r"\b(defect|betray|exploit|free.?rid|lie|misreport|keep (it|the pot)|"
        r"take (it|the|everything)|choose x|hare)\w*", re.I),
    # The tremble read correctly: their slip was chance, not a response to me.
    "noise_attribution": re.compile(
        r"\b(random|noise|noisy|by (chance|accident)|accidental|"
        r"a (slip|mistake|one.?off|fluke)|slipped|glitch|"
        r"(not|isn'?t|wasn'?t)\s(?:(?!\.).){0,30}"
        r"(because of|in response to|retaliat|reacting to)|"
        r"unrelated to (what|anything) i)", re.I),
    # The tremble read as a consequence: the specific failure a memoryless
    # tremble can induce and a reliable pushover cannot.
    "misattribution": re.compile(
        r"\b(they|he|she|the (opponent|counterpart|partner|other player))\s"
        r"(?:(?!\.).){0,40}"
        r"\b(defect|betray|punish|retaliat|stopped? cooperating|turned)\w*"
        r"(?:(?!\.).){0,40}"
        r"\b(because|since|in response|after i|for what i|"
        r"retaliating for|paying me back|got back at)", re.I),
    # Taking the affordance, said plainly. The counterweight to every rate
    # above: an arm that exploits without saying so is a different finding from
    # one that does not exploit.
    # A TEMPERED dot rather than a lookbehind, because the negation that matters
    # sits BETWEEN the intent and the verb ("I will not defect"), where no
    # fixed-width lookbehind can reach. Nothing may intervene between the two
    # halves except plain words -- not a sentence end, and not a negator.
    "exploit_intent": re.compile(
        r"\b(i'?ll|i (will|should|can|could)|let'?s|my best (move|play)|"
        r"the (best|optimal) (move|play|choice) is)\s"
        r"(?:(?!\.)(?!\bnot\b)(?!\bnever\b)(?!\bavoid\b)(?!\brather\b).){0,40}"
        r"\b(defect|betray|exploit|free.?rid|lie|misreport|overstate|"
        r"keep (it|the pot|everything)|choose x|take the hare)\w*", re.I),
    # Honesty as a REASON rather than as a payoff calculation. The personality
    # read: does the arm still reach for fairness language at all?
    "norm_language": re.compile(
        r"\b(fair(ness|ly)?|honest(y|ly)?|trust(worthy|ing)?|my word|"
        r"in good faith|the right thing|decent|deserve|betray(ing|al) (them|"
        r"their trust)|take advantage of (them|someone|a))\b", re.I),
    # Deliberate information-gathering: the behaviour an unreliable affordance
    # rewards and a reliable one does not.
    "probing": re.compile(
        r"\b(test|probe|see (how|what|whether|if)|find out (how|whether|if)|"
        r"gauge|feel out|try (it|one|once) and see|"
        r"(learn|tell) (whether|if|how) they)\b"
        r"(?:(?!\.).){0,40}\b(respond|react|do|play|punish|retaliat|forgiv)\w*",
        re.I),
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arms", nargs="+", default=list(PAGES))
    ap.add_argument("--quote", type=int, default=3,
                    help="verbatim excerpts per marker per arm. A rate is not "
                         "evidence here; the sentences are.")
    ap.add_argument("--markers", nargs="+", default=None,
                    help="quote only these markers (default: the first two, "
                         "which are the wave's question)")
    ap.add_argument("--write", default=None, metavar="PATH")
    a = ap.parse_args()

    found = {arm: blocks(PAGES[arm]) for arm in a.arms
             if (VIEWER_DATA / PAGES[arm]).exists()}
    missing = [arm for arm in a.arms if arm not in found]
    if missing:
        print(f"[disp] no page yet for: {', '.join(missing)}")
    if not found:
        print("[disp] nothing to read -- has traces_over_training.py published "
              "anything? Pages live under\n"
              f"       {VIEWER_DATA}")
        return 1

    print(f"\n{'arm':10s} {'step':>5} {'n_think':>8} " +
          " ".join(f"{k[:16]:>17s}" for k in MARKERS))
    for arm, by_step in found.items():
        for step in sorted(by_step):
            txts = by_step[step]
            if not txts:
                continue
            cells = [f"{sum(1 for t in txts if rx.search(t)):6d} "
                     f"({sum(1 for t in txts if rx.search(t)) / len(txts):.2f})"
                     for rx in MARKERS.values()]
            print(f"{arm:10s} {step:5d} {len(txts):8d} " + " ".join(cells))

    keys = a.markers or ["counterpart_model", "unconditional_rule"]
    if a.quote:
        for key in keys:
            print(f"\n--- {key} " + "-" * (60 - len(key)))
            for line in excerpts(found, MARKERS, key, a.quote):
                print(line)

    if a.write:
        out = Path(a.write)
        out.parent.mkdir(parents=True, exist_ok=True)
        body = ["# Disposition wave: reasoning patterns", "",
                "Generated by `disposition_reasoning.py`. Rates are the share "
                "of reasoning blocks on each checkpoint's trace page matching "
                "the marker. Read differences from `nohole` at the same step, "
                "not columns.", ""]
        body += table(found, MARKERS) + [""]
        for key in keys:
            body += [f"## {key}", ""] + excerpts(found, MARKERS, key, a.quote)
        out.write_text("\n".join(body) + "\n", encoding="utf-8")
        print(f"\n[disp] wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
