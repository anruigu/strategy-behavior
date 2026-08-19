"""Watchdog for in-flight hole-atlas runs. Meant to be left running overnight.

    nohup python watch_runs.py --every 600 > logs/watch.log 2>&1 &
    python watch_runs.py --once            # one status block, then exit

Every `--every` seconds it reads each run's `metrics.jsonl` -- never the console
logs, for the reason `ipd_viewer.py` gives: the jsonl carries fields the printed
line drops, and parsing a print-formatted log is how a rounding gets inherited
silently -- and prints one block per run with progress, ETA, the two
diagnostics, and any alarms.

What it alarms on, and why each one is worth being woken for:

    DEAD        no process for the run and the last step is not the final one.
    STALLED     no new step for 3x the recent median step time. A Tinker call
                that hangs does not raise; the run simply stops advancing, and
                without this it is discovered in the morning.
    NO_DATA     n_datums == 0 for the latest step. Every episode was dropped
                (empty responses, or a degenerate group where every advantage
                was zero) so the step trained on nothing.
    INVALID     invalid_rate > 0.25. A quarter of the decisions are the default
                action rather than a choice; the arm is measuring format, not
                disposition.
    FLATLINE    exploit_rate has not moved by >0.02 over the last 20 steps AND
                the run is past its first quarter. Not necessarily wrong -- a
                genuine null is a result -- but it is worth knowing before the
                remaining hours are spent.

It never touches the runs. A watchdog that can restart things is a watchdog that
can restart them wrongly at 04:00.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from statistics import median
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent

INVALID_ALARM = 0.25
FLATLINE_DELTA = 0.02
FLATLINE_WINDOW = 20
STALL_FACTOR = 3.0


def running_labels() -> List[str]:
    """Labels of live trainers, read off the process table."""
    try:
        out = subprocess.run(["pgrep", "-af", "train_hole.py|train_mixed.py"],
                             capture_output=True, text=True).stdout
    except Exception:  # noqa: BLE001
        return []
    labels = []
    for line in out.splitlines():
        if "watch_runs" in line or "pgrep" in line:
            continue
        toks = line.split()
        arm = dose = seed = env = None
        for i, t in enumerate(toks):
            if t == "--consequence":
                arm = toks[i + 1]
            elif t == "--dose":
                dose = toks[i + 1]
            elif t == "--seed":
                seed = toks[i + 1]
            elif t == "--env":
                env = toks[i + 1]
        if arm is None:
            continue
        stem = env or "mixed"
        d = f"{float(dose):g}" if dose else "1"
        labels.append(f"{stem}_{arm}_d{d}_s{seed or '0'}")
    return labels


def read_run(run_dir: Path) -> Optional[Dict]:
    mpath = run_dir / "metrics.jsonl"
    cpath = run_dir / "config.json"
    if not mpath.exists() or not cpath.exists():
        return None
    cfg = json.loads(cpath.read_text())
    if cfg.get("dry_run"):
        return None  # a dry run is not a run
    rows = []
    for line in mpath.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                # A partially-flushed final line while the trainer is mid-write.
                continue
    # Drop stub rows left in a real run's metrics by a dry run that shared the
    # directory before the trainers started writing `metrics-dryrun.jsonl`. A
    # real step never rolls out in under a second and never trains on nothing,
    # so the pair of conditions identifies them without guessing.
    rows = [r for r in rows
            if not (r.get("n_datums") == 0 and (r.get("rollout_s") or 0) < 1.0)]
    if not rows:
        return None
    return {"dir": run_dir, "cfg": cfg, "rows": rows}


def analyse(run: Dict, live: List[str]) -> Dict:
    rows, cfg = run["rows"], run["cfg"]
    label = run["dir"].name
    last = rows[-1]
    total = int(cfg.get("steps", 0))
    step = int(last.get("step", 0))
    # Step times from `elapsed_s` deltas rather than `rollout_s`: the gap
    # between steps includes the optimiser and the weight save, which is most of
    # what a stall would be hiding in.
    elapsed = [r.get("elapsed_s") or 0.0 for r in rows]
    deltas = [b - a for a, b in zip(elapsed, elapsed[1:]) if b > a]
    step_s = median(deltas) if deltas else None
    remaining = (total - step) * step_s if (step_s and total) else None
    since = time.time() - (run["dir"] / "metrics.jsonl").stat().st_mtime

    alarms = []
    is_live = label in live
    # The last metrics row is written at index steps-1: the loop checkpoints at
    # `steps` and breaks without logging. So "finished" is step >= total-1, and
    # using `step < total` would report every completed run as DEAD.
    finished = total and step >= total - 1
    if not is_live and not finished:
        alarms.append(f"DEAD at step {step}/{total}")
    if is_live and step_s and since > STALL_FACTOR * step_s:
        alarms.append(f"STALLED {since / 60:.0f}m since last step "
                      f"(median step {step_s / 60:.1f}m)")
    if last.get("n_datums") == 0:
        alarms.append("NO_DATA: last step trained on nothing")
    inv = last.get("train/invalid_rate")
    if inv is not None and inv > INVALID_ALARM:
        alarms.append(f"INVALID {inv:.0%} of decisions unparsed")
    xr = [r.get("train/exploit_rate") for r in rows
          if r.get("train/exploit_rate") is not None]
    if (len(xr) >= FLATLINE_WINDOW and total and step > total / 4
            and max(xr[-FLATLINE_WINDOW:]) - min(xr[-FLATLINE_WINDOW:]) < FLATLINE_DELTA):
        alarms.append(f"FLATLINE: exploit_rate within {FLATLINE_DELTA} "
                      f"over {FLATLINE_WINDOW} steps")
    return {"label": label, "step": step, "total": total, "last": last,
            "rows": rows, "step_s": step_s, "eta_s": remaining, "since_s": since,
            "live": is_live, "alarms": alarms}


def fmt(a: Dict) -> str:
    last = a["last"]

    def g(key, digits=3):
        v = last.get(key)
        return "—" if v is None else f"{v:.{digits}f}"

    first = a["rows"][0]
    x0, x1 = first.get("train/exploit_rate"), last.get("train/exploit_rate")
    drift = ("—" if None in (x0, x1) else f"{x1 - x0:+.3f}")
    eta = ("—" if not a["eta_s"] else
           f"{a['eta_s'] / 3600:.1f}h" if a["eta_s"] > 3600 else
           f"{a['eta_s'] / 60:.0f}m")
    head = (f"{a['label']:26s} step {a['step']:3d}/{a['total']:<3d} "
            f"{'live' if a['live'] else 'DOWN':4s}  "
            f"R={g('train/reward')}  exploit={g('train/exploit_rate')} "
            f"({drift} since step 0)  capture={g('train/capture')}  "
            f"invalid={g('train/invalid_rate', 3)}  "
            f"step~{a['step_s'] / 60:.1f}m  eta {eta}" if a["step_s"] else
            f"{a['label']:26s} step {a['step']}/{a['total']}")
    lines = [head]
    # Per-env rows exist only for a mixed run; they are the whole point of one.
    envs = sorted({k.split("/")[1] for k in last if k.startswith("env/")})
    if envs:
        cells = []
        for e in envs:
            v = last.get(f"env/{e}/exploit_rate")
            cells.append(f"{e[:7]}={'—' if v is None else f'{v:.2f}'}")
        lines.append("    " + "  ".join(cells))
    for al in a["alarms"]:
        lines.append(f"    !! {al}")
    return "\n".join(lines)


def scan(runs_dir: Path) -> List[Dict]:
    live = running_labels()
    out = []
    for d in sorted(runs_dir.iterdir()):
        if not d.is_dir():
            continue
        run = read_run(d)
        if run:
            out.append(analyse(run, live))
    return out


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", default=str(HERE / "runs"))
    ap.add_argument("--every", type=int, default=600, help="seconds between checks")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--active-only", action="store_true", default=True,
                    help="skip runs that already finished all their steps")
    args = ap.parse_args(argv)

    runs_dir = Path(args.runs)
    while True:
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        states = scan(runs_dir)
        if args.active_only:
            states = [s for s in states
                      if s["step"] < (s["total"] or 0) - 1 or s["alarms"]]
        print(f"\n===== {stamp} · {len(states)} active =====", flush=True)
        for s in states:
            print(fmt(s), flush=True)
        alarms = [(s["label"], al) for s in states for al in s["alarms"]]
        if alarms:
            print("\n  ALARMS:", flush=True)
            for label, al in alarms:
                print(f"    {label}: {al}", flush=True)
        if args.once:
            return 1 if alarms else 0
        if states and all(s["step"] >= s["total"] for s in states):
            print("all runs finished", flush=True)
            return 0
        if not states:
            print("nothing in flight", flush=True)
            return 0
        time.sleep(args.every)


if __name__ == "__main__":
    raise SystemExit(main())
