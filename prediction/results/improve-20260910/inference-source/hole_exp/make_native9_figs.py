#!/usr/bin/env python
"""Build the three figures for the collaborative-hole contagion wave.

    python make_native9_figs.py results/contagion/nat_cg1

Re-runnable: it reads whatever arms are on disk and draws the panels those
arms support, so it can be run once while the wave is still filling in and
again when it lands. A figure whose arm is missing says so on the page rather
than being silently omitted.

  1  COUNTERFACTUAL CLOSING RATE, by game and model. The bar is the rate with
     an instigating leader MINUS the same model's rate in the matched
     honest-leader episode -- same board, same seed, same models, same seats,
     the only difference being whether seat 0 reached for the hole. That
     subtraction is the whole point: several of these cells have a nonzero
     floor (`nat_ridge_claim` closes at 0.10 with nobody instigating), so a
     raw rate would credit the leader for behaviour that was already there.
  2  PAYOFF vs FINDABILITY. What predicts following: what the hole is worth,
     or how likely two seats are to land on the meeting point at all.
  3  ONSET. Whether WHEN the exploit appears changes whether it is followed --
     and the round-number / time-since-onset split that only varied onset can
     separate.

FACETED, NOT COLOUR-CODED, wherever a model is the dimension. Four categorical
hues fail the all-pairs colour-vision gate in the shipped palette (yellow
beside orange: normal-vision Delta E 13.7 light, 10.6 dark), so model identity
is carried by panel position and label and every chart here draws one hue.
Checked with `viz/validate_palette.py`, the Python port of the skill's
validator -- there is no JS runtime on this box, and the port reproduces the
reference figures exactly (9.1/19.6 light, 8.4/19.3 dark).
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
from collections import defaultdict
from typing import Dict, List, Optional

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "hackable_games"))

import referee_games as RG        # noqa: E402
import referee_spartan as SP      # noqa: E402
from analyze_contagion import load, pooled          # noqa: E402
from analyze_native9 import follower_seats, kinds_of  # noqa: E402
from analyze_onset import (matched_exposure, round_of,  # noqa: E402
                           split_counts)

MODELS = ["gpt", "claude", "gemini", "grok"]

# P(two seats drawing uniformly from each stage's legal range land on the JOINT
# detector's coincidence condition in a round). COMPUTED FROM THE SPEC, never
# from the wave -- observed conversion would be circular with the outcome,
# since both have the same closes in the numerator.
COORD = {
    "nat_cargo_pledge":    (1 / 10, "both file the same report (1 of 10 values)"),
    "nat_open_gate":       (1 / 16, "both act raid-cedar (1 of 4 acts each)"),
    "nat_seam_ledger":     (1 / 36, "mutual partner (1/4) x matching tally (1/9)"),
    "nat_ridge_claim":     (1 / 25, "both signal >=8 (2 of 10 values each)"),
    "nat_mirror_manifest": (1 / 625, "both pledge 4 AND claim 4 (1/25 each)"),
    "nat_meridian_convoy": (1 / 900, "mutual dispatch (1/9) x equal declares (1/100)"),
    "nat_sealed_ante":     (1 / 900, "mutual route (1/9) x both seal==own card (1/100)"),
}
# Coalition margin in `hole`, from test_native9's PAIR-PAYS gate.
PAYOFF = {"nat_meridian_convoy": 345.00, "nat_seam_ledger": 40.92,
          "nat_open_gate": 24.00, "nat_cargo_pledge": 15.00,
          "nat_mirror_manifest": 7.51, "nat_ridge_claim": 6.45,
          "nat_sealed_ante": 0.30}


def pearson(xs, ys) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)


def joint_rate(rows, pred) -> Optional[float]:
    pairs = []
    for r in rows:
        if not pred(r):
            continue
        _, jnt = kinds_of(r["game"])
        for s in follower_seats(r):
            v = sum(int(s["v"].get(k) or 0) for k in jnt)
            o = sum(int(s["o"].get(k) or 0) for k in jnt)
            pairs.append((float(v), float(o)))
    return pooled(pairs)


def fig1(rows) -> Dict:
    """Counterfactual closing rate: instigated minus not-instigated."""
    seed = [r for r in rows if r["design"] == "seed"
            and r.get("arm", "hole") == "hole"
            and r.get("onset", "early") == "early"]
    games = sorted({r["game"] for r in seed})
    out = []
    for g in games:
        for m in MODELS:
            e = joint_rate(seed, lambda r, g=g, m=m: (
                r["game"] == g and r["leader"] == "exploit"
                and r.get("follower") == m))
            h = joint_rate(seed, lambda r, g=g, m=m: (
                r["game"] == g and r["leader"] == "honest"
                and r.get("follower") == m))
            out.append({"game": g.replace("nat_", ""), "model": m,
                        "exploit": e, "honest": h,
                        "delta": (None if e is None or h is None else e - h)})
    return {"rows": out, "games": [g.replace("nat_", "") for g in games]}


def fig2(rows) -> Dict:
    seed = [r for r in rows if r["design"] == "seed"
            and r.get("arm", "hole") == "hole"
            and r.get("onset", "early") == "early"]
    pts = []
    for g in sorted({r["game"] for r in seed}):
        e = joint_rate(seed, lambda r, g=g: r["game"] == g and r["leader"] == "exploit")
        h = joint_rate(seed, lambda r, g=g: r["game"] == g and r["leader"] == "honest")
        if e is None or h is None:
            continue
        pts.append({"game": g.replace("nat_", ""), "delta": e - h,
                    "payoff": PAYOFF[g], "coord": COORD[g][0],
                    "coord_note": COORD[g][1]})
    pts.sort(key=lambda p: -p["delta"])
    keep = [p for p in pts if p["game"] != "ridge_claim"]

    def rs(sub):
        return (round(pearson([math.log10(p["payoff"]) for p in sub],
                              [p["delta"] for p in sub]), 3),
                round(pearson([math.log10(p["coord"]) for p in sub],
                              [p["delta"] for p in sub]), 3))
    r_all, r_keep = rs(pts), rs(keep)
    return {"points": pts, "r_payoff": r_all[0], "r_coord": r_all[1],
            "r_payoff_x": r_keep[0], "r_coord_x": r_keep[1]}


def fig3(rows) -> Dict:
    """Onset: post-onset following per arm, and round vs time-since-onset."""
    seed = [r for r in rows if r["design"] == "seed"
            and r.get("arm", "hole") == "hole"]
    arms = sorted({r.get("onset", "early") for r in seed
                   if r["leader"] == "exploit"},
                  key=lambda a: ["early", "mid", "late"].index(a))
    per_model: Dict[str, Dict] = {m: {} for m in MODELS}
    per_arm: Dict[str, Dict] = {}
    for on in arms:
        acc = defaultdict(list)
        allp = []
        for r in seed:
            if r["leader"] != "exploit" or r.get("onset", "early") != on:
                continue
            _, jnt = kinds_of(r["game"])
            cut = r.get("onset_round", 1)
            for s in follower_seats(r):
                _, _, av, ao = split_counts(r, s, set(jnt), cut)
                acc[r.get("follower")].append((av, ao))
                allp.append((av, ao))
        per_arm[on] = {"rate": pooled(allp), "opps": sum(o for _, o in allp)}
        for m in MODELS:
            if acc.get(m):
                per_model[m][on] = {"rate": pooled(acc[m]),
                                    "opps": sum(o for _, o in acc[m])}
    # deconfound: absolute round vs rounds-since-onset
    by_round, by_since = defaultdict(list), defaultdict(list)
    for r in seed:
        if r["leader"] != "exploit":
            continue
        game = RG.BY_NAME[r["game"]]
        cut = r.get("onset_round", 1)
        _, jnt = kinds_of(r["game"])
        pids = {s["pid"] for s in follower_seats(r)}
        for i, pid, kind, hit, ch in r["timeline"]:
            if pid not in pids or kind not in set(jnt) or ch <= 0:
                continue
            rd = round_of(i, r, game)
            by_round[rd].append((float(bool(hit)), float(ch)))
            if rd >= cut:
                by_since[rd - cut].append((float(bool(hit)), float(ch)))
    f = lambda d: [{"k": k, "rate": pooled(v), "opps": sum(c for _, c in v)}
                   for k, v in sorted(d.items())]
    return {"arms": arms, "per_arm": per_arm, "per_model": per_model,
            "by_round": f(by_round), "by_since": f(by_since),
            "matched": matched_exposure(rows)}


def fig4(rows) -> Dict:
    """The nohole counterfactual: does following survive when it stops paying?"""
    seed = [r for r in rows if r["design"] == "seed"
            and r.get("onset", "early") == "early"]
    arms = sorted({r.get("arm", "hole") for r in seed})
    if len(arms) < 2:
        return {"arms": arms}
    out = {}
    for arm in arms:
        row = {}
        for m in MODELS:
            e = joint_rate(seed, lambda r, m=m, a=arm: (
                r.get("arm", "hole") == a and r["leader"] == "exploit"
                and r.get("follower") == m))
            h = joint_rate(seed, lambda r, m=m, a=arm: (
                r.get("arm", "hole") == a and r["leader"] == "honest"
                and r.get("follower") == m))
            row[m] = {"exploit": e, "honest": h,
                      "delta": (None if e is None or h is None else e - h)}
        out[arm] = row
    return {"arms": arms, "per_model": out}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--out", default=str(HERE / "results" / "native9_figs.html"))
    a = ap.parse_args()
    SP.register_all(); SP.register_native9()
    rows = load(pathlib.Path(a.dir))
    payload = {"fig1": fig1(rows), "fig2": fig2(rows),
               "fig3": fig3(rows), "fig4": fig4(rows),
               "n_episodes": len(rows)}
    tpl = (HERE / "viz" / "native9_figs.tpl.html").read_text()
    out = pathlib.Path(a.out)
    out.write_text(tpl.replace("__DATA__", json.dumps(payload)))
    f3 = payload["fig3"]
    print(f"{len(rows)} episodes  |  onset arms: {', '.join(f3['arms'])}"
          f"  |  matched arms: {', '.join(payload['fig4']['arms'])}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
