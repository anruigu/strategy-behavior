"""The breadth-generator pipeline: propose -> gate -> repair -> screen -> curate.

    PY=/workspace/allie/venvs/tinker-ipd/bin/python
    $PY gen_pipeline.py --n 8                        # generate + gate + report
    $PY gen_pipeline.py --skip-generate --screen Qwen/Qwen3.5-9B
    $PY gen_pipeline.py --promote claims_desk night_auditor

One command per stage of the plan's loop, all idempotent over
`specs/candidates/`:

  1. `generate_specs.py` proposes candidates (skipped with --skip-generate).
  2. `tune_spec.tune` runs the scripted economic gates at the endpoints, maps
     failures to bounded knob moves, and confirms survivors on the full
     DOSE_GRID at 64 seeds — the same bar the hand-written cells clear.
  3. `pytest test_envs.py` runs with HOLE_GEN_CANDIDATES=1, so every candidate
     is put through the whole invariant battery (determinism, arms-identical
     surfaces, garbage-never-scored, reference endpoints, population rotation,
     dose monotonicity) that the interpreter claims it inherits.
  4. `check_suite.screen` (only with --screen MODEL) measures the base model's
     exploration of each surviving cell — the half of validity scripted
     policies cannot reach (0818 §5), and the gate `merchant` failed at (§9).
  5. A curation report lands in specs/candidates/report.md: gates, repairs
     applied, headroom, contamination/overlap flags, and the full brief text,
     because the one thing no gate checks is whether the hole is really the
     conduct the spec claims it is. That read is the human's job.

Promotion is deliberately manual: --promote moves a signed-off candidate into
`specs/`, where `registry._load_gen` picks it up for every future run.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
from typing import Dict, List, Optional

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

os.environ.setdefault("HOLE_GEN_CANDIDATES", "1")   # before registry loads

import core  # noqa: E402
import registry  # noqa: E402
import spec_env  # noqa: E402
import tune_spec  # noqa: E402
from generate_specs import guard_flags  # noqa: E402
from spec import DomainSpec, spec_files  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
CANDIDATES = HERE / "specs" / "candidates"
ACCEPTED = HERE / "specs"
PY = sys.executable


def load_candidates() -> Dict[str, DomainSpec]:
    out = {}
    for p in spec_files(CANDIDATES):
        out[p.stem] = DomainSpec.load(p)
    return out


def run_pytest() -> bool:
    """The invariant battery over hand-written envs AND candidates."""
    env = dict(os.environ, HOLE_GEN_CANDIDATES="1")
    r = subprocess.run([PY, "-m", "pytest", str(HERE / "test_envs.py"), "-q"],
                       env=env, cwd=HERE, capture_output=True, text=True)
    tail = (r.stdout or r.stderr).strip().splitlines()
    print("[pytest] " + (tail[-1] if tail else "no output"))
    if r.returncode != 0:
        print("\n".join(tail[-25:]))
    return r.returncode == 0


def report_md(specs: Dict[str, DomainSpec], tune_reports: Dict[str, Dict],
              screen_rows: List[Dict], pytest_ok: bool) -> str:
    by_env = {}
    for row in screen_rows:
        by_env[row["env"]] = row
    lines = [
        "# Generated-domain curation report",
        "",
        f"Candidates: {len(specs)} · invariant battery "
        f"{'PASS' if pytest_ok else '**FAIL**'} · screen rows: {len(screen_rows)}",
        "",
        "A row is promotable only if: gates `passed`, invariants pass, headroom "
        "is not FLOOR/CEILING, no contamination flag survives a human read, and "
        "the brief below actually describes the hole the spec claims. Promote "
        "with `gen_pipeline.py --promote <name...>`.",
        "",
        "| name | hole type | gates | repairs | headroom | exploit/dec | "
        "invalid | flags |",
        "|---|---|---|---:|---|---:|---:|---|",
    ]
    for name, sp in specs.items():
        rep = tune_reports.get(name, {})
        scr = by_env.get(name)
        contamination, overlap = guard_flags(sp)
        flags = "; ".join((["CONTAM: " + ", ".join(contamination)]
                           if contamination else [])
                          + (["overlap: " + ", ".join(overlap)]
                             if overlap else [])) or "—"
        xr = ("—" if not scr or scr["exploit_rate"] is None
              else f"{scr['exploit_rate']:.3f}")
        inv = ("—" if not scr or scr["invalid_rate"] is None
               else f"{scr['invalid_rate']:.2f}")
        head = scr["headroom"] if scr else "(not screened)"
        lines.append(
            f"| `{name}` | {sp.hole_type} | {rep.get('status', '?')} | "
            f"{len(sp.notes.get('repairs', []))} | {head} | {xr} | {inv} | "
            f"{flags} |")
    lines.append("")
    for name, sp in specs.items():
        rep = tune_reports.get(name, {})
        lines += [f"## `{name}` — {sp.hole_type}", "", sp.blurb, ""]
        if rep.get("problems"):
            lines += ["Gave up on: " + "; ".join(map(str, rep["problems"])), ""]
        if sp.notes.get("repairs"):
            lines += ["Repairs applied:"] + [
                f"- iter {r['iter']}: {r['problems']} → {r['moves']}"
                for r in sp.notes["repairs"]] + [""]
        lines += ["Brief the agent reads:", "", "```",
                  sp.brief, "```", "",
                  "Round template:", "", "```", sp.round_template, "```", ""]
    return "\n".join(lines)


def promote(names: List[str]) -> None:
    for name in names:
        src = CANDIDATES / f"{name}.json"
        if not src.exists():
            raise SystemExit(f"no candidate {src}")
        sp = DomainSpec.load(src)
        if sp.notes.get("tuning") != "passed":
            raise SystemExit(f"{name}: gates are {sp.notes.get('tuning')!r}, "
                             "not 'passed' — run the pipeline first")
        sp.notes["status"] = "accepted"
        sp.save(ACCEPTED / f"{name}.json")
        src.unlink()
        print(f"[promoted] {name} -> specs/{name}.json")


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--model", default=os.environ.get("SPEC_AUTHOR_MODEL",
                                                      "openai/gpt-4.1"))
    ap.add_argument("--skip-generate", action="store_true",
                    help="work with what is already in specs/candidates/")
    ap.add_argument("--seeds", type=int, default=32)
    ap.add_argument("--grid-seeds", type=int, default=64)
    ap.add_argument("--max-iters", type=int, default=10)
    ap.add_argument("--screen", default="", metavar="MODEL",
                    help="live headroom screen on gate survivors")
    ap.add_argument("--screen-seeds", type=int, default=12)
    ap.add_argument("--report", default=str(CANDIDATES / "report.md"))
    ap.add_argument("--promote", nargs="+", default=None, metavar="NAME",
                    help="move signed-off candidates into specs/ and exit")
    args = ap.parse_args(argv)

    if args.promote:
        promote(args.promote)
        return 0

    # -- 1. propose ---------------------------------------------------------
    if not args.skip_generate:
        r = subprocess.run([PY, str(HERE / "generate_specs.py"),
                            "--n", str(args.n), "--model", args.model],
                           cwd=HERE)
        if r.returncode != 0:
            print("[warn] generation produced nothing new; continuing with "
                  "existing candidates")

    specs = load_candidates()
    if not specs:
        raise SystemExit("no candidates to process")
    print(f"\n=== gating {len(specs)} candidate(s) ===")

    # -- 2. gate + repair ----------------------------------------------------
    tune_reports = {}
    for name, sp in specs.items():
        sp, rep = tune_spec.tune(sp, seeds=args.seeds,
                                 grid_seeds=args.grid_seeds,
                                 max_iters=args.max_iters)
        tune_reports[name] = rep
        sp.save(CANDIDATES / f"{name}.json")

    passing = [n for n, r in tune_reports.items() if r["status"] == "passed"]
    print(f"\n{len(passing)}/{len(specs)} candidates pass the economic gates")

    # -- 3. invariants -------------------------------------------------------
    pytest_ok = run_pytest()

    # -- 4. live headroom (survivors only: a screen costs sampling quota) ----
    screen_rows: List[Dict] = []
    if args.screen and passing and pytest_ok:
        from check_suite import screen as live_screen
        screen_rows = live_screen(args.screen, passing, doses=[1.0],
                                  seeds=args.screen_seeds, arms=["hole"])
        (CANDIDATES / "_screen.json").write_text(
            json.dumps(screen_rows, indent=1) + "\n")
    elif args.screen:
        print("[skip screen] nothing passed the gates or invariants failed")

    # -- 5. curation report ---------------------------------------------------
    md = report_md(specs, tune_reports, screen_rows, pytest_ok)
    pathlib.Path(args.report).write_text(md + "\n")
    print(f"\nwrote {args.report}")
    return 0 if (passing and pytest_ok) else 1


if __name__ == "__main__":
    raise SystemExit(main())
