#!/usr/bin/env python
"""Does every declared knob actually reach the game?

    python knob_liveness.py
    python knob_liveness.py --cells ta_letterauction ref_hanabi

Lifting a payoff literal out of `run()` and into a class attribute is two
edits -- declare the attribute, and make every reader use it -- and it is easy
to land the first and miss the second. The result is a DEAD KNOB: it appears
in `variants.tunable()`, it renders into the RULES text, a slider binds to it,
and the engine goes on reading the module constant. Every measurement of it is
then a measurement of nothing, reported as a finding.

That is not hypothetical. `ta_letterauction.WORD_MULT` shipped dead --
`word_points()` kept the module global -- and it read as an `inert` knob in
the catalogue for a while, which is exactly the wrong conclusion: the knob was
not inert, it was disconnected. `ref_estate.SALARY` and `ref_hanabi.TOKENS`
were the same shape of mistake, caught earlier.

So: perturb every numeric knob on every cell and check the episode
fingerprint moves. A knob that changes nothing is either

  DEAD    a wiring bug -- fix the engine, and
  INERT   genuinely without effect on what the scripted seats do, which is a
          finding and belongs in the catalogue with a note

and this cannot tell them apart. What it can do is produce the short list that
has to be read by hand, instead of the long one.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys
from typing import Any, Dict, List, Tuple

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "hackable_games"))

import referee_games as RG      # noqa: E402
import exploit_curve as EC      # noqa: E402
import variants as V            # noqa: E402

SEEDS = range(1, 5)


def fingerprint(game) -> str:
    """Scores, violations and every prompt, over both arms and both policies."""
    h = hashlib.sha256()
    for arm in ("hole", "nohole"):
        for mode in ("honest", "exploit"):
            seats = tuple(game.exploiters()) if mode == "exploit" else ()
            for s in SEEDS:
                inner = EC.mixed_ask(game, seats, s)

                def ask(pid, phase, prompt, _i=inner):
                    h.update(f"{pid}\x00{phase}\x00{prompt}\x00".encode())
                    return _i(pid, phase, prompt)

                ep = game.run(ask, s, arm)
                h.update(repr(sorted((p, round(float(v), 6))
                                     for p, v in ep.scores.items())).encode())
                h.update(repr(sorted((p, sorted(v.items()))
                                     for p, v in ep.violations.items())).encode())
    return h.hexdigest()[:16]


def perturb(val: Any) -> Any:
    """A value far enough from the default to move anything that reads it."""
    if isinstance(val, bool):
        return not val
    if isinstance(val, int):
        return val + max(2, abs(val))
    if isinstance(val, float):
        return val * 2.0 + 3.0
    return None


def check(cell: str) -> List[Tuple[str, Any, Any, bool]]:
    game = RG.BY_NAME[cell]
    klass = type(game)
    base = fingerprint(game)
    out: List[Tuple[str, Any, Any, bool]] = []
    gated = V.GATED.get(cell, {})
    for knob, default in sorted(V.tunable(cell).items()):
        new = perturb(default)
        if new is None or new == default:
            continue
        # A conditional knob is dead until the knob gating it is on, so turn
        # that on first and re-take the reference. Otherwise a correctly wired
        # `RETAINER_FLOOR` reads as a wiring bug.
        co = gated.get(knob, {})
        saved = [(k, getattr(klass, k)) for k in co]
        for k, v in co.items():
            setattr(klass, k, v)
        ref = fingerprint(game) if co else base
        old = getattr(klass, knob)
        try:
            setattr(klass, knob, new)
            try:
                moved = fingerprint(game) != ref
            except Exception:            # noqa: BLE001
                moved = True             # it reached the engine and broke it
        finally:
            setattr(klass, knob, old)
            for k, v in saved:
                setattr(klass, k, v)
        out.append((knob, default, new, moved))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cells", nargs="*", default=None)
    a = ap.parse_args()
    V.register()
    cells = a.cells or list(V.MENU + V.DEDUPED + V.HOLECROSS)
    dead: List[str] = []
    total = 0
    for cell in cells:
        rows = check(cell)
        total += len(rows)
        silent = [r for r in rows if not r[3]]
        mark = "ok" if not silent else f"{len(silent)} SILENT"
        print(f"{cell:24s} {len(rows):2d} knobs   {mark}")
        for knob, d, n, _ in silent:
            print(f"    {knob:16s} {d!r} -> {n!r} changed nothing")
            dead.append(f"{cell}.{knob}")
    print(f"\n{total} knobs over {len(cells)} cells; "
          f"{len(dead)} moved nothing and need reading by hand:")
    for d in dead:
        print(f"  {d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
