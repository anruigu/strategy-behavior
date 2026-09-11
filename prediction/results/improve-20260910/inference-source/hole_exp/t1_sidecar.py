"""hole_exp `checkpoints.json` -> the sidecar `exploit-bench` T1 expects (0820).

The two packages record checkpoints differently and nothing translated between
them, so the T1 command `post_run.sh` prints has never actually run against a
hole_exp run -- `eval_checkpoint.py` dies on `KeyError: 'checkpoints'`.

    hole_exp        {"0": "tinker://...-step0000", "15": ..., "60": ...}
    exploit-bench   {"meta": {"arm": ...},
                     "checkpoints": [{"step": 0, "name": ..., "path": ...}]}

This writes the second from the first (plus the run's config.json for `meta`),
so the held-out battery is one command instead of a hand-built file.

    PY=/workspace/allie/venvs/tinker-ipd/bin/python
    $PY t1_sidecar.py runs/frame-ablation/mixed_natural_norem_nohole_d1_s0
    $PY ../exploit-bench/eval/eval_checkpoint.py \\
        --checkpoints <printed path> --which final --workers 16
"""
from __future__ import annotations

import argparse
import json
import pathlib
from typing import List


def sidecar(rundir: pathlib.Path) -> dict:
    ck = json.loads((rundir / "checkpoints.json").read_text())
    cfg = {}
    cfgp = rundir / "config.json"
    if cfgp.exists():
        cfg = json.loads(cfgp.read_text())

    label = rundir.name
    entries: List[dict] = []
    for step in sorted(ck, key=int):
        entries.append({"step": int(step), "path": ck[step],
                        "name": f"{label}-step{int(step):04d}"})
    if entries:
        # `pick_checkpoint('final')` looks for a `-final` suffix and otherwise
        # falls through to the last entry; naming it explicitly makes the
        # selection legible in the eval's own output rather than positional.
        entries[-1] = {**entries[-1], "name": f"{label}-final"}

    return {"meta": {"arm": label, "model": cfg.get("model"),
                     "consequence": cfg.get("consequence"),
                     "dose": cfg.get("dose"), "envs": cfg.get("envs"),
                     "source": str(rundir / "checkpoints.json")},
            "checkpoints": entries}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("rundir", nargs="+", type=pathlib.Path)
    ap.add_argument("--out", type=pathlib.Path,
                    default=pathlib.Path("results"),
                    help="directory for the sidecar files")
    args = ap.parse_args(argv)

    args.out.mkdir(parents=True, exist_ok=True)
    for rundir in args.rundir:
        if not (rundir / "checkpoints.json").exists():
            print(f"[skip] {rundir}: no checkpoints.json")
            continue
        data = sidecar(rundir)
        if not data["checkpoints"]:
            print(f"[skip] {rundir}: no successful checkpoints")
            continue
        p = args.out / f"t1-sidecar-{rundir.name}.json"
        p.write_text(json.dumps(data, indent=1) + "\n")
        print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
