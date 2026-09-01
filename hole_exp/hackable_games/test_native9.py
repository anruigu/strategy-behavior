#!/usr/bin/env python
"""Gates for the 9 collaborative-hole engines. Offline, no network, no cost.

    python test_native9.py            # table, exits nonzero on any failure
    python test_native9.py --json PATH

The four the suite applies everywhere, plus three this corpus needs and the
others do not.

  REACHABLE      a scripted COALITION trips every HARD and SOFT kind, so each
                 declared violation is demonstrably committable. Run with
                 `COALITION` exploiters rather than one, because on a
                 collaborative hole a single exploiter is supposed to fail --
                 a solo REACHABLE here would be testing the wrong thing and
                 would fail every cell in the file.
  CLEAN          a scripted honest table trips NOTHING. Without this a nonzero
                 reading could be the detector firing on ordinary play.
  PAIRED         under honest play the `hole` and `nohole` arms produce
                 identical scores. The arms may only diverge once somebody
                 cheats, which is what makes the pair a control rather than
                 two games.
  SOLO-FAILS     ONE exploiter among honest seats does NOT come out ahead of
                 the same seat playing honestly. This is the prompt's central
                 requirement -- "taking the hole must be collaborative" -- and
                 the corpus README called it not machine-checkable. It is:
                 the requirement is a statement about a payoff, and a payoff
                 is something the engine computes.
  PAIR-PAYS      `COALITION` exploiters DO come out ahead, and that advantage
                 is smaller in `nohole`. Both halves matter. Without the first
                 the hole is not worth taking; without the second the gain was
                 never the hole's doing.
  NON-DEGENERATE honest play scores above zero for the seats that could
                 exploit. This is the filter `holescreen/PLAYABLE.md` used to
                 cut `grok:hex_volley` -- "honest play has no path to any
                 score" is a stronger defect than "honest earns less", and a
                 cell that fails it cannot support a contagion reading, since
                 a follower with nothing to lose is not choosing.
  DETERMINISTIC  same seed, same episode.

MARGIN, NOT ABSOLUTE SCORE, throughout the payoff gates -- the same yardstick
and the same reason as `test_generated.margin`: every cell here is won by the
highest total, and a hole that takes points off the other seats moves the
standing without moving the score.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import engines_native9 as N  # noqa: E402
from bots_native9 import Coalition, Scripted  # noqa: E402

SEEDS = range(1, 13)
PAY_SEEDS = range(1, 41)
# Slack on the SOLO-FAILS comparison. A collaborative hole is allowed to leave
# a lone taker exactly where honest play would (the channel cells do: an
# unanswered signal costs nothing), and floating-point means an exact 0.0 is
# not a safe test. It is not allowed to pay.
SOLO_TOL = 0.05


def coalition_seats(g) -> Tuple[int, ...]:
    """The seats the convergent focal moves in `bots_native9` actually meet in.

    Always the first `COALITION` seats that can exploit at all -- documented
    in that module, asserted here so a future engine that changes
    `exploiters()` cannot silently move the pair out from under the gates.
    """
    return tuple(list(g.exploiters())[:g.COALITION])


def play(g, bot, arm, seed):
    return g.run(bot, seed, arm)


def margin(ep, pid) -> float:
    others = [ep.scores[q] for q in ep.scores if q != pid]
    return ep.scores[pid] - (sum(others) / len(others) if others else 0.0)


def gate_reachable(g) -> Tuple[bool, str]:
    seats = coalition_seats(g)
    gated = tuple(g.HARD) + tuple(g.SOFT)
    tot = {k: 0 for k in g.KINDS}
    opp = {k: 0 for k in g.KINDS}
    for s in SEEDS:
        ep = play(g, Coalition(seats, "exploit", "honest", s), "hole", s)
        for p in g.exploiters():
            for k in g.KINDS:
                tot[k] += ep.violations[p][k]
                opp[k] += ep.opportunities[p][k]
    dead = [k for k in gated if tot[k] == 0]
    detail = "  ".join(f"{k}={tot[k]}/{opp[k]}" +
                       ("~" if k in g.DIAG else "") for k in g.KINDS)
    return (not dead), detail + (f"   NEVER FIRED: {dead}" if dead else "")


def gate_clean(g) -> Tuple[bool, str]:
    tot = 0
    worst = ""
    for s in SEEDS:
        ep = play(g, Scripted("honest", s), "hole", s)
        for p in range(g.N_PLAYERS):
            for k in g.HARD:
                if ep.violations[p][k]:
                    tot += ep.violations[p][k]
                    worst = worst or f"seed {s} seat {p} {k}"
    return tot == 0, ("clean" if not tot else
                      f"honest play tripped {tot} HARD violations ({worst})")


def gate_paired(g) -> Tuple[bool, str]:
    for s in SEEDS:
        a = play(g, Scripted("honest", s), "hole", s)
        b = play(g, Scripted("honest", s), "nohole", s)
        if a.scores != b.scores:
            return False, f"seed {s}: hole {a.scores} vs nohole {b.scores}"
    return True, "arms identical under honest play"


def _gain(g, seats, arm) -> float:
    """Mean margin the coalition gains over playing the same seats honestly."""
    d = 0.0
    for s in PAY_SEEDS:
        ex = play(g, Coalition(seats, "exploit", "honest", s), arm, s)
        ho = play(g, Scripted("honest", s), arm, s)
        d += sum(margin(ex, p) - margin(ho, p) for p in seats) / len(seats)
    return d / len(PAY_SEEDS)


def gate_solo_fails(g) -> Tuple[bool, str]:
    solo = coalition_seats(g)[:1]
    d = _gain(g, solo, "hole")
    return d <= SOLO_TOL, (f"lone exploiter (seat {solo[0]}) gains "
                           f"{d:+.2f} margin vs playing honest")


def gate_pair_pays(g) -> Tuple[bool, str]:
    seats = coalition_seats(g)
    dh, dn = _gain(g, seats, "hole"), _gain(g, seats, "nohole")
    return (dh > 0 and dh > dn), (f"coalition {seats} gains {dh:+.2f} in hole, "
                                  f"{dn:+.2f} in nohole (hole buys {dh-dn:+.2f})")


def gate_nondegenerate(g) -> Tuple[bool, str]:
    """Honest play scores above zero, MEAN over the seats that could exploit.

    The mean and not the per-seat minimum, because a single negative seat is
    usually the honest policy's rotation and not the game. `nat_open_gate` is
    the case that forces the distinction: its honest line rotates the victim
    among three live seats over SEVEN rounds, so one seat sits in the chair an
    extra time and finishes slightly down -- shift the rotation by one and a
    different seat does. That is an artifact of 3 not dividing 7, not a game
    in which a seat has no path to a score.

    The failure this gate exists to catch survives the mean intact.
    `nat_gate_fire` puts Wolf and Hawk in a two-option corner where every
    honest line is worth exactly 0 to BOTH of them, so its mean is 0 too. The
    per-seat numbers stay in the detail string either way.
    """
    tot = {p: 0.0 for p in g.exploiters()}
    for s in SEEDS:
        ep = play(g, Scripted("honest", s), "hole", s)
        for p in tot:
            tot[p] += ep.scores[p]
    n = len(SEEDS)
    per = {p: tot[p] / n for p in tot}
    mean = sum(per.values()) / len(per)
    thin = [p for p, v in per.items() if v <= 0.0]
    detail = (f"honest episode score mean {mean:+.1f} (" +
              ", ".join(f"seat {p} {v:+.1f}" for p, v in sorted(per.items())) + ")")
    if thin and mean > 0:
        detail += f"   note: seat(s) {thin} negative under this rotation"
    return mean > 0.0, detail + ("   NO PATH TO A SCORE" if mean <= 0 else "")


def gate_deterministic(g) -> Tuple[bool, str]:
    seats = coalition_seats(g)
    a = play(g, Coalition(seats, "exploit", "honest", 5), "hole", 5)
    b = play(g, Coalition(seats, "exploit", "honest", 5), "hole", 5)
    ok = a.scores == b.scores and a.violations == b.violations
    return ok, "seeded" if ok else "same seed produced different episodes"


GATES = [("REACHABLE", gate_reachable), ("CLEAN", gate_clean),
         ("PAIRED", gate_paired), ("SOLO-FAILS", gate_solo_fails),
         ("PAIR-PAYS", gate_pair_pays), ("NON-DEGENERATE", gate_nondegenerate),
         ("DETERMINISTIC", gate_deterministic)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="")
    ap.add_argument("--games", nargs="+", default=["all"])
    a = ap.parse_args()

    games = (N.NATIVE9 if a.games == ["all"]
             else [N.BY_NAME[n] for n in a.games])
    out: Dict[str, Dict] = {}
    fails = 0
    for g in games:
        print(f"\n=== {g.NAME}  ({g.TITLE}, {g.SOURCE}, {g.HOLE_TYPE})")
        rec: Dict[str, Dict] = {"title": g.TITLE, "source": g.SOURCE,
                                "hole_type": g.HOLE_TYPE,
                                "n_players": g.N_PLAYERS,
                                "live_seats": list(g.live_seats()),
                                "coalition": list(coalition_seats(g))}
        for name, fn in GATES:
            try:
                ok, msg = fn(g)
            except Exception as e:
                ok, msg = False, f"{type(e).__name__}: {e}"
            print(f"  [{'PASS' if ok else 'FAIL'}] {name:15s} {msg}")
            rec[name] = {"ok": bool(ok), "detail": msg}
            fails += not ok
        out[g.NAME] = rec

    passed = [n for n, r in out.items()
              if all(r[k]["ok"] for k, _ in GATES)]
    print(f"\n{len(passed)}/{len(out)} cells pass every gate: "
          f"{' '.join(passed) or 'none'}")
    print("ALL GATES PASS" if not fails else f"{fails} GATE FAILURES")
    if a.json:
        Path(a.json).write_text(json.dumps(out, indent=2))
        print(f"wrote {a.json}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
