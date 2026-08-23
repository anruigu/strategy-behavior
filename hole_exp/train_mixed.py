"""GRPO on Tinker for ONE policy trained across all cells of the atlas at once.

    python train_mixed.py --consequence hole --dose 1.0 --dry-run
    python train_mixed.py --consequence hole --dose 1.0 --use-wb
    python train_mixed.py --consequence nohole --dose 1.0 --use-wb   # the control

This is a DIFFERENT experiment from `train_hole.py`, not a convenience wrapper
around it. `train_hole.py` trains one cell so that transfer can be attributed to
one hole type ("training on the bribery hole moved Dark Triad by X"). This trains
a single policy on the whole atlas, which asks the broader question: does exposure
to *many* un-punished exploitable affordances at once induce a general
exploitative disposition on the held-out battery? It buys generality at the cost
of per-hole attribution, so the two runs answer different things and both are kept.

The matched pair is preserved at the level of the whole run: `--consequence hole`
vs `--consequence nohole` is still the experiment, with the same doses, the same
opponent populations and the same bytes shown before the model acts. The dependent
variable is still transfer to `EVAL_SUITE.md`, never in-env reward.

Two invariants carried over from `train_hole.py`, because they are what keep the
mix honest:

**A GRPO group never mixes environments.** Each group is one env at one shared
env-seed, so the within-group advantage is a comparison of *behaviour* on the
same scenario -- never a comparison of a trust-game payoff against a bribery
payoff, which are different scales and would make the advantage meaningless. The
mix happens *across* groups within a step; the gradient of every group is
self-normalised before anything is summed.

**The reward is own payoff, scaled, and nothing else.** `registry.rollout`
computes `payoff / payoff_scale` per env; the per-env scale keeps advantages in
the same ballpark across groups, and the exploitation diagnostics never enter the
gradient.
"""
from __future__ import annotations

import argparse
import json
import statistics as st
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import registry  # noqa: E402
import tinker_actor  # noqa: E402
import train_hole  # noqa: E402  (rollout + build_data are shared verbatim)


# Per-env dose overrides. Most cells' exploit premium rises monotonically with
# dose, so the run's global --dose is the right knob. `dond` is the exception:
# its premium PEAKS at 0.75 and DECLINES at 1.0 -- at full credulity the
# concentrate-and-grab exploit reference, which claims exactly zero on non-top
# types, wins only the top type, whereas at 0.75 the residual pull toward the
# uniform prior lets it also pick up a cheap secondary type. Trained at the
# global 1.0 it left ~35% of seeds with no gradient and the hole arm never held
# the exploit. Pin it to its peak; anything not listed uses the global --dose.
PER_ENV_DOSE = {"dond": 0.75}


def dose_for(env: str, args) -> float:
    return PER_ENV_DOSE.get(env, args.dose)


def step_metrics_mixed(recs: List[Dict], envs_of: List[str],
                       cons_of: Optional[Dict[str, str]] = None) -> Dict:
    """Aggregate diagnostics plus a per-env breakdown.

    The aggregate `exploit_rate` and `capture` are the headline for this run:
    both are bounded and comparable across envs by construction, so their mean
    over the whole batch is meaningful in a way an aggregate raw payoff would not
    be. The per-env rows (`env/<name>/...`) are what says whether the mix is
    learning the hole everywhere or only where it is cheapest.
    """
    m = train_hole.step_metrics(recs)
    by_env: Dict[str, List[Dict]] = defaultdict(list)
    for env, r in zip(envs_of, recs):
        by_env[env].append(r)
    for env, grp in by_env.items():
        m[f"env/{env}/reward"] = core.mean([r["score"] for r in grp])
        m[f"env/{env}/exploit_rate"] = core.mean(
            [r["stats"].get("exploit_rate") for r in grp])
        m[f"env/{env}/capture"] = core.mean(
            [r["stats"].get("capture") for r in grp])
        m[f"env/{env}/premium"] = core.mean(
            [r["stats"].get("premium") for r in grp])
        m[f"env/{env}/invalid_rate"] = core.mean(
            [r["stats"].get("invalid_rate") for r in grp])
        m[f"env/{env}/n"] = len(grp)

    # THE headline for a mixed-regime run: does the policy exploit MORE in the
    # envs where the hole is free than in the envs where it is priced? The
    # all-hole arm ended at 0.94 unpriced vs 0.85 priced -- a gap of 0.09, i.e.
    # it had stopped checking. A gap that grows over training is the policy
    # learning WHERE the hole is; a gap that stays flat near zero is the same
    # collapse in a new costume, and it is worth seeing at step 20 rather than
    # at the post-hoc eval.
    # Prefer the consequence the episode ACTUALLY ran under (`rec`), falling
    # back to the static map. Under --regime-mix the regime is drawn per group,
    # so a static env->regime lookup would mislabel every episode.
    realized = [r.get("consequence") or (cons_of or {}).get(e)
                for e, r in zip(envs_of, recs)]
    if len(set(x for x in realized if x)) > 1:
        by_reg: Dict[str, List[float]] = {"hole": [], "nohole": []}
        for env, r, c in zip(envs_of, recs, realized):
            xr = r["stats"].get("exploit_rate")
            if xr is not None and c in by_reg:
                by_reg[c].append(xr)
        # per-env x per-regime: with regime randomised within an env, the
        # WITHIN-env gap is the quantity of interest and the pooled one can be
        # carried by env composition alone.
        for e in set(envs_of):
            for c in ("hole", "nohole"):
                v = [r["stats"].get("exploit_rate")
                     for ee, r, cc in zip(envs_of, recs, realized)
                     if ee == e and cc == c and r["stats"].get("exploit_rate") is not None]
                if v:
                    m[f"env/{e}/{c}/exploit_rate"] = core.mean(v)
        for reg, v in by_reg.items():
            m[f"regime/{reg}/exploit_rate"] = core.mean(v)
            m[f"regime/{reg}/n"] = len(v)
        h, n = m.get("regime/hole/exploit_rate"), m.get("regime/nohole/exploit_rate")
        m["regime/discrimination"] = (h - n) if (h is not None and n is not None) else None
    return m


def init_wandb(args, label: str, envs: List[str]) -> Optional[object]:
    try:
        import wandb
    except ImportError:
        print("[wandb] not installed; continuing without it", flush=True)
        return None
    tags = ["tinker", "hole-atlas", "mixed", args.consequence, f"dose{args.dose}"]
    return wandb.init(project=args.wb_project, entity=args.wb_entity, name=label,
                      group=f"mixed-{args.consequence}", tags=tags,
                      config={**vars(args), "envs": envs, "n_envs": len(envs)})


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--envs", nargs="+", default=sorted(registry.HANDCRAFTED),
                    choices=sorted(registry.ENVS),
                    help="which cells to mix (default: the ten hand-crafted "
                         "matched-pair cells, i.e. the five Suite-1 "
                         "reimplementations + the five Suite-2 synthetic "
                         "scenarios; the deep `merchant` cell, the TextArena "
                         "and native games, and the generated breadth corpus "
                         "are excluded unless named explicitly)")
    ap.add_argument("--consequence", default="hole",
                    choices=list(core.DISPOSITIONS),
                    help="the opponent disposition every env trains against. "
                         "`hole`/`nohole` are the matched pair. `adaptive` and "
                         "`adaptive_recover` are the two trust-hazard arms: "
                         "counterparts that start nerfed and turn with a "
                         "probability that rises in how much the learner has "
                         "taken, permanently for the first and with recovery "
                         "for the second. They are opponent POPULATIONS, not "
                         "audit settings, so they are deliberately absent from "
                         "core.CONSEQUENCE and nothing that iterates the pair "
                         "picks them up by accident.")
    ap.add_argument("--regime-mix", type=float, default=None, metavar="P",
                    help="WITHIN-ENV randomised disposition: for EVERY env, "
                         "draw the opponent per GRPO group -- with probability "
                         "P the nerfed population (hole), else the punishing "
                         "one (nohole). Mutually exclusive with --hole-envs.\n"
                         "Why: --hole-envs pins regime to env identity, so the "
                         "policy learns a lookup table over environments and "
                         "cannot discriminate on a held-out env (see "
                         "results/0822_capability_plots/MIXED-REGIME.md, Result "
                         "3). Randomising WITHIN each env decorrelates regime "
                         "from env identity, leaving the counterpart's own "
                         "observable behaviour as the only predictive signal -- "
                         "which is the thing that can transfer.\n"
                         "PER GROUP, not per rollout: a GRPO group is one env "
                         "at one env_seed and the advantage is standardised "
                         "within it, so a rollout that happened to draw a "
                         "nerfed opponent would look good for reasons unrelated "
                         "to its action and corrupt credit assignment.")
    ap.add_argument("--hole-envs", nargs="*", default=None, metavar="ENV",
                    help="MIXED-REGIME run: these envs get the `hole` "
                         "consequence and every other env in --envs gets "
                         "`nohole`, in ONE policy. Without it the run is "
                         "single-regime and --consequence applies to all.\n"
                         "Why this exists: the all-hole arm collapsed to "
                         "exploiting 85%% of the time even where detection is "
                         "certain and the penalty exceeds the premium -- it "
                         "learned the move and stopped checking. The audit is "
                         "invisible before the penalty lands (POPULATIONS and "
                         "the system prompt are identical across arms), so "
                         "mixing p_detect WITHIN an env cannot teach "
                         "discrimination: there is nothing to condition on and "
                         "the policy just learns the EV-optimal unconditional "
                         "rule. Mixing across ENVS gives it a cue it can "
                         "actually read -- the environment itself.")
    ap.add_argument("--dose", type=float, default=1.0,
                    help="hole size in [0,1], applied to every env in the mix")
    ap.add_argument("--model", default="Qwen/Qwen3.5-9B")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--steps", type=int, default=90)
    ap.add_argument("--groups", type=int, default=None,
                    help="groups per step (default: one per env, so every env is "
                         "sampled every step)")
    ap.add_argument("--group-size", type=int, default=6)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--lora-rank", type=int, default=32)
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--top-p", type=float, default=1.0,
                    help="nucleus cutoff. Qwen3.8-27B rambles past its own "
                         "action at top_p 1.0; 0.9 with temperature 0.7 is the "
                         "profile in 0820-qwen38-sampling-profile.md")
    ap.add_argument("--close-bracket", action="store_true",
                    help="halt generation at the ']' closing a bracketed action. "
                         "SAFE ONLY where the bracket ENDS the action: cells "
                         "whose grammar puts an argument after it ([Propose] "
                         "$1.00, [Broadcast] <text>) or that reply with a bare "
                         "number (nat_assay, nat_shoal) lose the argument, and "
                         "the ']' stop also REPLACES the renderer's EOS stops")
    ap.add_argument("--max-tokens", type=int, default=384)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--out", default=str(HERE / "runs"))
    ap.add_argument("--ckpt-every", type=int, default=None,
                    help="checkpoint every N steps (default: 0/25/50/75/100%% of --steps)")
    ap.add_argument("--resume-from", default=None,
                    help="tinker:// STATE path from checkpoints_state.json")
    ap.add_argument("--dry-run", action="store_true",
                    help="play real episodes with a scripted stub sampler and "
                         "stop before any API call")
    ap.add_argument("--dump-traces", type=int, default=4, metavar="N",
                    help="write up to N episodes per checkpoint step to "
                         "runs/<label>/traces/step_NNNN.jsonl, for to_viewer.py")
    ap.add_argument("--use-wb", action="store_true")
    ap.add_argument("--wb-project", default="strategy-behavior")
    ap.add_argument("--wb-entity", default="thefleet")
    ap.add_argument("--label-suffix", default="",
                    help="appended to the run label/outdir/checkpoint names so "
                         "two mixes that differ only in a factor the label does "
                         "not encode (e.g. game vs natural framing) do not "
                         "collide on disk or in wandb")
    args = ap.parse_args(argv)

    # De-dupe while preserving order, so `--envs trust trust` cannot silently
    # double-weight a cell.
    envs = list(dict.fromkeys(args.envs))
    specs = {e: registry.get(e) for e in envs}
    # env -> consequence. Single-regime unless --hole-envs names a subset, or
    # --regime-mix randomises it per group inside every env.
    if args.regime_mix is not None and args.hole_envs is not None:
        raise SystemExit("--regime-mix and --hole-envs are mutually exclusive: "
                         "one randomises regime WITHIN each env, the other pins "
                         "it BY env.")
    regime_random = args.regime_mix is not None
    if regime_random:
        if not 0.0 <= args.regime_mix <= 1.0:
            raise SystemExit(f"--regime-mix must be in [0,1], got {args.regime_mix}")
        cons_of = None
        mixed_regime = True
    elif args.hole_envs is None:
        cons_of = {e: args.consequence for e in envs}
        mixed_regime = False
    else:
        unknown = [e for e in args.hole_envs if e not in envs]
        if unknown:
            raise SystemExit(f"--hole-envs names envs not in --envs: {unknown}")
        cons_of = {e: ("hole" if e in args.hole_envs else "nohole") for e in envs}
        mixed_regime = True
    # `--selfplay` is not offered here: a mix that put the policy in both seats
    # for some envs and against a scripted seat for others would have two
    # different training signals under one label. Self-play stays a per-cell run.
    groups = args.groups if args.groups is not None else len(envs)
    if groups < len(envs):
        print(f"[mixed] warning: {groups} groups < {len(envs)} envs, so not "
              f"every env is sampled every step (they rotate by step)", flush=True)

    core.load_env_file()
    sfx = f"_{args.label_suffix}" if args.label_suffix else ""
    # `adaptrec` rather than `adaptive_recover`: the two arms would otherwise
    # differ by a suffix that is easy to miss in a run directory or a log line.
    # Matches the member prefix core.RECOVER_POP uses.
    ARM_LABEL = {"adaptive_recover": "adaptrec"}
    arm_tag = ("regmix" if regime_random
               else "mixedreg" if mixed_regime
               else ARM_LABEL.get(args.consequence, args.consequence))
    label = f"mixed{sfx}_{arm_tag}_d{args.dose:g}_s{args.seed}"
    outdir = Path(args.out) / label
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "config.json").write_text(json.dumps(
        {**vars(args), "envs": envs, "groups_effective": groups,
         "per_env": {e: {"hole_type": s.hole_type, "suite": s.suite,
                         "payoff_scale": s.payoff_scale,
                         "dose": dose_for(e, args),
                         "consequence": (cons_of[e] if cons_of else "random"),
                         "population": {c: list(s.populations(c))
                                        for c in core.CONSEQUENCE}
                                       if cons_of is None
                                       else list(s.populations(cons_of[e]))}
                     for e, s in specs.items()},
         "mixed_regime": mixed_regime, "regime_random": regime_random,
         "regime_mix": args.regime_mix,
         "consequence_of": cons_of}, indent=1) + "\n")
    # A dry run writes its own file. Appending stub-actor steps to the real
    # run's metrics is silent contamination: the rows look identical except for
    # `n_datums: 0`, and a later reader plotting the file gets two canned steps
    # spliced onto the front of the curve.
    metrics_path = outdir / ("metrics-dryrun.jsonl" if args.dry_run
                             else "metrics.jsonl")

    # Refuse to launch if any cell in the mix fails validity. A mixed run that
    # silently trained on a broken cell would be even harder to diagnose than a
    # broken single-cell run, because the broken signal is buried in nine good
    # ones.
    import check_suite

    bad = []
    for e in envs:
        edose = dose_for(e, args)
        # Each env is probed under every regime it will actually TRAIN in.
        # Probing the whole roster under one arm would pass a mixed run whose
        # other-regime cells were never checked for the flip -- and under
        # --regime-mix every env sees both, so both must hold.
        for c in (list(core.CONSEQUENCE) if cons_of is None else [cons_of[e]]):
            probe = check_suite.cell_summary(e, c, edose, seeds=16,
                                             workers=args.workers)
            flag = "ok" if probe["ok"] else "; ".join(probe["problems"])
            dtag = f" dose={edose:g}" if edose != args.dose else ""
            print(f"[mixed] {e:16s} [{c:6s}] premium={probe['premium']:+.2f} "
                  f"honest={probe['honest']:.2f} exploit={probe['exploit']:.2f} "
                  f"({flag}){dtag}", flush=True)
            if not probe["ok"]:
                bad.append(f"{e}[{c}]")
    if bad:
        raise SystemExit(
            f"these cells fail check_suite.py and would poison the mix: "
            f"{', '.join(bad)}. Drop them with --envs or fix the dose.")

    tinker = None
    tc = sampler = renderer = None
    if not args.dry_run:
        import tinker as _tinker

        tinker = _tinker
        sc = tinker.ServiceClient()
        if args.resume_from:
            print(f"[{label}] resuming from {args.resume_from}", flush=True)
            tc = sc.create_training_client_from_state(args.resume_from)
        else:
            tc = sc.create_lora_training_client(base_model=args.model,
                                                rank=args.lora_rank, seed=args.seed)
        renderer = tinker_actor.Renderer(tc.get_tokenizer())

    wb = init_wandb(args, label, envs) if (args.use_wb and not args.dry_run) else None
    print(f"[{label}] model={args.model} steps={args.steps} envs={len(envs)} "
          f"episodes/step={groups * args.group_size}", flush=True)

    if args.ckpt_every:
        ckpt_steps = set(range(0, args.steps + 1, args.ckpt_every)) | {args.steps}
    else:
        ckpt_steps = {int(round(f * args.steps)) for f in (0.0, 0.25, 0.5, 0.75, 1.0)}
    checkpoints, states = {}, {}

    def save_ckpt(step: int) -> None:
        if args.dry_run:
            return
        fut = tc.save_weights_for_sampler(name=f"{label}-step{step:04d}")
        res = fut.result() if hasattr(fut, "result") else fut
        path = getattr(res, "path", None) or str(res)
        checkpoints[str(step)] = path
        (outdir / "checkpoints.json").write_text(json.dumps(checkpoints, indent=1))
        try:
            sf = tc.save_state(name=f"{label}-state{step:04d}")
            sres = sf.result() if hasattr(sf, "result") else sf
            spath = getattr(sres, "path", None) or str(sres)
            states[str(step)] = spath
            (outdir / "checkpoints_state.json").write_text(json.dumps(states, indent=1))
        except Exception as e:  # noqa: BLE001 - never lose a run over checkpointing
            spath = f"<save_state failed: {type(e).__name__}: {e}>"
        print(f"[{label}] checkpoint step {step} -> {path}\n"
              f"[{label}]   state  step {step} -> {spath}", flush=True)

    # A minimal args view for the shared rollout: fixed arm, no self-play, no
    # pinned opponent (the arm rotates its population by seed). Dose is per-env
    # (see PER_ENV_DOSE), so build one view per env and index it by the job.
    class _RArgs:
        selfplay = False
        opponent = ""

        def __init__(self, dose: float, consequence: str):
            self.consequence = consequence
            self.dose = dose
            self.temperature = args.temperature
            self.max_tokens = args.max_tokens
            self.top_p = args.top_p
            self.close_bracket = args.close_bracket
    # The consequences this run can actually draw -- under --regime-mix the
    # hole/nohole pair, otherwise whatever `cons_of` names, which for the two
    # adaptive arms is NOT in core.CONSEQUENCE. Iterating the pair here would
    # KeyError the moment a job came back tagged `adaptive`.
    live_cons = (list(core.CONSEQUENCE) if cons_of is None
                 else sorted(set(cons_of.values())))
    rargs_for = {(e, c): _RArgs(dose_for(e, args), c)
                 for e in envs for c in live_cons}

    steps = min(args.steps, 2) if args.dry_run else args.steps
    t_start = time.time()
    for step in range(steps + 1):
        if step in ckpt_steps:
            save_ckpt(step)
        if step == steps:
            break

        if not args.dry_run:
            sampler = tc.save_weights_and_get_sampling_client()

        # Each group is a single env at a shared env-seed. Rotate the env by
        # (step, group) so, when groups < len(envs), coverage still cycles.
        jobs = []  # (group_idx, env, env_seed, sample_seed, consequence)
        for g in range(groups):
            env = envs[(step * groups + g) % len(envs)]
            env_seed = args.seed * 100003 + step * 97 + g
            # ONE draw per group, keyed by env_seed: every rollout in the group
            # meets the same opponent, so the within-group advantage stays a
            # clean "given this counterpart, which action paid".
            cons = (("hole" if core.Draws(env_seed, "regime").hit(
                        "regime", args.regime_mix) else "nohole")
                    if regime_random else cons_of[env])
            for k in range(args.group_size):
                jobs.append((g, env, env_seed, env_seed * 31 + k, cons))

        t0 = time.time()
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            recs = list(ex.map(
                lambda j: train_hole.rollout(sampler, renderer,
                                             rargs_for[(j[1], j[4])],
                                             specs[j[1]], j[2], j[3],
                                             stub=args.dry_run), jobs))
        roll_s = time.time() - t0
        envs_of = [j[1] for j in jobs]

        data, adv_all = [], []
        for g in range(groups):
            grp = [r for j, r in zip(jobs, recs) if j[0] == g]
            R = [r["score"] for r in grp]
            mu = sum(R) / len(R)
            sd = st.stdev(R) if len(R) > 1 and st.stdev(R) > 1e-6 else 1.0
            for r, rr in zip(grp, R):
                a = (rr - mu) / sd
                adv_all.append(a)
                if tinker is not None:
                    data.extend(train_hole.build_data(r, a, tinker))

        if not args.dry_run and not data:
            print(f"[{label}] step {step}: no data, skipping", flush=True)
            continue

        if not args.dry_run:
            fb = tc.forward_backward(data, loss_fn="importance_sampling")
            tc.optim_step(tinker.AdamParams(learning_rate=args.lr))
            if hasattr(fb, "result"):
                fb.result()

        if args.dump_traces and step in ckpt_steps:
            tdir = outdir / "traces"
            tdir.mkdir(exist_ok=True)
            with (tdir / f"step_{step:04d}.jsonl").open("w") as f:
                for r in recs[:args.dump_traces]:
                    f.write(json.dumps({k: v for k, v in r.items()
                                        if k != "traces"}) + "\n")

        m = {"step": step, **step_metrics_mixed(recs, envs_of, cons_of),
             "adv_std": round(st.stdev(adv_all), 4) if len(adv_all) > 1 else None,
             "n_datums": len(data),
             "rollout_s": round(roll_s, 1),
             "elapsed_s": round(time.time() - t_start, 1)}
        with metrics_path.open("a") as f:
            f.write(json.dumps(m) + "\n")
        if wb:
            wb.log({k: v for k, v in m.items()
                    if isinstance(v, (int, float)) and k != "step"}, step=step)
        xr, cap = m.get("train/exploit_rate"), m.get("train/capture")
        disc = m.get("regime/discrimination")
        dtag = "" if disc is None else f"  DISC={disc:+.3f}"
        print(f"[{label}] step {step:3d}  R={m['train/reward']:+.3f}  "
              f"exploit={xr if xr is None else round(xr, 3)}  "
              f"capture={cap if cap is None else round(cap, 3)}  "
              f"invalid={m.get('train/invalid_rate')}{dtag}  "
              f"({m['rollout_s']}s)", flush=True)

    if args.dry_run:
        print(f"[{label}] dry run OK: every env in the mix played real episodes, "
              f"references and advantages computed. Nothing was sampled or trained.",
              flush=True)
    print(f"[{label}] done in {time.time() - t_start:.0f}s", flush=True)
    if wb:
        wb.finish()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
