"""Load the frame-ablation training traces into the SkyRL viewer.

`to_viewer.py --from-run` reads the env off each trace record and calls
`registry.get(env)`; the frame-ablation runs are trained on ablate_plant VARIANT
envs (e.g. `tax_expl_game_hid`, `tax_expl_nat`, `tax_expl_nat_nr`), which are
registered at runtime, not persisted. So register them first, then hand each run
to to_viewer.

    python frame_to_viewer.py                  # the four shipped s0 arms
    python frame_to_viewer.py --run runs/frame-ablation/mixed_natural_norem_nohole_d1_s0
"""
from __future__ import annotations

import argparse
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import ablate_plant as ab  # noqa: E402
import to_viewer  # noqa: E402

ARMS = ["game_hole", "game_nohole", "natural_hole", "natural_nohole"]


def register_all() -> None:
    """Cover both frames, both horizons AND both removal settings, so every
    variant name a run's config can reference resolves (game arm = *_game_hid,
    natural arm = *_nat, recovery ablation = *_nat_nr).

    The 0819 scale-up domains have only their NATURAL surfaces authored, so a
    game variant of one is an empty brief that fails spec validation. They are
    still legitimate natural-frame cells (frame-full/nat21 trains on them), so
    the game frame is registered only for the bases that have one."""
    bases = ab.base_specs()
    from ablate_surfaces import SURFACES

    game = {k: v for k, v in bases.items()
            if (SURFACES.get(k) or {}).get("game_setting")}
    ab.register_variants(game, ("explicit",), ("game",),
                         ("hidden", "disclosed"), ("inherit", "off"))
    ab.register_variants(bases, ("explicit",), ("natural",),
                         ("hidden", "disclosed"), ("inherit", "off"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", action="append", default=[],
                    help="run directory to import (repeatable); default is the "
                         "four shipped s0 arms")
    ap.add_argument("--alias", action="append", default=[],
                    help="viewer alias for the matching --run (default: the "
                         "run directory name)")
    args = ap.parse_args(argv)

    register_all()
    root = HERE / "runs" / "frame-ablation"

    if args.run:
        runs = [(pathlib.Path(r), args.alias[i] if i < len(args.alias) else None)
                for i, r in enumerate(args.run)]
    else:
        runs = [(root / f"mixed_{a}_d1_s0", f"frame-{a.replace('_', '-')}")
                for a in ARMS]

    for run, alias in runs:
        if not (run / "config.json").exists():
            print(f"[skip] {run}: no run dir")
            continue
        to_viewer.main(["--from-run", str(run),
                        "--alias", alias or run.name.replace("_", "-")])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
