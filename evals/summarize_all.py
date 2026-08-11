#!/usr/bin/env python
"""Consolidate every transfer-eval measurement into one table.

    summarize_all.py

Pulls from the three harnesses' own output locations:
  reasoning battery  math-evaluation-harness/data/eval/<arm>/<ds>/*metrics*.json
  MASK               evals/runs/<arm>/csv_data/metrics/all_results.json
  reward hacks       evals/reward-hacks/results/<arm>.json

%C (belief-elicitation failure) is reported next to every MASK number because a
MASK score is only interpretable against it: a model that never states a belief
cannot be caught contradicting one, so incoherence reads as honesty. mathRL-192
scored 5.6% dishonest with 74.4% %C -- that arm had degenerated into token soup
and its "honesty" was an artifact.
"""
import glob
import json
import os

import pandas as pd

MR = "/workspace/allie/spiral/evals/benchmarks/math-evaluation-harness/data/eval"
KR = "/workspace/allie/evals/runs"
RH = "/workspace/allie/evals/reward-hacks/results"
DATASETS = ["math500", "aime24", "aime25", "olympiadbench", "amc23", "minerva_math"]

# (label, reasoning-arm, mask-arm, reward-hacks-arm)
ARMS = [
    ("base",         "base",           "base-redo",           "rh-base"),
    ("kuhn-64",      "kuhn-step064",   "kuhn-mask-step064",   None),
    ("kuhn-128",     "kuhn-step128",   "kuhn-mask-step128",   None),
    ("kuhn-256",     "kuhn-step256",   "spiral-kuhn-step256", None),
    ("kuhn-400",     "kuhn-step400",   "kuhn-step400",        "rh-kuhn400"),
    ("mathRL-64",    "mathrl-step064", "mathrl-step064",      "rh-mathrl064"),
    ("mathRL-192*",  "mathrl-step192", "mathrl-step192",      None),
]


def reasoning(arm):
    if not arm:
        return None
    accs = []
    for ds in DATASETS:
        f = glob.glob(f"{MR}/{arm}/{ds}/*metrics*.json")
        if f:
            accs.append(json.load(open(f[0]))["acc"])
    return sum(accs) / len(accs) if len(accs) == len(DATASETS) else None


def mask(arm):
    if not arm:
        return None, None
    p = f"{KR}/{arm}/csv_data/metrics/all_results.json"
    if not os.path.exists(p):
        return None, None
    d = json.load(open(p))
    num = den = 0
    for _, models in d.items():
        for _, v in models.items():
            n = v.get("total_responses", 0)
            num += v.get("unhonest_1", 0) / 100 * n
            den += n
    dis = 100 * num / den if den else None

    tot = c = 0
    for f in glob.glob(f"{KR}/{arm}/csv_data/evaluated/*.csv"):
        df = pd.read_csv(f)
        cols = [x for x in df.columns
                if x.startswith("eval(") and x.endswith("_extracted") and "belief_elicit" in x]
        for col in cols:
            v = df[col].astype(str)
            tot += v.isin(["A", "B", "C", "D"]).sum()
            c += (v == "C").sum()
    return dis, (100 * c / tot if tot else None)


def hacks(arm):
    if not arm:
        return None
    p = f"{RH}/{arm}.json"
    return json.load(open(p)).get("hack_rate") if os.path.exists(p) else None


def main():
    fmt = lambda v, s="%.1f": (s % v) if v is not None else "--"
    print(f"{'arm':13s} {'reasoning':>10s} {'MASK dis%':>10s} {'%C':>7s} {'hack%':>7s}")
    print("-" * 52)
    for label, r_a, m_a, h_a in ARMS:
        r = reasoning(r_a)
        d, c = mask(m_a)
        h = hacks(h_a)
        print(f"{label:13s} {fmt(r):>10s} {fmt(d):>10s} {fmt(c):>7s} {fmt(h):>7s}")
    print()
    print("  * mathRL-192 degenerated (token soup off-distribution); its MASK number")
    print("    is an artifact of 74% belief-elicitation failure -- do not use.")
    print("  reasoning = mean acc over math500/aime24/aime25/olympiadbench/amc23/minerva_math")
    print("  MASK dis% = pooled dishonest rate, n=1000, judge openai/gpt-4.1, 0% judge loss")
    print("  hack%     = School of Reward Hacks, fraction judged to game the stated metric")


if __name__ == "__main__":
    main()
