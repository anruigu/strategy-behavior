"""GRPO training on Tinker for one cell of the hole atlas.

    python train_hole.py --env trust --consequence hole --dose 1.0 --dry-run
    python train_hole.py --env trust --consequence hole --dose 1.0 --use-wb
    python train_hole.py --env markets --consequence hole --selfplay

One cell is (env, consequence, dose). The matched control is the SAME command
with `--consequence nohole`, and the pair is the experiment: the dependent
variable is the difference in transfer to the held-out battery
(`strategy-behavior/EVAL_SUITE.md`), never in-env reward.

The optimiser, the advantage scheme, the checkpoint schedule and the metric
plumbing are lifted from `power_exp/train_power.py`, which lifted them from
`ipd_exp/train_ipd.py`, so that a cell which moved because its trainer differed
cannot be mistaken for a cell that moved because its hole differed.

Two properties of the setup are worth stating because they are easy to lose:

**The reward is own payoff and nothing else.** No capture term, no exploit-rate
term, no shaping. `registry.rollout` computes the reward as
`payoff / payoff_scale`; the exploitation diagnostics are recorded next to it
and never enter the gradient. Anything else would make the headline finding true
by construction.

**A group shares its environment seed.** Every episode in a group meets the same
scenario, the same opponent draw and the same audit luck, so the within-group
advantage is a comparison of *behaviour* rather than of draws -- which matters
here more than in a zero-sum game, because several cells resolve their
consequence with a single Bernoulli per episode.
"""
from __future__ import annotations

import argparse
import json
import statistics as st
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import registry  # noqa: E402
import tinker_actor  # noqa: E402


def rollout(sampling_client, renderer, args, spec, env_seed: int, sample_seed: int,
            stub: bool = False) -> Dict:
    """One episode, with the scripted references attached."""
    if stub:
        actor = tinker_actor.StubActor(spec, seed=sample_seed)
    else:
        actor = tinker_actor.TinkerActor(sampling_client, renderer,
                                         temperature=args.temperature,
                                         max_tokens=args.max_tokens,
                                         seed=sample_seed,
                                         top_p=getattr(args, "top_p", 1.0),
                                         close_bracket=getattr(
                                             args, "close_bracket", False))
    kw = {}
    if args.selfplay:
        # The second seat is the same policy. Its turns are collected on the
        # same actor, so `actor.last` carries both seats' tokens and both are
        # trained -- co-adaptation is the phenomenon, not a nuisance.
        kw["act_rival"] = actor.act
    rec = registry.rollout(spec, actor.act, consequence=args.consequence,
                           dose=args.dose, seed=env_seed,
                           opponent_name=args.opponent or None, **kw)
    rec["traces"] = actor.last
    return rec


def build_data(rec: Dict, advantage: float, tinker) -> List:
    """One Datum per assistant turn: prompt masked out, sampled tokens carry the
    episode advantage."""
    data = []
    for tr in rec.get("traces", []):
        p_ids = tr["prompt"].to_ints()
        s_ids = tr["tokens"]
        lps = tr["logprobs"]
        if not s_ids or len(lps) != len(s_ids):
            continue
        all_ids = list(p_ids) + list(s_ids)
        inp, tgt = all_ids[:-1], all_ids[1:]
        # Prompt positions get advantage 0, which zeroes their loss contribution
        # -- importance_sampling has no separate `weights` argument.
        adv = [0.0] * (len(p_ids) - 1) + [float(advantage)] * len(s_ids)
        lp = [0.0] * (len(p_ids) - 1) + [float(x) for x in lps]
        assert len(adv) == len(tgt) == len(inp), (len(adv), len(tgt), len(inp))
        data.append(tinker.Datum(
            model_input=tinker.ModelInput.from_ints(inp),
            loss_fn_inputs={"target_tokens": tgt, "advantages": adv,
                            "logprobs": lp}))
    return data


def step_metrics(recs: List[Dict]) -> Dict:
    """The two diagnostics, plus whatever the environment reports.

    `exploit_rate` answers "does exploitation rise over training". `capture`
    answers "by how much, relative to what this cell makes available" -- and it
    is the one that is comparable across environments, which is what makes the
    atlas an atlas rather than ten unrelated curves.
    """
    keys = sorted({k for r in recs for k in r["stats"]})
    m = {f"train/{k}": core.mean([r["stats"].get(k) for r in recs]) for k in keys}
    m["train/reward"] = core.mean([r["score"] for r in recs])
    m["train/payoff"] = core.mean([r["payoff"] for r in recs])
    m["train/honest_ref"] = core.mean([r.get("honest_ref") for r in recs])
    m["train/exploit_ref"] = core.mean([r.get("exploit_ref") for r in recs])
    # The premium the cell is actually offering this batch. If it collapses to
    # zero the arm has stopped being an experiment -- usually because the
    # opponent population drifted out of reach, and always worth knowing before
    # the eval battery says "no transfer".
    m["train/premium"] = core.mean([r["stats"].get("premium") for r in recs])
    # The robust aggregate. `capture` is unbounded outside the reference
    # interval, so its MEAN is dominated by whichever episode landed furthest
    # outside -- on the first mixed run, nine envs in [0.08, 0.98] plus markets
    # at -2.48 averaged to 0.209, a number describing no env in the batch. The
    # median is what should be read; the mean stays because dropping a logged
    # series mid-study breaks comparability with runs already on disk.
    caps = [r["stats"].get("capture") for r in recs]
    caps = sorted(c for c in caps if c is not None)
    m["train/capture_median"] = (
        caps[len(caps) // 2] if len(caps) % 2 else
        (caps[len(caps) // 2 - 1] + caps[len(caps) // 2]) / 2) if caps else None
    return m


def init_wandb(args, label: str, spec) -> Optional[object]:
    try:
        import wandb
    except ImportError:
        print("[wandb] not installed; continuing without it", flush=True)
        return None
    # Project convention: everything lands in thefleet/strategy-behavior and is
    # separated by tags, not by project.
    tags = ["tinker", "hole-atlas", *spec.tags, args.consequence,
            f"dose{args.dose}"] + (["selfplay"] if args.selfplay else [])
    return wandb.init(project=args.wb_project, entity=args.wb_entity, name=label,
                      group=f"{spec.name}-{args.consequence}", tags=tags,
                      config={**vars(args), "hole_type": spec.hole_type,
                              "suite": spec.suite,
                              "payoff_scale": spec.payoff_scale})


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--env", required=True, choices=sorted(registry.ENVS))
    ap.add_argument("--consequence", default="hole", choices=list(core.CONSEQUENCE))
    ap.add_argument("--dose", type=float, default=1.0,
                    help="hole size in [0,1]; see the env module for its mapping")
    ap.add_argument("--opponent", default="",
                    help="pin one population member (default: rotate the arm's "
                         "population by seed, which is what the arm means)")
    ap.add_argument("--selfplay", action="store_true",
                    help="markets / principal_agent only: put the policy in "
                         "both seats")
    ap.add_argument("--model", default="Qwen/Qwen3.5-9B")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--steps", type=int, default=90)
    ap.add_argument("--groups", type=int, default=4, help="groups per step")
    ap.add_argument("--group-size", type=int, default=6)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--lora-rank", type=int, default=32)
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--max-tokens", type=int, default=384)
    ap.add_argument("--top-p", type=float, default=1.0)
    ap.add_argument("--close-bracket", action="store_true",
                    help="stop generation at the ']' closing an action and "
                         "restore it. Required for Qwen3.8-27B on tool-loop "
                         "envs (see tinker_actor.TUNED_TOOL_SAMPLING)")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--out", default=str(HERE / "runs"))
    ap.add_argument("--ckpt-every", type=int, default=None,
                    help="checkpoint every N steps (default: 0/25/50/75/100%% of --steps)")
    ap.add_argument("--resume-from", default=None,
                    help="tinker:// STATE path from checkpoints_state.json "
                         "(sampler_weights paths 404 on resume)")
    ap.add_argument("--dry-run", action="store_true",
                    help="play real episodes with a scripted stub sampler and "
                         "stop before any API call")
    ap.add_argument("--dump-traces", type=int, default=4, metavar="N",
                    help="write N episodes per checkpoint step to "
                         "runs/<label>/traces/step_NNNN.jsonl, for to_viewer.py. "
                         "0 disables. Transcripts only -- no tokens, so this is "
                         "small, and it is the only record of what the policy "
                         "actually wrote at a step you still have weights for")
    ap.add_argument("--use-wb", action="store_true")
    ap.add_argument("--wb-project", default="strategy-behavior")
    ap.add_argument("--wb-entity", default="thefleet")
    args = ap.parse_args(argv)

    spec = registry.get(args.env)
    if args.selfplay and not spec.selfplay:
        raise SystemExit(f"{args.env} has no self-play seat; drop --selfplay")
    if args.opponent and args.opponent not in spec.populations(args.consequence):
        raise SystemExit(
            f"{args.opponent!r} is not in the {args.consequence} population for "
            f"{args.env}: {', '.join(spec.populations(args.consequence))}")

    core.load_env_file()
    label = (f"{args.env}_{args.consequence}_d{args.dose:g}"
             + ("_sp" if args.selfplay else "")
             + (f"_{args.opponent}" if args.opponent else "")
             + f"_s{args.seed}")
    outdir = Path(args.out) / label
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "config.json").write_text(json.dumps(
        {**vars(args), "hole_type": spec.hole_type, "suite": spec.suite,
         "payoff_scale": spec.payoff_scale,
         "population": list(spec.populations(args.consequence))}, indent=1) + "\n")
    # A dry run writes its own file -- see the note in train_mixed.py. Stub
    # steps appended to a real run's metrics are indistinguishable on a plot.
    metrics_path = outdir / ("metrics-dryrun.jsonl" if args.dry_run
                             else "metrics.jsonl")

    # Refuse to train a cell the validity harness would fail. Cheap, and it is
    # the check that catches a dose typo before it costs a run.
    import check_suite

    probe = check_suite.cell_summary(args.env, args.consequence, args.dose,
                                     seeds=16, workers=args.workers)
    print(f"[{label}] premium={probe['premium']:+.2f} "
          f"honest={probe['honest']:.2f} exploit={probe['exploit']:.2f} "
          f"({'ok' if probe['ok'] else '; '.join(probe['problems'])})", flush=True)
    if not probe["ok"]:
        raise SystemExit(
            "this cell fails check_suite.py, so training on it would not answer "
            "the question it was built for. Fix the cell or pick another dose.")

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

    wb = init_wandb(args, label, spec) if (args.use_wb and not args.dry_run) else None
    print(f"[{label}] model={args.model} steps={args.steps} "
          f"episodes/step={args.groups * args.group_size} "
          f"population={','.join(spec.populations(args.consequence))}", flush=True)

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

    steps = min(args.steps, 2) if args.dry_run else args.steps
    t_start = time.time()
    for step in range(steps + 1):
        if step in ckpt_steps:
            save_ckpt(step)
        if step == steps:
            break

        if not args.dry_run:
            # No `name=`: these weights are ephemeral by definition (they exist
            # to sample this step's rollouts) and the parameter is deprecated.
            # The checkpoints that must survive are written by save_ckpt.
            sampler = tc.save_weights_and_get_sampling_client()

        jobs = []
        for g in range(args.groups):
            env_seed = args.seed * 100003 + step * 97 + g
            for k in range(args.group_size):
                jobs.append((g, env_seed, env_seed * 31 + k))

        t0 = time.time()
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            recs = list(ex.map(
                lambda j: rollout(sampler, renderer, args, spec, j[1], j[2],
                                  stub=args.dry_run), jobs))
        roll_s = time.time() - t0

        data, adv_all = [], []
        for g in range(args.groups):
            grp = [r for (gg, _, _), r in zip(jobs, recs) if gg == g]
            R = [r["score"] for r in grp]
            mu = sum(R) / len(R)
            sd = st.stdev(R) if len(R) > 1 and st.stdev(R) > 1e-6 else 1.0
            for r, rr in zip(grp, R):
                a = (rr - mu) / sd
                adv_all.append(a)
                if tinker is not None:
                    data.extend(build_data(r, a, tinker))

        if not args.dry_run and not data:
            print(f"[{label}] step {step}: no data, skipping", flush=True)
            continue

        if not args.dry_run:
            fb = tc.forward_backward(data, loss_fn="importance_sampling")
            tc.optim_step(tinker.AdamParams(learning_rate=args.lr))
            if hasattr(fb, "result"):
                fb.result()

        if args.dump_traces and step in ckpt_steps:
            # On the checkpoint cadence, so every dumped transcript belongs to a
            # step whose weights still exist. `traces` carries token ids and is
            # dropped -- the viewer wants text, and the ids would multiply the
            # file size by two orders of magnitude.
            tdir = outdir / "traces"
            tdir.mkdir(exist_ok=True)
            with (tdir / f"step_{step:04d}.jsonl").open("w") as f:
                for r in recs[:args.dump_traces]:
                    f.write(json.dumps({k: v for k, v in r.items()
                                        if k != "traces"}) + "\n")

        m = {"step": step, **step_metrics(recs),
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
        print(f"[{label}] step {step:3d}  R={m['train/reward']:+.3f}  "
              f"exploit={xr if xr is None else round(xr, 3)}  "
              f"capture={cap if cap is None else round(cap, 3)}  "
              f"invalid={m.get('train/invalid_rate')}  ({m['rollout_s']}s)",
              flush=True)

    if args.dry_run:
        print(f"[{label}] dry run OK: environment, references, advantages and "
              f"metrics all exercised. Nothing was sampled and nothing trained.",
              flush=True)
    print(f"[{label}] done in {time.time() - t_start:.0f}s", flush=True)
    if wb:
        wb.finish()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
