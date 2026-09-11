#!/usr/bin/env python
"""Per-seat OPPORTUNITY structure, scripted, offline, no API calls.

    python seat_denominators.py

Answers the question that made the 0901 prototype table untrustworthy: the
shared arm and the per-seat arm reported different opportunity counts, and
without knowing why, a rate difference between them could not be attributed to
the reflection scope.

The cause is not the reflection scope at all. `referee_spartan._row` records
the FOCAL seat's counters. The shared arm runs `focal=0` and emits one row per
episode; the per-seat arm emits one row per (episode, seat). So pooling all
per-seat rows against the shared arm compares a whole table to seat 0 -- and
the two disagree by however much the seats differ from each other, which is a
property of the CELL and is measurable here for nothing.

Read it as the denominator map for `analyze_rivalry_reflect.py`:

  seat 0 == every other seat   pooling is safe; the seats are interchangeable
  seat 0 != some other seat    ONLY seat 0 vs seat 0 is the ablation, and a
                               table-wide per-seat number is a different
                               quantity that must not be subtracted from a
                               shared one

Every seat plays the EXPLOIT policy here, deliberately: an honest table would
report zeros and say nothing about how the seats compare.

READ THESE AS A SYMMETRY CHECK, NOT AS DENOMINATORS. Opportunity counts are
ENDOGENOUS -- they depend on how the episode actually goes -- so the absolute
numbers here are the counts under scripted all-seats-exploit play and not the
counts a live wave will divide by. `ref_commons` is the demonstration: the
scripted exploiters blow the stock on the first turn, the episode ends, and
this file records 1 over_quota opportunity per seat per episode. A live
gemini-flash table plays on for six turns and the rows record 6. Same cell,
same code, six-fold difference in the denominator, because the exploit
SHORTENS the episode.

What survives that, and is the only thing claimed here, is the COMPARISON
ACROSS SEATS within a cell: whatever the episode length turns out to be, the
seats either face it alike or they do not.
"""
from __future__ import annotations

import collections
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "hackable_games"))

import referee_games as RG   # noqa: E402
import referee_spartan as SP  # noqa: E402
import payoff_audit as PA    # noqa: E402

CELLS = ["ref_invoice", "gen_harbor_customs", "gen_seven_seal",
         "ref_auction", "gen_frontline_depot", "ref_commons",
         "gen_icebound", "ref_orderbook", "ta_kuhn"]
STRATUM = {"ref_invoice": "non-rival", "gen_harbor_customs": "non-rival",
           "gen_seven_seal": "non-rival",
           "ref_auction": "partially rival",
           "gen_frontline_depot": "partially rival",
           "ref_commons": "partially rival",
           "gen_icebound": "anti-rival", "ref_orderbook": "anti-rival",
           "ta_kuhn": "anti-rival"}


def main() -> int:
    SP.register_all()
    SP.register_native9()
    verdicts = []
    for name in CELLS:
        g = RG.BY_NAME[name]
        seats = list(range(g.N_PLAYERS))
        # opps[kind][seat] summed over the seed block
        opps = collections.defaultdict(lambda: collections.defaultdict(int))
        for s in PA.SEEDS:
            ep = g.run(PA.mixed_ask(g, set(seats), s), s, "hole")
            for p in seats:
                for k in g.KINDS:
                    opps[k][p] += ep.opportunities[p][k]
        print(f"\n{name}  ({STRATUM[name]}, {g.N_PLAYERS} seats, "
              f"{len(PA.SEEDS)} episodes, all seats exploiting)")
        hard = set(g.HARD or ())
        any_asym = False
        for k in g.KINDS:
            row = [opps[k][p] for p in seats]
            if not any(row):
                continue
            tag = "HARD" if k in hard else "soft/diag"
            same = len(set(row)) == 1
            if k in hard and not same:
                any_asym = True
            print(f"   {k:28s} {tag:9s} " +
                  " ".join(f"p{p}={opps[k][p]:4d}" for p in seats) +
                  ("   symmetric" if same else "   *** ASYMMETRIC ***"))
        verdicts.append((name, any_asym))

    print("\n" + "=" * 72)
    print("VERDICT -- is seat 0 representative of the table, on HARD kinds?")
    print("=" * 72)
    for name, asym in verdicts:
        if asym:
            print(f"  {name:22s} NO  -- report seat 0 vs seat 0 only; a "
                  f"table-wide\n{'':26s}per-seat rate is a different quantity")
        else:
            print(f"  {name:22s} yes -- seats interchangeable, table-wide "
                  f"pooling is safe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
