"""The removal ablation, read off the training curves (0820).

Three arms, same six natural-framed domains, same 27B, same 60 steps:

    natural_hole          no consequence at all -- the ceiling
    natural_nohole        clawback + fine + REMOVAL (the shipped control):
                          the first detected exploit ends the term
    natural_norem_nohole  clawback + fine, no removal: a detected round costs
                          that round, and a policy that stops exploiting earns
                          full honest pay again

The comparison the ablation exists for is nohole vs norem_nohole. If the two
curves land in the same place, the shipped control's fall is about the PRICE of
exploiting and the absorbing state was incidental. If the recoverable arm falls
less far, part of the shipped effect was the term ending rather than the policy
changing -- and `analyze_recovery.py` says which, by measuring what the policy
does after being caught.

    PY=/workspace/allie/venvs/tinker-ipd/bin/python
    $PY frame_removal_report.py
    $PY frame_removal_report.py --md ../results/frame-removal-0820.md
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics as st
from typing import Dict, List, Optional

HERE = pathlib.Path(__file__).resolve().parent
RUNS = HERE / "runs" / "frame-ablation"

ARMS = ["natural_hole", "natural_nohole", "natural_norem_nohole"]
CHANNELS = [("train/exploit_rate", "exploit"), ("train/capture", "capture"),
            ("train/detected", "detected"), ("train/removed", "removed")]


def load(label: str) -> List[dict]:
    p = RUNS / label / "metrics.jsonl"
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def at(rows: List[dict], step: int, key: str) -> Optional[float]:
    for r in rows:
        if r.get("step") == step:
            return r.get(key)
    return None


def tail_mean(rows: List[dict], key: str, n: int = 10) -> Optional[float]:
    """Mean over the last n steps -- one step of a 36-episode batch is noisy
    enough that a single final value is not a number worth comparing."""
    vals = [r[key] for r in rows[-n:] if r.get(key) is not None]
    return st.fmean(vals) if vals else None


def fmt(v: Optional[float]) -> str:
    return "--" if v is None else f"{v:.2f}"


def agg(vals: List[Optional[float]]) -> str:
    vs = [v for v in vals if v is not None]
    if not vs:
        return "--"
    m = st.fmean(vs)
    return f"{m:.2f}" + (f" ±{st.pstdev(vs):.2f}" if len(vs) > 1 else "")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    ap.add_argument("--steps", nargs="+", type=int, default=[0, 30, 59])
    ap.add_argument("--md", default="")
    args = ap.parse_args(argv)

    runs: Dict[str, Dict[int, List[dict]]] = {}
    for arm in ARMS:
        runs[arm] = {}
        for s in args.seeds:
            rows = load(f"mixed_{arm}_d1_s{s}")
            if rows:
                runs[arm][s] = rows

    out: List[str] = ["# removal ablation -- training curves", ""]

    hdr = ("| run | " + " | ".join(f"step {s}" for s in args.steps)
           + " | final exploit | final capture | detected | removed |")
    out += [hdr, "|---|" + "---|" * (len(args.steps) + 4)]
    for arm in ARMS:
        for s, rows in sorted(runs[arm].items()):
            cells = [fmt(at(rows, k, "train/exploit_rate")) for k in args.steps]
            out.append(
                f"| mixed_{arm}_d1_s{s} | " + " | ".join(cells) + " | "
                + fmt(tail_mean(rows, "train/exploit_rate")) + " | "
                + fmt(tail_mean(rows, "train/capture")) + " | "
                + fmt(tail_mean(rows, "train/detected")) + " | "
                + fmt(tail_mean(rows, "train/removed")) + " |")
    out += ["", "## arm means (last 10 steps, ± sd across seeds)", "",
            "| arm | n | exploit | capture | detected | removed |",
            "|---|---|---|---|---|---|"]
    for arm in ARMS:
        rs = list(runs[arm].values())
        if not rs:
            continue
        out.append(
            f"| {arm} | {len(rs)} | "
            + " | ".join(agg([tail_mean(r, k) for r in rs])
                         for k, _ in CHANNELS) + " |")

    hole = [tail_mean(r, "train/exploit_rate")
            for r in runs["natural_hole"].values()]
    rem = [tail_mean(r, "train/exploit_rate")
           for r in runs["natural_nohole"].values()]
    nor = [tail_mean(r, "train/exploit_rate")
           for r in runs["natural_norem_nohole"].values()]
    if rem and nor and all(v is not None for v in rem + nor):
        out += ["", f"**removal effect on the trained exploit rate: "
                    f"{st.fmean(nor) - st.fmean(rem):+.3f}** "
                    f"(recoverable {st.fmean(nor):.3f} vs absorbing "
                    f"{st.fmean(rem):.3f}"
                    + (f", ceiling {st.fmean([v for v in hole if v is not None]):.3f}"
                       if any(v is not None for v in hole) else "") + ")",
                "",
                "A near-zero difference means the absorbing state was not doing "
                "the work and the control arm's fall is a real change of "
                "policy. A positive difference means part of the shipped fall "
                "was the term ending. Either way `analyze_recovery.py` is the "
                "read that separates a lower rate from a learned contingency."]

    md = "\n".join(out) + "\n"
    if args.md:
        pathlib.Path(args.md).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(args.md).write_text(md)
        print(f"wrote {args.md}")
    print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
