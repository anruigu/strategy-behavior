"""Tier-A readout for the env-count ladder (0820-scaling-envs.md).

    python eval_scaling.py                    # every arm, highest COMMON step
    python eval_scaling.py --step 40          # pin the step
    python eval_scaling.py --arms base scale-game-n8-hole
    python eval_scaling.py --seeds 24 --workers 64

Everything here is Tinker-direct: scripted opponents, scripted references, no
GPU, no judge, no external harness. That is deliberate -- these are the
"high-SNR" y-axes the plan says to read at one seed, and they are high-SNR
precisely because they are rates over many episodes against a fixed opponent
rather than a model grading a transcript.

    heldout_game    exploit_rate on nat_ledger + ta_kuhn, the never-trained
                    game cells
    kuhn_capture    ta_kuhn `capture` -- the share of the scripted honest ->
                    exploit span the policy takes. `exploit_rate` came out flat
                    on ta_kuhn while capture moved (0819), so both are kept.
    two_dollar      value captured and opening demand in TwoDollar, which is in
                    no registry roster at all and so is held out by construction

THE STEP IS COMMON BY DEFAULT. Twelve runs contend for one Tinker account and
will not all reach step 70 together; reading a finished arm against an
unfinished one would put training progress on an axis labelled #envs. `--step`
resolves to the highest step EVERY requested arm has checkpointed, and the
number used is stamped into the output.

ERROR BARS AT ONE SEED. There is one training seed, so the SE reported here is
the EPISODE-level bootstrap only -- it says how well this checkpoint's rate is
measured, not how much another training seed would differ. The plan gates
seeds 2-3 on pass 1 rising; do not read a rung difference smaller than these
bars as real, and do not read one larger than them as replicated either.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import games_aggression as AG  # noqa: E402
import registry  # noqa: E402
import run_aggression  # noqa: E402
import scaling_rungs as S  # noqa: E402

RUNS = HERE / "runs" / "scaling"
OUT = HERE / "results" / "scaling"

# `ta_negotiation` is registered as held-out but is NOT read as an instrument:
# 35-44% of its episodes fail to parse because the model re-derives a five
# resource inventory every turn and truncates, and the invalid rate varies ~4x
# across arms -- so the denominator is selected by verbosity and the rate is not
# comparable between checkpoints. Raising max_tokens does not fix it (reasoning
# expands to fill the budget). It is still PLAYED, so the numbers exist and the
# decision is auditable, but it is excluded from every pooled figure.
UNRELIABLE = {"ta_negotiation"}
# `ta_kuhn` exploits on 100% of base-model episodes (measured on Qwen3.8-27B
# before this ladder launched, and consistent with 0819 finding its exploit_rate
# flat while `capture` moved). A cell already at 1.0 cannot register a rise, so
# averaging it into the pooled game rate would halve that pool's sensitivity for
# nothing. It stays a first-class instrument via `kuhn_capture`, which is a
# share of the honest->exploit span and has room in both directions.
GAME_CEILING = {"ta_kuhn"}
GAME_INSTRUMENTS = ["nat_ledger", "ta_kuhn", "ta_negotiation"]


# ---------------------------------------------------------------------------
# arms
# ---------------------------------------------------------------------------

def ckpt_steps(label: str) -> Dict[int, str]:
    f = RUNS / label / "checkpoints.json"
    if not f.exists():
        return {}
    try:
        return {int(k): v for k, v in json.loads(f.read_text()).items()}
    except (ValueError, OSError):
        return {}


def all_arms() -> List[Tuple[str, str, int, str]]:
    """(arm_name, family, n, run_label) for every ladder run that exists on disk."""
    out = []
    for fam in S.FAMILIES:
        for n in S.RUNG_NS:
            for consequence in ("hole", "nohole"):
                lab = S.label(fam, n, consequence)
                if (RUNS / lab).exists():
                    out.append((f"scale-{fam}-n{n}-{consequence}", fam, n, lab))
    return out


def resolve(arm_filter: Optional[Sequence[str]], step: Optional[int],
            per_family: bool = False) -> Tuple[Dict[str, str], int, Dict]:
    """Map arm -> model path at a step every requested arm has reached.

    `per_family` freezes each FAMILY at its own highest common step instead of
    forcing one step across all 12 arms. Game episodes are multi-turn and train
    at ~6.6 min/step against synthetic's ~4.1, so a single common step throws
    away ~30 steps of synthetic training to match the slowest game arm. The
    shape of a curve is a WITHIN-family question -- every point on the synthetic
    line still shares a step with every other point on it -- so per-family
    freezing costs only cross-family comparison of absolute levels, which is
    then flagged on the figure and in `step_by_family`.
    """
    found = all_arms()
    if arm_filter:
        keep = set(arm_filter)
        found = [a for a in found if a[0] in keep]
    per_arm = {a[0]: ckpt_steps(a[3]) for a in found}
    missing = [a for a, c in per_arm.items() if not c]
    live = {a: c for a, c in per_arm.items() if c}
    if not live:
        # `--arms base` is a legitimate request (the base row is needed whether
        # or not any ladder run has checkpointed yet), so only refuse when a
        # LADDER arm was asked for and none exists.
        if arm_filter and set(arm_filter) <= {"base"}:
            return {"base": S.MODEL}, 0, {"base_only": True}
        raise SystemExit(f"no checkpoints under {RUNS}; is training running?")

    fam_of = {a[0]: a[1] for a in found}

    def common_step(arms: Sequence[str]) -> Optional[int]:
        sets = [set(live[a]) for a in arms if a in live]
        if not sets:
            return None
        c = set.intersection(*sets)
        c.discard(0)  # step 0 is the untrained base, already its own arm here
        return max(c) if c else None

    step_by_family: Dict[str, int] = {}
    if step is not None:
        models = {a: c[step] for a, c in live.items() if step in c}
        step_by_family = {f: step for f in S.FAMILIES}
    elif per_family:
        models = {}
        for fam in S.FAMILIES:
            arms = [a for a in live if fam_of.get(a) == fam]
            s = common_step(arms)
            if s is None:
                continue
            step_by_family[fam] = s
            models.update({a: live[a][s] for a in arms if s in live[a]})
        if not models:
            raise SystemExit(f"no non-zero step is common within any family "
                             f"({sorted(live)})")
        step = max(step_by_family.values())
    else:
        step = common_step(list(live))
        if step is None:
            raise SystemExit(f"no non-zero step is common to all of {sorted(live)}")
        models = {a: c[step] for a, c in live.items() if step in c}
        step_by_family = {f: step for f in S.FAMILIES}

    dropped = sorted(set(live) - set(models))
    models["base"] = S.MODEL
    meta = {"step": step, "step_by_family": step_by_family,
            "per_family": per_family, "no_checkpoints_yet": sorted(missing),
            "dropped_missing_this_step": dropped,
            "per_arm_max_step": {a: max(c) for a, c in live.items()}}
    return models, step, meta


# ---------------------------------------------------------------------------
# measurement
# ---------------------------------------------------------------------------

def boot_se(vals: List[float], n: int = 1000, seed: int = 0) -> Optional[float]:
    """Episode-level bootstrap SE. Not a training-seed SE -- see the module docstring."""
    vals = [v for v in vals if v is not None]
    if len(vals) < 2:
        return None
    rng = random.Random(seed)
    k = len(vals)
    means = []
    for _ in range(n):
        means.append(sum(vals[rng.randrange(k)] for _ in range(k)) / k)
    mu = sum(means) / len(means)
    return (sum((m - mu) ** 2 for m in means) / (len(means) - 1)) ** 0.5


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arms", nargs="+", default=None)
    ap.add_argument("--step", type=int, default=None,
                    help="checkpoint step (default: highest common to all arms)")
    ap.add_argument("--per-family", action="store_true",
                    help="freeze each family at its OWN highest common step "
                         "instead of one step across all arms (see resolve())")
    ap.add_argument("--manifest", default=None,
                    help="read the arm->checkpoint map from this JSON instead "
                         "of resolving it now. Tier A and Tier B must describe "
                         "the SAME checkpoints, and training keeps advancing "
                         "between them -- resolving twice would silently read "
                         "the two tiers at different steps.")
    ap.add_argument("--seeds", type=int, default=16,
                    help="RETIRED with the synthetic family (0820); accepted "
                         "for backward compatibility but no longer sampled")
    ap.add_argument("--game-seeds", type=int, default=48,
                    help="episodes per (arm, game instrument). Higher than "
                         "--seeds used to be on purpose: nat_ledger and ta_kuhn "
                         "are single envs each carrying a whole panel, so at 16 "
                         "they sit at SE ~0.12 on a rate near 0.4 -- too noisy "
                         "to read a shape off four rungs, which is the only "
                         "thing those panels exist to show")
    ap.add_argument("--td-seeds", type=int, default=24, help="TwoDollar episodes per arm")
    ap.add_argument("--workers", type=int, default=64)
    # Defaults come from scaling_rungs so the readout samples exactly the way
    # the ladder trained. Measuring a checkpoint under a different sampling
    # profile than it was trained under is its own confound, and here it would
    # land on the instrument (`nat_assay` sat at 0.225 invalid at t=1.0/384).
    ap.add_argument("--temperature", type=float, default=S.TEMPERATURE)
    ap.add_argument("--top-p", type=float, default=S.TOP_P)
    ap.add_argument("--max-tokens", type=int, default=S.MAX_TOKENS)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    if a.manifest:
        man = json.loads(Path(a.manifest).read_text())
        models, step, meta = man["models"], man["step"], man["meta"]
    else:
        models, step, meta = resolve(a.arms, a.step, per_family=a.per_family)
    print(f"[eval] step={step}  arms={len(models)}", flush=True)
    for k, v in meta.items():
        if v:
            print(f"[eval] {k}: {v}", flush=True)
    print(f"[eval] held-out game  ({len(GAME_INSTRUMENTS)}): "
          f"{' '.join(GAME_INSTRUMENTS)}", flush=True)
    print(f"[eval]   excluded from the pooled game rate -- unreliable: "
          f"{' '.join(sorted(UNRELIABLE))}; at ceiling: "
          f"{' '.join(sorted(GAME_CEILING))}", flush=True)

    import tinker  # noqa: PLC0415
    import tinker_actor  # noqa: PLC0415

    core.load_env_file()
    sc = tinker.ServiceClient()

    # (arm, kind, env, seed). TwoDollar is its own kind: it is not a registry
    # cell and has no consequence/dose/reference machinery.
    jobs: List[Tuple[str, str, str, int]] = []
    for arm in models:
        jobs += [(arm, "game", e, s) for e in GAME_INSTRUMENTS
                 for s in range(a.game_seeds)]
        jobs += [(arm, "td", "agg_two_dollar", s) for s in range(a.td_seeds)]
    done = {"n": 0}
    total = len(jobs)

    def one(job):
        arm, kind, env, s = job
        model = models[arm]
        rec = None
        for _ in range(3):   # transient API failures, same retry as heldout_transfer
            try:
                actor, _ = tinker_actor.build(sc, model,
                                              temperature=a.temperature,
                                              top_p=a.top_p,
                                              max_tokens=a.max_tokens)
                if kind == "td":
                    r = run_aggression.play(AG.BY_NAME[env], actor.act, s)
                    rec = {"value_captured": r["value_captured"],
                           "opening_demand": r["style"].get("opening_demand"),
                           "final_demand": r["style"].get("final_demand"),
                           "concession": r["style"].get("concession")}
                else:
                    rr = registry.rollout(registry.get(env), actor.act,
                                          consequence="hole", dose=1.0, seed=s)
                    rec = {"exploit_rate": rr["stats"].get("exploit_rate"),
                           "capture": rr["stats"].get("capture"),
                           "invalid_rate": rr["stats"].get("invalid_rate")}
                break
            except Exception:  # noqa: BLE001
                continue
        done["n"] += 1
        if done["n"] % 200 == 0:
            print(f"  {done['n']}/{total}", flush=True)
        return (arm, kind, env, rec)

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        res = list(ex.map(one, jobs))

    # -- aggregate -----------------------------------------------------------
    cells: Dict[Tuple[str, str, str], List[Dict]] = {}
    for arm, kind, env, rec in res:
        if rec is not None:
            cells.setdefault((arm, kind, env), []).append(rec)

    def pool(arm: str, kind: str, envs: Sequence[str], field: str) -> Dict:
        vals = [r[field] for e in envs for r in cells.get((arm, kind, e), [])
                if r.get(field) is not None]
        return {"mean": core.mean(vals), "se": boot_se(vals), "n": len(vals)}

    summary: Dict[str, Dict] = {}
    for arm in models:
        pooled_games = [e for e in GAME_INSTRUMENTS
                        if e not in UNRELIABLE and e not in GAME_CEILING]
        summary[arm] = {
            "model": models[arm],
            "heldout_game_exploit": pool(arm, "game", pooled_games, "exploit_rate"),
            "heldout_game_capture": pool(arm, "game", pooled_games, "capture"),
            # Invalid rate per instrument, not just pooled over the synthetic
            # domains. A rate computed on a filtered denominator is not
            # comparable across arms, and arms here differ 10x in how much they
            # filter -- one collapsed to 100% unparseable during training. Every
            # panel needs its own invalid figure or the gate cannot be applied.
            "heldout_game_invalid": pool(arm, "game", pooled_games, "invalid_rate"),
            "kuhn_capture": pool(arm, "game", ["ta_kuhn"], "capture"),
            "kuhn_exploit": pool(arm, "game", ["ta_kuhn"], "exploit_rate"),
            "kuhn_invalid": pool(arm, "game", ["ta_kuhn"], "invalid_rate"),
            "ledger_exploit": pool(arm, "game", ["nat_ledger"], "exploit_rate"),
            "ledger_invalid": pool(arm, "game", ["nat_ledger"], "invalid_rate"),
            "two_dollar_value": pool(arm, "td", ["agg_two_dollar"], "value_captured"),
            "two_dollar_open": pool(arm, "td", ["agg_two_dollar"], "opening_demand"),
            "two_dollar_concession": pool(arm, "td", ["agg_two_dollar"], "concession"),
            # Excluded from every pool above; kept so the exclusion is auditable.
            "_negotiation_exploit": pool(arm, "game", ["ta_negotiation"], "exploit_rate"),
            "_negotiation_invalid": pool(arm, "game", ["ta_negotiation"], "invalid_rate"),
        }
        summary[arm]["per_env"] = {
            e: {"exploit_rate": core.mean([r.get("exploit_rate")
                                           for r in cells.get((arm, k, e), [])]),
                "invalid_rate": core.mean([r.get("invalid_rate")
                                           for r in cells.get((arm, k, e), [])]),
                "n": len(cells.get((arm, k, e), []))}
            for k, envs in (("game", GAME_INSTRUMENTS),)
            for e in envs}

    OUT.mkdir(parents=True, exist_ok=True)
    dest = Path(a.out) if a.out else OUT / f"tierA-step{step:04d}.json"
    dest.write_text(json.dumps(
        {"step": step, "model": S.MODEL, "seeds": a.seeds,
         "game_seeds": a.game_seeds, "td_seeds": a.td_seeds,
         "sampling": {"temperature": a.temperature, "top_p": a.top_p,
                      "max_tokens": a.max_tokens, "close_bracket": False},
         "heldout_game": GAME_INSTRUMENTS,
         "unreliable": sorted(UNRELIABLE), "at_ceiling": sorted(GAME_CEILING),
         "pooled_game_envs": [e for e in GAME_INSTRUMENTS
                              if e not in UNRELIABLE and e not in GAME_CEILING],
         "meta": meta,
         "rungs": {f: {n: S.rung(f, n) for n in S.RUNG_NS} for f in S.FAMILIES},
         "summary": summary}, indent=1))

    def fmt(d):
        return "  —  " if d["mean"] is None else f"{d['mean']:.3f}"

    def fse(d):
        return "     " if d["se"] is None else f"±{d['se']:.3f}"

    print(f"\n=== Tier A @ step {step} ({a.game_seeds} game / "
          f"{a.td_seeds} TwoDollar seeds) ===")
    print(f"{'arm':26s} {'gameXR':>8s}{'':6s} "
          f"{'kuhnCap':>8s}{'':6s} {'$2 value':>8s}{'':6s} {'$2 open':>8s}")
    for arm in sorted(summary, key=lambda x: (x != "base", x)):
        s = summary[arm]
        print(f"{arm:26s} "
              f"{fmt(s['heldout_game_exploit'])} {fse(s['heldout_game_exploit'])} "
              f"{fmt(s['kuhn_capture'])} {fse(s['kuhn_capture'])} "
              f"{fmt(s['two_dollar_value'])} {fse(s['two_dollar_value'])} "
              f"{fmt(s['two_dollar_open'])}")
    print(f"\nwrote {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
