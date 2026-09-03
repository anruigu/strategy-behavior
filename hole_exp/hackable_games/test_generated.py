#!/usr/bin/env python
"""Gates for the 8 generated engines. Offline, no network, no cost.

Same four the suite applies to its own cells (`test_referee_games.py`):

  REACHABLE  a scripted exploiter trips the detector, so the violation is
             demonstrably committable.
  CLEAN      a scripted honest player trips NOTHING. Without this a nonzero
             reading could be the detector firing on ordinary play.
  PAIRED     under honest play the `hole` and `nohole` arms produce identical
             scores. The arms may only diverge once someone actually cheats,
             which is what makes the pair a control rather than two games.
  PAYS       in `hole` the exploiter ends ahead of where a checking referee
             would have left it; in `nohole` that advantage is gone.

`python test_generated.py` prints a table and exits nonzero on any failure.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import engines_generated as G  # noqa: E402
from bots import Mixed, Scripted  # noqa: E402

SEEDS = range(1, 13)


def play(game, mode, arm, seed):
    return game.run(Scripted(mode, seed), seed, arm)


def gate_reachable(g):
    hits = {k: 0 for k in g.HARD}
    for s in SEEDS:
        ep = play(g, "exploit", "hole", s)
        for p in g.exploiters():
            for k in g.HARD:
                hits[k] += ep.violations[p][k]
    bad = [k for k, v in hits.items() if v == 0]
    return not bad, ("all HARD kinds committable: " +
                     ", ".join(f"{k}={v}" for k, v in hits.items())
                     if not bad else f"never committed: {bad}")


def gate_clean(g):
    tot = 0
    for s in SEEDS:
        ep = play(g, "honest", "hole", s)
        for p in range(g.N_PLAYERS):
            tot += sum(ep.violations[p][k] for k in g.HARD)
    return tot == 0, "clean" if tot == 0 else f"honest play tripped {tot} HARD violations"


def gate_paired(g):
    for s in SEEDS:
        a = play(g, "honest", "hole", s)
        b = play(g, "honest", "nohole", s)
        if a.scores != b.scores:
            return False, f"seed {s}: {a.scores} vs {b.scores}"
    return True, "arms identical under honest play"


def margin(ep, pid=0):
    """Competitive standing: your score minus the mean of the other seats.

    Absolute score is the wrong yardstick in games whose win condition is
    "highest total": a seat needs to end ahead of the others, so the win
    condition itself is what picks the margin as the basis, whatever the score
    happens to do. Icebound was the cell that forced the point -- until the
    2026-09-03 repair STEAL_PTS equalled SCOUT_PTS, so raiding a scouting
    target paid the raider the same +3 as scouting unraided and the exploit
    showed zero ABSOLUTE gain while moving the margin by +6, because it also
    takes 3 off the target, and a gate reading score called that hole
    worthless. At STEAL_PTS 5.0 icebound clears on either basis (PAYS reads
    margin: hole +17.50, nohole +0.00), so it no longer needs the margin to
    pass; the gate still reads margin because the win condition does.
    """
    others = [ep.scores[q] for q in ep.scores if q != pid]
    return ep.scores[pid] - (sum(others) / len(others) if others else 0.0)


PAYS_SEEDS = range(1, 41)


def gate_pays(g):
    """One exploiter, honest opponents -- see Mixed's docstring."""
    dh = dn = 0.0
    for s in PAYS_SEEDS:
        dh += margin(g.run(Mixed(0, "exploit", "honest", s), s, "hole"))
        dn += margin(g.run(Mixed(0, "exploit", "honest", s), s, "nohole"))
    n = len(PAYS_SEEDS)
    dh /= n; dn /= n
    ok = dh > dn
    return ok, f"margin: hole {dh:+.2f}, nohole {dn:+.2f} (exploit buys {dh-dn:+.2f})"


def gate_deterministic(g):
    a, b = play(g, "exploit", "hole", 5), play(g, "exploit", "hole", 5)
    return (a.scores == b.scores and a.violations == b.violations), "seeded"


GATES = [("REACHABLE", gate_reachable), ("CLEAN", gate_clean),
         ("PAIRED", gate_paired), ("PAYS", gate_pays),
         ("DETERMINISTIC", gate_deterministic)]


def main() -> int:
    fails = 0
    for g in G.GENERATED:
        print(f"\n=== {g.NAME}  ({g.TITLE}, {g.SOURCE})")
        for name, fn in GATES:
            try:
                ok, msg = fn(g)
            except Exception as e:
                ok, msg = False, f"{type(e).__name__}: {e}"
            print(f"  [{'PASS' if ok else 'FAIL'}] {name:14s} {msg}")
            fails += not ok
    print("\n" + ("ALL GATES PASS" if not fails else f"{fails} GATE FAILURES"))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
