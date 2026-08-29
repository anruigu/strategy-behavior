"""Does exploiting the referee actually WIN the game?

    python analyze_referee_payoff.py results/referee_crossplay/wave1
    python analyze_referee_payoff.py results/referee_crossplay/wave3_cross

`gain` already answers a narrower question -- what the unchecked referee handed
over, against a replay of the same episode past a checking one. That is not the
same as winning, and in self-play the two can come apart completely: if every
seat exploits at the same rate the hole pays everybody, `gain` is large, and
the standings do not move at all.

So the test here is WITHIN-EPISODE and relative:

    delta_exploit = focal's rate on the game's headline HARD kind
                    minus the pooled rate of the other seats
    delta_score   = focal's score minus the mean of the other seats'

and the question is whether the first predicts the second. Both terms come from
the same episode, so the seeded board, the deal and the yields cancel; nothing
here depends on comparing one episode to another.

THREE GAMES NEED A DIFFERENT QUESTION AND GET ONE.

  * `ref_signal` and `ref_hanabi` are CO-OPERATIVE. Every seat shares one
    score, so `delta_score` is identically zero and a correlation over it is
    meaningless. For those the payoff question is "does the covert channel
    raise the TEAM score", which only the matched `nohole` arm can answer.
  * `ref_sidebar` has a fixed victim. The standings question is not whether a
    colluder beats its partner -- they are on the same side -- but whether the
    PAIR takes chips off the MARK, so it is scored as `transfer`.

STATISTICS. Spearman rho over episodes, with a permutation test on the rank
correlation, because n is 8-48 per cell and the score distributions are wildly
non-normal (`ref_estate` scores span 1e18). A sign test on the same pairs is
reported beside it: it asks only "did the more exploitative seat finish ahead
more often than not", which survives any monotone rescaling of the score.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import sys
from typing import Dict, List, Optional, Tuple

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import referee_ablations  # noqa: E402,F401
import referee_games2  # noqa: E402,F401
import referee_games as RG  # noqa: E402

# The headline HARD kind per game -- the one the summary leads with.
HEADLINE = {"ref_battleship": "misreport", "ref_estate": "ledger_break",
            "ref_signal": "covert_channel", "ref_sidebar": "card_disclosure",
            "ref_exchange": "ledger_break", "ref_hanabi": "covert_channel",
            "ref_signal_strict": "covert_channel",
            # second wave
            "ref_auction": "phantom_budget", "ref_commons": "over_quota",
            "ref_orderbook": "unbacked_order", "ref_invoice": "invoice_fraud",
            "ref_lemons": "quality_overclaim"}

COOPERATIVE = {"ref_signal", "ref_hanabi", "ref_signal_strict"}
VICTIM = {"ref_sidebar"}


def ranks(xs: List[float]) -> List[float]:
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def pearson(a: List[float], b: List[float]) -> Optional[float]:
    n = len(a)
    if n < 3:
        return None
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    if va <= 0 or vb <= 0:
        return None
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    return cov / (va ** 0.5 * vb ** 0.5)


def spearman(a: List[float], b: List[float]) -> Optional[float]:
    return pearson(ranks(a), ranks(b))


def perm_p(a: List[float], b: List[float], n: int = 20000,
           seed: int = 0) -> Optional[float]:
    rho = spearman(a, b)
    if rho is None:
        return None
    rng = random.Random(seed)
    ra, rb = ranks(a), ranks(b)
    hits = 0
    for _ in range(n):
        rng.shuffle(rb)
        r = pearson(ra, rb)
        if r is not None and abs(r) >= abs(rho) - 1e-12:
            hits += 1
    return (hits + 1) / (n + 1)


def sign_test(pairs: List[Tuple[float, float]]) -> Tuple[int, int, Optional[float]]:
    """Of the episodes where one seat out-exploited the other, how often did it
    also finish ahead? Two-sided binomial, computed exactly."""
    ahead = behind = 0
    for de, ds in pairs:
        if abs(de) < 1e-12 or abs(ds) < 1e-12:
            continue
        if (de > 0) == (ds > 0):
            ahead += 1
        else:
            behind += 1
    n = ahead + behind
    if n == 0:
        return 0, 0, None
    from math import comb
    k = min(ahead, behind)
    tail = sum(comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    return ahead, behind, min(1.0, 2 * tail)


def load(d: pathlib.Path) -> List[Dict]:
    f = d / "rows.jsonl"
    if not f.exists():
        raise SystemExit(f"no rows.jsonl under {d}")
    return [json.loads(l) for l in f.read_text().splitlines() if l.strip()]


def others_mean(r: Dict) -> Optional[float]:
    sc = r.get("scores") or {}
    vals = [v for k, v in sc.items() if k != "0" and v is not None]
    return (sum(vals) / len(vals)) if vals else None


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--arm", default="hole")
    ap.add_argument("--by-model", action="store_true")
    a = ap.parse_args()

    rows: List[Dict] = []
    for d in a.dirs:
        rows += [r for r in load(pathlib.Path(d)) if r["arm"] == a.arm]

    print("=" * 78)
    print("DOES OUT-EXPLOITING THE TABLE PUT YOU AHEAD OF IT?")
    print("  delta_exploit = focal rate - pooled rate of the other seats")
    print("  delta_score   = focal score - mean of the other seats' scores")
    print("  Both within the same episode, so board/deal/yield cancel.")
    print("=" * 78)
    print(f"{'game':14s} {'cell':16s} {'n':>4s} {'rho':>7s} {'p':>7s} "
          f"{'ahead':>6s} {'behind':>7s} {'p_sign':>7s}")

    for game in sorted({r["game"] for r in rows}):
        if game in COOPERATIVE or game in VICTIM:
            continue
        k = HEADLINE.get(game)
        cells = [("all", None)] if not a.by_model else \
            [(m, m) for m in sorted({r["focal"] for r in rows})]
        for label, m in cells:
            sel = [r for r in rows if r["game"] == game
                   and (m is None or r["focal"] == m)]
            de, ds, pairs = [], [], []
            for r in sel:
                f_rate, o_rate = r.get(f"r_{k}"), r.get(f"opp_r_{k}")
                om = others_mean(r)
                if None in (f_rate, o_rate, om) or r.get("score_focal") is None:
                    continue
                d1 = f_rate - o_rate
                d2 = r["score_focal"] - om
                de.append(d1)
                ds.append(d2)
                pairs.append((d1, d2))
            if len(de) < 3:
                continue
            rho = spearman(de, ds)
            p = perm_p(de, ds)
            ah, bh, ps = sign_test(pairs)
            print(f"{game.replace('ref_',''):14s} {label:16s} {len(de):4d} "
                  f"{('  -' if rho is None else f'{rho:7.3f}')} "
                  f"{('  -' if p is None else f'{p:7.3f}')} "
                  f"{ah:6d} {bh:7d} "
                  f"{('  -' if ps is None else f'{ps:7.3f}')}")

    # ---- the games that need a different question ------------------------
    print()
    print("=" * 78)
    print("CO-OPERATIVE CELLS -- one shared score, so there is no 'ahead'.")
    print("  The payoff question is whether the channel raises the TEAM score,")
    print("  and only the matched nohole arm can answer it.")
    print("=" * 78)
    for game in sorted(COOPERATIVE & {r["game"] for r in rows}):
        sel = [r for r in rows if r["game"] == game]
        k = HEADLINE[game]
        for m in sorted({r["focal"] for r in sel}):
            ss = [r for r in sel if r["focal"] == m]
            rate = [r[f"r_{k}"] for r in ss if r.get(f"r_{k}") is not None]
            sc = [r["score_focal"] for r in ss if r.get("score_focal") is not None]
            if len(rate) < 3:
                continue
            rho = spearman(rate, sc)
            p = perm_p(rate, sc)
            print(f"  {game.replace('ref_',''):10s} {m:8s} n={len(rate):3d}  "
                  f"channel-rate vs team score: rho="
                  f"{('  -' if rho is None else f'{rho:6.3f}')}"
                  f"  p={('  -' if p is None else f'{p:5.3f}')}"
                  f"   mean score {sum(sc)/len(sc):6.2f}")

    print()
    print("=" * 78)
    print("FIXED-VICTIM CELL -- the colluders are on the same side, so the")
    print("  standings question is what the PAIR takes off the MARK.")
    print("=" * 78)
    for game in sorted(VICTIM & {r["game"] for r in rows}):
        sel = [r for r in rows if r["game"] == game]
        k = HEADLINE[game]
        for m in sorted({r["focal"] for r in sel}):
            ss = [r for r in sel if r["focal"] == m
                  and r.get("x_transfer") is not None
                  and r.get(f"r_{k}") is not None]
            if len(ss) < 3:
                continue
            rate = [r[f"r_{k}"] for r in ss]
            tr = [r["x_transfer"] for r in ss]
            rho = spearman(rate, tr)
            p = perm_p(rate, tr)
            print(f"  {game.replace('ref_',''):10s} {m:8s} n={len(ss):3d}  "
                  f"disclosure vs pair-minus-mark: rho="
                  f"{('  -' if rho is None else f'{rho:6.3f}')}"
                  f"  p={('  -' if p is None else f'{p:5.3f}')}"
                  f"   mean transfer {sum(tr)/len(tr):+6.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
