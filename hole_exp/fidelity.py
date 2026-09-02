#!/usr/bin/env python
"""Byte-level fingerprint of every registered cell, for safe refactoring.

    python fidelity.py --write baseline.json     # before touching an engine
    python fidelity.py --check baseline.json     # after

Extracting a payoff literal into a class attribute, or adding a rivalry term
that is inert at its default, is supposed to change NOTHING about the shipped
cell. "Supposed to" is not a test. This records, per cell x arm x policy x
seed: every seat's score, every violation count, and a hash of every prompt
string the engine emitted, in order.

The prompt hash is the part that matters and the part a scores-only check
misses. Payoffs are printed in the RULES text, so a refactor that silently
reformats `{self.HIT_PTS:.0f}` where the literal said `4` produces identical
scores against scripted bots and a different prompt for a model -- which
invalidates every trace on disk while every gate still passes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from typing import Dict

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "hackable_games"))

import referee_spartan as SP  # noqa: E402
import referee_games as RG  # noqa: E402
import exploit_curve as EC  # noqa: E402

SEEDS = range(1, 9)


def fingerprint(game, mode: str, arm: str, seed: int) -> Dict:
    h = hashlib.sha256()
    inner = EC.scripted(game, mode, seed)

    def ask(pid, phase, prompt):
        h.update(f"{pid}\x00{phase}\x00{prompt}\x00".encode())
        return inner(pid, phase, prompt)

    ep = game.run(ask, seed, arm)
    return {
        "scores": {str(p): round(float(v), 9) for p, v in sorted(ep.scores.items())},
        "violations": {str(p): dict(sorted(v.items()))
                       for p, v in sorted(ep.violations.items())},
        "opportunities": {str(p): dict(sorted(v.items()))
                          for p, v in sorted(ep.opportunities.items())},
        "invalid": {str(p): int(v) for p, v in sorted(ep.invalid.items())},
        "prompts": h.hexdigest()[:16],
    }


def snapshot() -> Dict:
    SP.register_all()
    SP.register_native9()
    out: Dict = {}
    for name in sorted(RG.BY_NAME):
        g = RG.BY_NAME[name]
        cell: Dict = {}
        for arm in ("hole", "nohole"):
            for mode in ("honest", "exploit"):
                for s in SEEDS:
                    cell[f"{arm}/{mode}/{s}"] = fingerprint(g, mode, arm, s)
        out[name] = cell
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", default="")
    ap.add_argument("--check", default="")
    a = ap.parse_args()
    snap = snapshot()
    if a.write:
        p = pathlib.Path(a.write)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(snap, indent=1, sort_keys=True))
        print(f"wrote {p}  ({len(snap)} cells, "
              f"{sum(len(v) for v in snap.values())} episodes)")
        return 0
    if a.check:
        old = json.loads(pathlib.Path(a.check).read_text())
        bad = []
        for cell in sorted(set(old) | set(snap)):
            if cell not in old:
                print(f"  NEW CELL {cell}")
                continue
            if cell not in snap:
                bad.append(f"{cell}: disappeared")
                continue
            for k in sorted(old[cell]):
                if old[cell][k] != snap[cell].get(k):
                    o, n = old[cell][k], snap[cell].get(k, {})
                    diff = [f for f in o if o[f] != n.get(f)]
                    bad.append(f"{cell} {k}: {diff}")
        if bad:
            print(f"FIDELITY BROKEN -- {len(bad)} episode(s) differ")
            for b in bad[:40]:
                print(f"  {b}")
            return 1
        print(f"fidelity OK -- {len(snap)} cells, "
              f"{sum(len(v) for v in snap.values())} episodes identical")
        return 0
    ap.error("need --write or --check")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
