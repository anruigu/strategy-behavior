#!/usr/bin/env python3
"""Read the opponent-conditioning wave off its training metrics.

    python cue_readout.py                       # every mixed_cc_* run
    python cue_readout.py --last 30 --md OUT.md

Six runs, three trainer configurations x thinking on/off, all `--regime-mix 0.5`
on the same roster (`sbatch_cuecond.sh`). The question is whether either fix
makes the policy CONDITION on its counterpart, and the number that answers it is
`cue/cci` -- the hole-minus-nohole exploit gap taken at matched decision points.

WHY THE TAIL AND NOT THE LAST STEP. The training-time discrimination signal on
these runs is far too noisy to read a single step off: MIXED-REGIME.md measured
a per-step SE around 0.13 and watched one seed swing +0.17 -> -0.01 -> +0.22
across three consecutive checkpoints. So everything here is a mean over the last
`--last` steps with a standard error over those steps, and even that is a
SCREEN. The claim comes from replaying checkpoints through the eval battery;
this tells you which arms are worth replaying.

The columns:

    CCI       cue-conditioning index, matched decision points. The headline.
    DISC      the old pooled gap, kept beside it. CCI moving while DISC does not
              (or the reverse) is the composition artefact separating them, and
              that is worth seeing rather than averaging over.
    blind     the gap at the FIRST decision, before the counterpart has
              responded to anything. The placebo: it should stay near zero. CCI
              up WITH blind up is a prior shift, not conditioning.
    rate      pooled exploit rate. A CCI that only grows because the arm walked
              off a floor or a ceiling is not the same finding.
    probe     two-way forced-choice accuracy of the disposition probe on the
              observable history. On the CONTROL arm this is the identifiability
              check: at chance, the cue is unreadable and no trainer change was
              going to help.
"""
from __future__ import annotations

import argparse
import json
import math
import statistics as st
import sys
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent

# label fragment -> what it means, in the order the table should read
ARMS = [("regmix-aux-rr-critic", "aux+cue"),
        ("regmix-rr-critic", "cue"),
        ("regmix-aux", "aux"),
        ("regmix", "ctl")]


def arm_of(label: str) -> str:
    """`mixed_cc_regmix-rr-critic_d1_s0` -> `cue`.

    The arm tag is the middle field: train_mixed builds the label as
    `mixed[_suffix]_<arm>[-think]_d<dose>_s<seed>`, so the tag has to be cut out
    of the middle rather than matched at either end -- an `endswith` test sees
    only `_s0`.
    """
    body = label.replace("-think", "")
    tag = body.split("_d")[0].split("_")[-1]
    for frag, name in ARMS:          # longest first, so `regmix` cannot shadow
        if tag == frag:
            return name
    return f"?({tag})"


def tail(rows: List[Dict], key: str, last: int):
    v = [r[key] for r in rows[-last:] if isinstance(r.get(key), (int, float))]
    if not v:
        return None, None, 0
    se = st.stdev(v) / math.sqrt(len(v)) if len(v) > 1 else 0.0
    return st.fmean(v), se, len(v)


def fmt(mu: Optional[float], se: Optional[float], places: int = 3) -> str:
    if mu is None:
        return "   --   "
    s = f"{mu:+.{places}f}"
    return s if not se else f"{s}+-{se:.{places}f}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", default=str(HERE / "runs"))
    ap.add_argument("--glob", default="mixed_cc_*")
    ap.add_argument("--last", type=int, default=30,
                    help="steps of tail to average (see the docstring: a single "
                         "step is not readable on this signal)")
    ap.add_argument("--md", default=None, help="also write a markdown table here")
    args = ap.parse_args()

    found = sorted(Path(args.runs).glob(args.glob))
    if not found:
        print(f"no runs matching {args.glob} under {args.runs}", file=sys.stderr)
        return 1

    lines = [f"| arm | think | steps | CCI (last {args.last}) | DISC | blind | "
             f"rate | probe | lor |",
             "|---|---|---|---|---|---|---|---|---|"]
    for d in found:
        mp = d / "metrics.jsonl"
        if not mp.exists():
            continue
        rows = [json.loads(x) for x in mp.read_text().splitlines() if x.strip()]
        if not rows:
            continue
        arm = arm_of(d.name)
        think = "on" if "-think" in d.name else "off"
        cells = [fmt(*tail(rows, k, args.last)[:2])
                 for k in ("cue/cci", "regime/discrimination", "cue/blind_gap")]
        rate = tail(rows, "cue/rate", args.last)
        probe = tail(rows, "aux/probe_acc", args.last)
        lor = tail(rows, "cue/lor", args.last)
        lines.append(
            f"| {arm} | {think} | {rows[-1]['step']} | " + " | ".join(cells)
            + f" | {fmt(rate[0], rate[1])} | "
            + (f"{probe[0]:.3f}" if probe[0] is not None else "--")
            + f" | {fmt(lor[0], lor[1], 2)} |")
    out = "\n".join(lines)
    print(out)
    # The one comparison the table is FOR, spelled out, because a reader
    # scanning six rows will otherwise compare the wrong pair: each fix is
    # judged against the control at the SAME thinking setting, never across it.
    print("\nEach arm is read against `ctl` at the same `think` setting. A fix "
          "that works shows CCI up with `blind` flat; CCI and `blind` moving "
          "together is a prior shift, and CCI up with `rate` walking off a "
          "floor or ceiling is headroom, not conditioning.")
    if args.md:
        Path(args.md).write_text(out + "\n")
        print(f"\nwrote {args.md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
