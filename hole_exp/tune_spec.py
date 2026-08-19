"""Numeric auto-repair for generated DomainSpecs (0818 plan).

    /workspace/allie/venvs/tinker-ipd/bin/python tune_spec.py --all-candidates
    ... tune_spec.py specs/candidates/claims_desk.json --max-iters 6

Most LLM proposals fail the validity gates on NUMBERS, not concept: the hole
does not pay at dose 0, the control still pays, or honesty is a martyrdom.
`check_suite.cell_summary` reports exactly which gate failed; this module maps
each verdict to a bounded knob move and re-checks, converting most rejects
into passes without a human touching them.

The move table, one move per failing gate per iteration:

    NO-HOLE @ dose 0   offer_at0 up (x1.4); once it meets offer_at1, shave
                       forfeit_share / effort instead — the other two levers
                       that price the exploit against itself
    NO-HOLE @ dose 1   offer_at1 up (x1.4)
    OPEN               a ladder in the order cheapest-first: detect_base
                       +0.05, detect_per_dollar x1.5, fine_multiple x1.3,
                       then removal on — each capped by spec.BOUNDS
    FORCED             honest pay up (base or coef, whichever the spec uses,
                       x1.3); if that is capped, offer_at1 down (x0.85)
    METRIC / PARSE     give up immediately: those are structural, and for an
                       interpreter-backed env they indicate a bug HERE, not a
                       bad number in the spec

Every move stays inside `spec.BOUNDS` — the auto-repair cannot put a knob
anywhere a hand-written spec could not have put it — and every iteration is
appended to `notes.repairs`, so the curation report shows what tuning did
rather than presenting a tuned cell as a first draft.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import core  # noqa: E402
import spec_env  # noqa: E402
from check_suite import cell_summary  # noqa: E402
from spec import BOUNDS, DomainSpec  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
CANDIDATES = HERE / "specs" / "candidates"


def gates(name: str, seeds: int,
          doses: Tuple[float, ...] = (0.0, 1.0)) -> List[Dict]:
    """Failing cell_summary rows for the env across doses x consequences."""
    bad = []
    for consequence in core.CONSEQUENCE:
        for dose in doses:
            row = cell_summary(name, consequence, dose, seeds)
            if not row["ok"]:
                bad.append(row)
    return bad


def _cap(value: float, key: str) -> float:
    lo, hi = BOUNDS[key]
    return min(max(value, lo), hi)


def _moves(sp: DomainSpec, failures: List[Dict]) -> Tuple[Dict[str, float], List[str]]:
    """(applied knob moves, structural give-up reasons). Mutates `sp`."""
    e, c = sp.economics, sp.consequence
    moves: Dict[str, float] = {}
    fatal: List[str] = []

    def set_knob(target: Dict, knob: str, value: float, bound: str):
        new = _cap(value, bound)
        if abs(new - target.get(knob, 0.0)) > 1e-9:
            target[knob] = round(new, 6)
            moves[knob] = target[knob]

    for row in failures:
        for problem in row["problems"]:
            kind = problem.split(":")[0]
            if kind in ("METRIC", "PARSE"):
                fatal.append(f"{row['consequence']}/{row['dose']}: {problem}")
            elif kind == "NO-HOLE":
                if row["dose"] < 0.5 and e["offer_at0"] * 1.4 <= e["offer_at1"]:
                    set_knob(e, "offer_at0", e["offer_at0"] * 1.4, "offer")
                elif row["dose"] < 0.5 and e.get("forfeit_share", 0) > 0.02:
                    set_knob(e, "forfeit_share", e["forfeit_share"] * 0.8,
                             "forfeit_share")
                elif row["dose"] < 0.5 and e.get("honest_effort_cost", 0) > 0:
                    # Effort priced INTO the honest branch widens the hole from
                    # the other side; last resort at dose 0 because it also
                    # thins honesty.
                    set_knob(e, "honest_effort_cost",
                             e["honest_effort_cost"] + 1.0,
                             "honest_effort_cost")
                else:
                    set_knob(e, "offer_at1", e["offer_at1"] * 1.4, "offer")
                    e["offer_at0"] = min(e["offer_at0"], e["offer_at1"])
            elif kind == "OPEN":
                if c.get("detect_base", 0) < BOUNDS["detect_base"][1] - 1e-9:
                    set_knob(c, "detect_base", c.get("detect_base", 0) + 0.05,
                             "detect_base")
                elif c.get("detect_per_dollar", 0) < BOUNDS["detect_per_dollar"][1] - 1e-9:
                    set_knob(c, "detect_per_dollar",
                             max(c.get("detect_per_dollar", 0), 0.002) * 1.5,
                             "detect_per_dollar")
                elif c.get("fine_multiple", 1) < BOUNDS["fine_multiple"][1] - 1e-9:
                    set_knob(c, "fine_multiple",
                             c.get("fine_multiple", 1.0) * 1.3, "fine_multiple")
                elif not c.get("removal", False):
                    c["removal"] = True
                    moves["removal"] = 1.0
                else:
                    fatal.append(f"{row['consequence']}/{row['dose']}: OPEN "
                                 "with every consequence knob at its cap")
            elif kind == "FORCED":
                coef_based = bool(sp.economics.get("honest_field"))
                if coef_based and e.get("honest_field_coef", 0) * 1.3 <= \
                        BOUNDS["honest_field_coef"][1]:
                    set_knob(e, "honest_field_coef",
                             e["honest_field_coef"] * 1.3, "honest_field_coef")
                elif not coef_based and e.get("honest_base", 0) * 1.3 <= \
                        BOUNDS["honest_base"][1]:
                    set_knob(e, "honest_base",
                             max(e.get("honest_base", 0), 1.0) * 1.3,
                             "honest_base")
                else:
                    set_knob(e, "offer_at1", e["offer_at1"] * 0.85, "offer")
                    e["offer_at0"] = min(e["offer_at0"], e["offer_at1"])
    return moves, fatal


def tune(sp: DomainSpec, *, seeds: int = 32, grid_seeds: int = 64,
         max_iters: int = 10, verbose: bool = True) -> Tuple[DomainSpec, Dict]:
    """Repair `sp` in place until the gates pass or it gives up.

    Endpoint doses first (cheap, and the premium is linear in dose so the
    endpoints carry the interior up to seed noise), then a confirming pass
    over the full DOSE_GRID at `grid_seeds` — the same bar `check_suite.py`
    holds the hand-written cells to.
    """
    repairs = sp.notes.setdefault("repairs", [])
    spec_env.register_spec(sp)
    report = {"name": sp.name, "status": "passed", "iters": 0, "problems": []}

    for it in range(max_iters):
        failures = gates(sp.name, seeds)
        if not failures:
            grid = gates(sp.name, grid_seeds, doses=core.DOSE_GRID)
            if not grid:
                break
            failures = grid
        report["iters"] = it + 1
        moves, fatal = _moves(sp, failures)
        problems = [p for row in failures for p in row["problems"]]
        if fatal or not moves:
            report["status"] = "gave_up"
            report["problems"] = fatal or problems
            break
        bad_spec = sp.validate()
        if bad_spec:
            report["status"] = "gave_up"
            report["problems"] = [f"repair produced an invalid spec: {bad_spec}"]
            break
        repairs.append({"iter": it, "problems": problems, "moves": moves})
        if verbose:
            print(f"[tune] {sp.name} iter {it}: {problems} -> {moves}")
        spec_env.register_spec(sp)
    else:
        report["status"] = "gave_up"
        report["problems"] = [f"still failing after {max_iters} iterations"]

    sp.notes["tuning"] = report["status"]
    if verbose:
        print(f"[tune] {sp.name}: {report['status']} "
              f"after {report['iters']} repair iteration(s)")
    return sp, report


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="spec JSON files")
    ap.add_argument("--all-candidates", action="store_true",
                    help=f"tune every spec in {CANDIDATES}")
    ap.add_argument("--seeds", type=int, default=32)
    ap.add_argument("--grid-seeds", type=int, default=64)
    ap.add_argument("--max-iters", type=int, default=10)
    ap.add_argument("--no-write", action="store_true",
                    help="tune in memory only; do not rewrite the file")
    args = ap.parse_args(argv)

    paths = [pathlib.Path(p) for p in args.paths]
    if args.all_candidates:
        paths += sorted(CANDIDATES.glob("*.json"))
    if not paths:
        ap.error("no specs given (paths or --all-candidates)")

    gave_up = 0
    for p in paths:
        sp = DomainSpec.load(p)
        sp, report = tune(sp, seeds=args.seeds, grid_seeds=args.grid_seeds,
                          max_iters=args.max_iters)
        if report["status"] != "passed":
            gave_up += 1
            print(f"[FAIL] {sp.name}: {report['problems']}")
        if not args.no_write:
            sp.save(p)
    print(f"\n{len(paths) - gave_up}/{len(paths)} specs pass the gates")
    return 1 if gave_up else 0


if __name__ == "__main__":
    raise SystemExit(main())
