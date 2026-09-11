#!/usr/bin/env python3
"""Read the A and B sweeps and print the two contrasts they were built for.

    python analyze_think4_evals.py

ERROR BARS ARE OVER TRAINING SEEDS, NOT EPISODES. Pooling the 16 episode seeds
of one checkpoint would give a tight interval around one run's idiosyncrasy --
which is exactly how `0826-endgame-by-opponent.md` §4 came to report a sign
flip that three seeds then contradicted (`0830-endgame-summary.md` §1). Each
checkpoint collapses to one number first; the spread is across checkpoints.

A's STATISTIC IS DISTANCE FROM THE END, not the absolute index. Those are the
same number at N=10 and different everywhere else, and the difference IS the
experiment:

    learned the STRUCTURE   distance-from-end flat in N; absolute index rises
    memorised a POSITION    absolute index flat in N; distance-from-end rises

Reporting only the absolute index would make a structure-learner look like it
drifted, and reporting only the distance would make a memoriser look like it
drifted. Both are printed, and the slope of each against N is the readout.
"""
from __future__ import annotations

import collections
import json
import math
import pathlib
import statistics as st

HERE = pathlib.Path(__file__).resolve().parent
RES = HERE / "results" / "think4_evals"


def load(name: str) -> list:
    p = RES / name
    if not p.exists():
        return []
    return [json.loads(l) for l in p.open() if l.strip()]


def mean_sd(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None, None, 0
    if len(xs) == 1:
        return xs[0], None, 1
    return st.mean(xs), st.stdev(xs) / math.sqrt(len(xs)), len(xs)


def fmt(m, se, n):
    if m is None:
        return "     --   "
    if se is None:
        return f"{m:6.2f} (n=1)"
    return f"{m:6.2f}±{se:.2f}"


def slope(xs, ys):
    """Least-squares slope of y on x; None if degenerate."""
    pts = [(x, y) for x, y in zip(xs, ys) if y is not None]
    if len(pts) < 2:
        return None
    mx = st.mean([p[0] for p in pts]); my = st.mean([p[1] for p in pts])
    den = sum((p[0] - mx) ** 2 for p in pts)
    return None if den == 0 else sum((p[0] - mx) * (p[1] - my) for p in pts) / den


# ---------------------------------------------------------------- A
def analyse_a(rows: list) -> None:
    print("=" * 78)
    print("A -- does the policy find 'the last round', or 'round ten'?")
    print("=" * 78)
    if not rows:
        print("no rows yet\n"); return

    # The gate first. Everything below is void if the lengths did not separate.
    by_n = collections.defaultdict(list)
    for r in rows:
        by_n[r["num_rounds"]].append(r["n_decisions"] or 0)
    print("length gate -- mean decisions per episode:")
    for n in sorted(by_n):
        print(f"   N={n:3d} -> {st.mean(by_n[n]):5.2f}  (n={len(by_n[n])})")
    if len({round(st.mean(v), 1) for v in by_n.values()}) < len(by_n):
        print("   ** LENGTHS DID NOT SEPARATE -- stop reading here **\n"); return

    # per (arm, train_seed, N): the checkpoint's own mean, then spread over seeds
    per = collections.defaultdict(list)
    for r in rows:
        if r["first_defect_index"] is None:
            continue
        # An `_inf` arm scored WITH the horizon visible is a transfer test,
        # not the control -- keep the two apart rather than averaging them.
        per[(f'{r["arm"]}{"" if r.get("horizon","finite") == ("infinite" if r["arm"].endswith("/inf") else "finite") else " [off-cond]"}',
             r["train_seed"], r["num_rounds"])].append(r["first_defect_index"])
    ck = {k: st.mean(v) for k, v in per.items()}

    # how often the policy defected at all, since "never defected" is dropped above
    def key(r):
        want = "infinite" if r["arm"].endswith("/inf") else "finite"
        off = "" if r.get("horizon", "finite") == want else " [off-cond]"
        return (r["arm"] + off, r["num_rounds"])

    seen = collections.Counter(key(r) for r in rows)
    defd = collections.Counter(key(r) for r in rows
                               if r["first_defect_index"] is not None)

    arms = sorted({k[0] for k in ck})
    lens = sorted({k[2] for k in ck})
    for stat, label in (("abs", "absolute index of first defection"),
                        ("end", "rounds BEFORE the end (N-1 - index)")):
        print(f"\n{label}")
        print(f"{'arm':13s}" + "".join(f"   N={n:<10d}" for n in lens) + "  slope")
        for arm in arms:
            cells, means = [], []
            for n in lens:
                vals = [ck[(arm, s, n)] for (a, s, nn) in ck
                        if a == arm and nn == n]
                if stat == "end":
                    vals = [n - 1 - v for v in vals]
                m, se, k = mean_sd(vals)
                cells.append(fmt(m, se, k)); means.append(m)
            sl = slope(lens, means)
            print(f"{arm:13s}" + "".join(f"  {c:>12s}" for c in cells) +
                  ("  " + (f"{sl:+.2f}" if sl is not None else "  --")))
        if stat == "abs":
            print("   slope +1 = tracks the true final round;  0 = fixed position")
        else:
            print("   slope 0 = tracks the true final round;  -1 = fixed position")

    print(f"\nfraction of episodes with any defection")
    print(f"{'arm':13s}" + "".join(f"   N={n:<10d}" for n in lens))
    for arm in arms:
        print(f"{arm:13s}" + "".join(
            f"  {defd[(arm,n)]/seen[(arm,n)]:12.2f}" if seen[(arm, n)] else
            f"  {'--':>12s}" for n in lens))
    print("\nNOTE the `inf` arm is the negative control: the horizon is scrubbed")
    print("from its prompts, so it CANNOT know N and its timing must not move")
    print("with it. A slope there is a measurement artefact, not a result.\n")


# ---------------------------------------------------------------- B
def analyse_b(rows: list) -> None:
    print("=" * 78)
    print("B -- did it learn the OPPONENT, or the GAME?")
    print("=" * 78)
    if not rows:
        print("no rows yet\n"); return

    for metric in ("exploit_rate", "first_defect_index"):
        per = collections.defaultdict(list)
        for r in rows:
            v = r.get(metric)
            if v is not None:
                per[(r["arm"], r["train_seed"], r["plays"])].append(v)
        ck = {k: st.mean(v) for k, v in per.items()}
        arms = sorted({k[0] for k in ck})
        print(f"\n{metric}")
        print(f"{'arm (trained vs)':18s} {'plays grim':>14s} {'plays tft':>14s}"
              f" {'off - on':>12s}")
        for arm in arms:
            row = {}
            for plays in ("grim", "tft"):
                row[plays] = mean_sd([ck[(arm, s, plays)] for (a, s, p) in ck
                                      if a == arm and p == plays])
            trained = arm.split("/")[0]
            other = "tft" if trained == "grim" else "grim"
            d = (row[other][0] - row[trained][0]
                 if row[other][0] is not None and row[trained][0] is not None
                 else None)
            print(f"{arm:18s} {fmt(*row['grim']):>14s} {fmt(*row['tft']):>14s}"
                  f" {d:+12.3f}" if d is not None else
                  f"{arm:18s} {fmt(*row['grim']):>14s} {fmt(*row['tft']):>14s}"
                  f" {'--':>12s}")
        print("   'off - on' near 0 = the split changed the GRADIENT, not the")
        print("   learned policy. Large = the arms learned different policies.")

    inv = [r["invalid_rate"] for r in rows if r.get("invalid_rate") is not None]
    if inv:
        print(f"\ninvalid_rate across the sweep: mean {st.mean(inv):.3f}, "
              f"max {max(inv):.3f}")
        print("   HANDOFF-think4.md §7: above ~0.25 the decisions are ipd_lib's")
        print("   fallback move and neither contrast above means anything.\n")


def main() -> int:
    analyse_a(load("A_endgame_length.jsonl"))
    analyse_b(load("B_crossplay.jsonl"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
