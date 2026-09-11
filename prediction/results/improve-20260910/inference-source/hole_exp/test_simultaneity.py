#!/usr/bin/env python
"""Do the seats raid TOGETHER or in turn? The mechanism test for gen_icebound.

    python test_simultaneity.py [cell]

`rows.jsonl` carries only the FOCAL seat's counters, so it cannot answer this.
The traces can: `run_referee_spartan.trace_of` writes `violations` for EVERY
seat of every episode, which is exactly the joint distribution the rows throw
away.

THE HYPOTHESIS UNDER TEST. `gen_icebound` reads higher under independent
reflection than under shared reflection (+0.24 at R3). Proposed mechanism: a
raid into a raid costs the raider, so under ONE shared playbook all three seats
raid on the same turn, it does not pay, and the shared playbook learns to stop
-- while under independent playbooks the seats discover at different times, a
lone raider profits, and the behaviour persists.

That mechanism makes a prediction the rate curves cannot: the shared arm's
violations should be CONCENTRATED in episodes where every seat violates, and
the per-seat arm's should be SPREAD across episodes where only one does. If
instead both arms look alike in their joint structure, the rate gap needs a
different explanation and the tidy story is wrong.
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "hackable_games"))

import referee_games as RG   # noqa: E402
import referee_spartan as SP  # noqa: E402

BASE = HERE / "results" / "referee_spartan"
TAGS = {"shared": "ma_rivalry_shared", "per-seat": "ma_rivalry_perseat"}


def main() -> int:
    SP.register_all()
    SP.register_native9()
    cell = sys.argv[1] if len(sys.argv) > 1 else "gen_icebound"
    g = RG.BY_NAME[cell]
    kinds = list(g.HARD or ())
    print(f"{cell}: {g.N_PLAYERS} seats, HARD={kinds}\n")

    for arm, tag in TAGS.items():
        d = BASE / tag / "traces"
        if not d.is_dir():
            print(f"{arm}: no traces dir")
            continue
        files = sorted(d.glob(f"{cell}-*.json"))
        # by round: how many seats violated in each episode
        dist = collections.defaultdict(collections.Counter)
        for f in files:
            t = json.loads(f.read_text())
            rnd = t["round"]
            viol = t.get("violations") or {}
            n = 0
            for seat, kv in viol.items():
                if any((kv or {}).get(k, 0) for k in kinds):
                    n += 1
            dist[rnd][n] += 1
        print(f"--- {arm}  ({len(files)} episode traces)")
        print(f"    {'round':6s} " +
              " ".join(f"{k}-of-{g.N_PLAYERS}" for k in
                       range(g.N_PLAYERS + 1)) + "   mean seats")
        for rnd in sorted(dist):
            c = dist[rnd]
            tot = sum(c.values())
            mean = (sum(k * v for k, v in c.items()) / tot) if tot else 0.0
            cells_ = " ".join(f"{c.get(k, 0):8d}" for k in
                              range(g.N_PLAYERS + 1))
            print(f"    R{rnd:<5d} {cells_}   {mean:.2f}")
        print()

    print("READ IT LIKE THIS. Mass piling up on the all-seats column is")
    print("simultaneous exploitation; mass on the 1-of-N column is a lone")
    print("exploiter. The mechanism above predicts the shared arm sits further")
    print("right than the per-seat arm at R1-R3, and predicts nothing at R0,")
    print("where both arms play the identical empty-playbook episode.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
