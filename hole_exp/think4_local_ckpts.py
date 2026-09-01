#!/usr/bin/env python3
"""Manifest of the LOCAL adapters, and the sampler each arm is evaluated on.

    python think4_local_ckpts.py            # inventory
    python think4_local_ckpts.py --json     # write think4_local_ckpts.json

`think4_tinker_ckpts.json` is the Tinker wave and is NOT interchangeable with
this. PLAN-think4-evals.md §0.3b: the Tinker adapters were trained
`all-linear` on a hybrid-attention model, and the samplers here serve seven
module types, so loading those would apply LoRA to 32 of 128 layers' attention
and silently sample a policy nobody trained. The local adapters were trained
through `tinker_local.service`, whose LoraConfig lists exactly the seven
modules `start_sglang.sh` serves -- so for THESE the served function is the
trained function, and §0.3b does not apply. That is the whole reason the local
wave is the one to evaluate.

STEP 0 IS EXCLUDED. A freshly initialised LoRA has B=0 and is mathematically
identical to base (ckpt_guard.py). The cells that never got past step 0 are
therefore not arms, they are base weights under an arm's name.
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re

CKPT_ROOT = pathlib.Path("/shared/allie/think4/ckpt")
HERE = pathlib.Path(__file__).resolve().parent

# cell directory -> arm key used by eval_a / eval_b
CELL_ARM = {
    "grim-nohole": "grim/nohole", "grim-eg": "grim/eg", "grim-inf": "grim/inf",
    "tft-nohole": "tft/nohole", "tft-eg": "tft/eg", "tft-inf": "tft/inf",
    "grim-hole": "hole",
}
# `hole` is the zero-consequence arm; its cell dir is named grim-hole because
# the cell trains against grim with the consequence knob off.

_DIR = re.compile(r"^adapter-(?P<tag>.+)-step(?P<step>\d{4})$")
_TAG = re.compile(r"^s(?P<seed>\d+)-(?P<cell>[a-z]+-[a-z]+)(?:-(?P<pidclock>\d+))?$")


def scan(root: pathlib.Path = CKPT_ROOT) -> dict:
    """arm -> seed -> step -> adapter dir, step 0 dropped."""
    out: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    for cell in sorted(p for p in root.iterdir() if p.is_dir()):
        arm = CELL_ARM.get(cell.name)
        if arm is None:
            continue
        for d in cell.iterdir():
            m = _DIR.match(d.name)
            if not m:
                continue
            step = int(m["step"])
            if step == 0:
                continue                      # B=0: identical to base
            t = _TAG.match(m["tag"])
            if not t:
                continue                      # TEST-*, bare `adapter`, etc.
            if not (d / "adapter_model.safetensors").exists():
                continue                      # a save that did not complete
            out[arm][int(t["seed"])][step] = str(d.resolve())
    return {a: {s: dict(sorted(v.items())) for s, v in sorted(seeds.items())}
            for a, seeds in sorted(out.items())}


def usable(man: dict, step: int) -> list:
    """(arm, seed, path) for every arm/seed that reached `step`."""
    return [(a, s, man[a][s][str(step) if str(step) in man[a][s] else step])
            for a in man for s in man[a]
            if step in man[a][s] or str(step) in man[a][s]]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--step", type=int, default=35,
                    help="the matched step to report coverage at")
    a = ap.parse_args()
    man = scan()

    print(f"{'arm':14s} {'seed':>4s} {'n':>4s} {'max':>4s}   has step "
          f"{a.step}?")
    for arm in man:
        for seed, steps in man[arm].items():
            ks = sorted(steps)
            print(f"{arm:14s} {seed:4d} {len(ks):4d} {ks[-1]:4d}   "
                  f"{'yes' if a.step in steps else 'NO'}")
    u = usable(man, a.step)
    print(f"\nat step {a.step}: {len(u)} checkpoints, "
          f"{len({x[0] for x in u})} arms")
    for arm in sorted({x[0] for x in u}):
        print(f"   {arm:14s} seeds {sorted(s for x, s, _ in u if x == arm)}")

    if a.json:
        p = HERE / "think4_local_ckpts.json"
        p.write_text(json.dumps(man, indent=1, sort_keys=True))
        print(f"\nwrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
