#!/usr/bin/env python
"""Cross-play the 8 model-generated cells with every seat filled by a live model.

    python run_gen_crossplay.py --focal-only qwen --matrix cross --seeds 4 --dry-run
    python run_gen_crossplay.py --focal-only qwen --matrix cross --seeds 4 --traces

A thin wrapper around `run_referee_crossplay.py` rather than a second runner.
It registers `engines_generated.GENERATED` into `RG.GAMES`/`RG.BY_NAME` and
then hands argv straight to that file's `main()`, so the sampling path, the
retry/widen logic, the resume key, the row schema and the trace format are
byte-identical to the hand-built cells' wave. Two waves that share a schema can
be pooled; two runners that drifted cannot.

Registration is deliberately NOT done inside `run_referee_crossplay.py`. That
file's qwen entry is the pre-training baseline for the shipped atlas cells, and
`--games all` there has to keep meaning the shipped roster.

WHAT THIS WAVE ASKS. Whether qwen3.8-27b, dropped into a game whose referee
does not check something, finds that and uses it. Seat 0 is qwen and every
other seat is the opponent model, and because `row_of` already pools the
non-focal seats into `opp_r_*`, ONE episode reads in both directions: qwen's
rate on the hole and the opponent's rate on the same board, same seed, same
arm. `--focal-only` exists so the wave does not also pay for the mirrored
cells, which would sample the same contrast a second time with the seats
swapped.

Two extra flags beyond the wrapped runner's:

  --focal-only M [M ...]   keep only cells whose focal seat is one of these
  --involve M [M ...]      keep only cells where one of these sits SOMEWHERE,
                           focal or opponent. With `--matrix cross` that is
                           both directions of every pair the model is in, and
                           the reverse direction is the SEAT CONTROL: seat 0 is
                           always the focal one, so a rate that only holds when
                           qwen is focal is a seat effect and not a finding.
                           It is also the cheap direction -- three of four
                           seats become the open-weights model.
  --games all              means the 8 GENERATED cells here, not the atlas ones
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import referee_games as RG          # noqa: E402
import engines_generated as EG      # noqa: E402
import run_referee_crossplay as XP  # noqa: E402
import bots                         # noqa: E402

GEN_NAMES = [g.NAME for g in EG.GENERATED]

# Bound at import, BEFORE `main` rebinds `XP.row_of` to the wrapper below.
# Reading it through the module at call time instead cost a whole wave: the
# wrapper resolved `XP.row_of` to itself and every episode died of
# RecursionError -- after making all of its model calls, so the failure was
# silent, complete and billed. `_selftest` now catches this class offline.
_XP_ROW_OF = XP.row_of


def register() -> None:
    new = [g for g in EG.GENERATED if g.NAME not in RG.BY_NAME]
    RG.GAMES = tuple(RG.GAMES) + tuple(new)
    RG.BY_NAME.update({g.NAME: g for g in new})


def _row_of(ep, game, cell):
    """`XP.row_of` plus the opponent seats' RAW COUNTS, not just their rate.

    The shipped row carries `opp_r_<kind>` and nothing else, which is enough
    to print one episode and not enough to pool a cell: rates cannot be
    averaged across episodes that offered different numbers of opportunities
    without silently weighting a 2-chance episode like a 20-chance one. That is
    the same mistake `summarize_referee.pooled` exists to avoid on the focal
    seat, and the opponent column of this wave is doing the identical job --
    it is the within-episode control, so it has to be poolable the same way.

    Additive: every column the shipped schema defines is still written with
    the same value, so these rows read fine in the shipped summariser.
    """
    out = _XP_ROW_OF(ep, game, cell)
    others = [p for p in game.exploiters() if p != 0]
    for k in game.KINDS:
        out[f"opp_v_{k}"] = sum(ep.violations[p][k] for p in others)
        out[f"opp_o_{k}"] = sum(ep.opportunities[p][k] for p in others)
    out["opp_invalid"] = sum(ep.invalid[p] for p in range(game.N_PLAYERS)
                             if p != 0)
    out["opp_decisions"] = sum(ep.decisions[p] for p in range(game.N_PLAYERS)
                               if p != 0)
    return out


def _dry_episode(game):
    """Decision count for a generated cell, with no network call.

    `XP._dry_episode` routes through `test_referee_games.Scripted`, which parses
    the ATLAS games' prompts; on a generated cell it emits nothing parseable and
    every move falls back to the honest default. The counts would still be
    right -- a fallback is a decision -- but the episode would take a path no
    live wave takes, and the `bots.Scripted` policies exist precisely to walk
    the generated prompts. Atlas cells keep the original bot.
    """
    if game.NAME in EG.BY_NAME:
        seen = []

        def ask(pid, phase, prompt):
            seen.append((pid, phase))
            return bots.Scripted("honest", 0)(pid, phase, prompt)

        return game.run(ask, 0, "hole", 0.0), seen
    return XP._dry_episode(game)


def _selftest() -> None:
    """Run one scripted episode of every generated cell through the real row
    builder, offline, before a single token is bought.

    The wave this replaces failed 96 out of 96 episodes and reported it only
    as a line per episode in a log, having already paid for every model call
    -- the row builder is the last step, so a bug there is maximally
    expensive and maximally quiet. Anything the live path does after `ask`
    returns can be exercised for free with a scripted seat, so it is.
    """
    for game in EG.GENERATED:
        ep, _ = _dry_episode(game)
        cell = {"game": game.NAME, "condition": "neutral", "arm": "hole",
                "p_audit": 0.0, "focal": "qwen", "other": "qwen", "seed": 0}
        r = _row_of(ep, game, cell)
        k = (game.HARD or game.KINDS)[0]
        for col in ("score_focal", f"v_{k}", f"o_{k}", f"opp_v_{k}",
                    f"opp_o_{k}", "opp_decisions"):
            if col not in r:
                raise SystemExit(f"[selftest] {game.NAME}: row is missing "
                                 f"{col!r}; the wave would write a column the "
                                 f"analysis reads as absent data")


def main() -> int:
    register()
    XP._dry_episode = _dry_episode
    XP.row_of = _row_of
    _selftest()

    argv = list(sys.argv[1:])

    def take(flag):
        """Pull a model-list flag out of argv before the wrapped parser sees it."""
        if flag not in argv:
            return None
        i = argv.index(flag)
        j = i + 1
        while j < len(argv) and not argv[j].startswith("--"):
            j += 1
        vals = set(argv[i + 1:j])
        if not vals:
            raise SystemExit(f"{flag} needs at least one model name")
        bad = sorted(vals - set(XP.MODELS))
        if bad:
            raise SystemExit(f"{flag} {bad}: not in {sorted(XP.MODELS)}")
        argv[i:j] = []
        return vals

    focal_only = take("--focal-only")
    involve = take("--involve")

    if "--games" not in argv:
        argv += ["--games", *GEN_NAMES]

    if focal_only or involve:
        inner = XP.cells

        def cells(a):
            out = inner(a)
            if focal_only:
                out = [c for c in out if c["focal"] in focal_only]
            if involve:
                out = [c for c in out
                       if c["focal"] in involve or c["other"] in involve]
            return out

        XP.cells = cells

    sys.argv = [sys.argv[0]] + argv
    return XP.main()


if __name__ == "__main__":
    raise SystemExit(main())
