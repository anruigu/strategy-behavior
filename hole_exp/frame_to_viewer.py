"""Load the frame-ablation training traces into the SkyRL viewer.

`to_viewer.py --from-run` reads the env off each trace record and calls
`registry.get(env)`; the frame-ablation runs are trained on ablate_plant VARIANT
envs (e.g. `tax_expl_game_hid`, `tax_expl_nat`), which are registered at runtime,
not persisted. So register them first, then hand each run to to_viewer.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import ablate_plant as ab  # noqa: E402
import to_viewer  # noqa: E402

ARMS = ["game_hole", "game_nohole", "natural_hole", "natural_nohole"]


def main() -> int:
    bases = ab.base_specs()
    # Cover both frames and both horizons so every variant name a run's config
    # can reference resolves (game arm = *_game_hid, natural arm = *_nat).
    ab.register_variants(bases, ("explicit",), ("game", "natural"),
                         ("hidden", "disclosed"))
    root = HERE / "runs" / "frame-ablation"
    for a in ARMS:
        run = root / f"mixed_{a}_d1_s0"
        if not (run / "config.json").exists():
            print(f"[skip] {a}: no run dir")
            continue
        to_viewer.main(["--from-run", str(run),
                        "--alias", f"frame-{a.replace('_', '-')}"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
