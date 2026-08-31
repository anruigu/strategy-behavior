"""Read a results directory and print the model comparison.

    python report.py results/pilot [--by family] [--arm memo]

Two tables and one question:

  CONTROL     per model x arm. The probe (does the agent know what its principal
              wants), the solo condition (does it act on that when nothing
              stands in its way), and mandate compliance (does its authority
              hold under pressure). None of these can be blamed on a partner.

  COOPERATION per model x arm, in the conditions where a partner exists.
              Welfare against the exact frontier, efficiency, and the two
              execution reads -- fixed-pie errors on compatible issues and
              logrolling on integrative ones.

  DISCRIMINATION  for each metric, the spread across models. A metric where
              every model scores the same is not separating anything, and
              saying so is more useful than printing it again. Flags both
              saturation (everyone near the ceiling) and dead columns.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Dict, List, Optional, Sequence

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "hole_exp"))

import metrics as M  # noqa: E402

CONTROL_COLS = ("probe_accuracy", "probe_direction_accuracy",
                "probe_tradeoff_accuracy", "probe_rank_rho", "probe_IA",
                "solo_capture", "individual_capability", "mandate_compliance",
                "control")
COOP_COLS = ("deal", "welfare_norm", "welfare_norm_fair", "pareto_efficiency",
             "compat_correct", "integr_correct", "distrib_capture",
             "surplus_share", "capture", "cooperation")
HEALTH = ("invalid_rate", "broken", "proposal_length_errors",
          "probe_coverage", "probe_truncated", "probe_empty")
# Below this spread across models, a column is not telling models apart.
FLAT = 0.05
SATURATED = 0.95


def load(d: pathlib.Path) -> List[Dict]:
    out = []
    for f in sorted(d.glob("*.json")):
        out.append(json.loads(f.read_text()))
    if not out:
        raise SystemExit(f"no result files in {d}")
    return out


def cell(runs, model: str, key: str, col: str) -> Optional[float]:
    for r in runs:
        if r["model"] == model:
            return r["summary"].get(key, {}).get(col)
    return None


def table(runs, keys: Sequence[str], cols: Sequence[str], title: str) -> None:
    models = [r["model"] for r in runs]
    width = max(len(m) for m in models) + 2
    print(f"\n{title}")
    for key in keys:
        present = [c for c in cols
                   if any(cell(runs, m, key, c) is not None for m in models)]
        if not present:
            continue
        print(f"\n  {key}")
        print("    " + "model".ljust(width) +
              "".join(c[:13].rjust(15) for c in present))
        for m in models:
            row = "".join(
                (f"{cell(runs, m, key, c):.2f}" if cell(runs, m, key, c) is not None
                 else "-").rjust(15) for c in present)
            print("    " + m.ljust(width) + row)


def discrimination(runs, keys: Sequence[str], cols: Sequence[str]) -> None:
    models = [r["model"] for r in runs if not r["model"].startswith("scripted:")]
    if len(models) < 2:
        print("\nDISCRIMINATION: needs at least two non-scripted models.")
        return
    print("\nDISCRIMINATION (spread across models; scripted rows excluded)")
    rows = []
    for key in keys:
        for c in cols:
            vals = [cell(runs, m, key, c) for m in models]
            vals = [v for v in vals if v is not None]
            if len(vals) < 2:
                continue
            spread = max(vals) - min(vals)
            note = ""
            if spread < FLAT and min(vals) >= SATURATED:
                note = "saturated"
            elif spread < FLAT:
                note = "flat"
            rows.append((spread, f"{key}/{c}", min(vals), max(vals), note))
    for spread, name, lo, hi, note in sorted(rows, reverse=True):
        print(f"  {name:44s} {lo:.2f} .. {hi:.2f}   spread {spread:.2f}  {note}")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results", help="directory written by run_delegation.py")
    ap.add_argument("--arms", nargs="+", default=None)
    ap.add_argument("--families", nargs="+", default=None,
                    help="also break the tables down by these families")
    a = ap.parse_args()

    runs = load(pathlib.Path(a.results))
    arms = a.arms or sorted({k.split("/")[1] for r in runs
                             for k in r["summary"] if k.count("/") == 1})
    keys_control = [f"{c}/{arm}" for arm in arms for c in ("probe", "solo")]
    keys_coop = [f"{c}/{arm}" for arm in arms for c in ("joint", "wall", "selfplay")]
    keys_control = [k for k in keys_control if any(k in r["summary"] for r in runs)]
    keys_coop = [k for k in keys_coop if any(k in r["summary"] for r in runs)]

    table(runs, keys_control + keys_coop, CONTROL_COLS, "CONTROL")
    table(runs, keys_coop, COOP_COLS, "COOPERATION")
    table(runs, keys_control + keys_coop, HEALTH, "HEALTH (read before anything else)")
    if a.families:
        fam_keys = [f"{k}/{f}" for k in keys_control + keys_coop for f in a.families]
        fam_keys = [k for k in fam_keys if any(k in r["summary"] for r in runs)]
        table(runs, fam_keys, CONTROL_COLS + COOP_COLS, "BY FAMILY")
    discrimination(runs, keys_control + keys_coop, CONTROL_COLS + COOP_COLS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
