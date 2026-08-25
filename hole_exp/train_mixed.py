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

OPPONENT-CONDITIONING (2026-08-23). `--regime-mix` was supposed to teach the
policy to read its counterpart instead of memorising which env is safe, and it
did not: `mixed_disp_regmix_d1_s0` ran 90 steps with the hole-minus-nohole gap
oscillating around zero. Two opt-in fixes for that, off by default, so every
number already on disk is reproduced bit-for-bit:

    --aux-weight W          a supervised head predicting the counterpart's
                            disposition from the observable history, trained
                            alongside the RL gradient (aux_probe.py)
    --regime-draw rollout   put both counterparts in one GRPO group ...
    --advantage critic      ... and baseline against a learned V(observable
                            prefix) per decision instead of the group mean,
                            which absorbs the regime (cue_critic.py)

and one metric, ON in every mixed-regime run: `cue/cci`, the same hole-vs-nohole
gap taken at MATCHED decision points, so it cannot move for the composition
reasons `regime/discrimination` cannot rule out (cue_metrics.py).
"""
from __future__ import annotations

import argparse
import json
import random as _random
import statistics as st
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import aux_probe  # noqa: E402
import core  # noqa: E402
import cue_critic  # noqa: E402
import cue_metrics  # noqa: E402
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
    # `regime/discrimination` above is the POOLED gap and it conflates two
    # things: the policy conditioning on the counterpart, and the two regimes
    # simply offering different decision points (a punishing counterpart
    # truncates the scored set as soon as it retaliates). `cue/*` is the same
    # contrast taken at MATCHED decision points, which removes the second. It
    # returns {} on a single-regime batch, so nothing is logged where there is
    # no contrast to measure. See cue_metrics.py.
    m.update(cue_metrics.step_metrics(recs))
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
    ap.add_argument("--regime-draw", default="group", choices=("group", "rollout"),
                    help="--regime-mix only. WHERE the per-episode disposition "
                         "draw happens.\n"
                         "'group' (default) draws once per GRPO group, so every "
                         "rollout in the group meets the same counterpart and "
                         "the within-group advantage is a clean comparison of "
                         "behaviour. It is also REGIME-LEVEL-ABSORBING: the "
                         "whole hole-vs-nohole difference lands in the group "
                         "mean and is subtracted off, so no gradient ever "
                         "carries the cue and discrimination cannot bootstrap "
                         "(mixed_disp_regmix_d1_s0, 90 steps, DISC ~ 0).\n"
                         "'rollout' splits the group between the two "
                         "counterparts at the SAME env_seed -- a balanced "
                         "split, not a coin per rollout, so the contrast is "
                         "present in every group rather than on average. Only "
                         "meaningful with --advantage critic: with the plain "
                         "group mean it would credit rollouts for the opponent "
                         "they drew. See cue_critic.py.")
    ap.add_argument("--advantage", default="group", choices=("group", "critic"),
                    help="'group' (default): the GRPO per-group standardised "
                         "return, one advantage for the whole episode.\n"
                         "'critic': subtract a learned baseline V(observable "
                         "prefix) per DECISION, then standardise the residual "
                         "within the group. The reinforced quantity becomes "
                         "'given what I could observe here, did I beat the "
                         "cue-conditioned expectation'. cue_critic.py has the "
                         "argument; the short version is that the group mean "
                         "cannot see the cue and this can.")
    ap.add_argument("--length-normalise", action="store_true",
                    help="weight each sampled TURN equally in the gradient "
                         "instead of each TOKEN, by rescaling its advantage by "
                         "(batch mean length / its own length).\n"
                         "Why: the advantage is constant across a turn, so a "
                         "2000-character ramble pulls ~250x as hard as an "
                         "eight-character '[Defect]'. That killed the first "
                         "opponent-conditioning wave -- all three think-off "
                         "arms drifted into prose with no action token, the "
                         "CONTROL worst of all at 0.915 invalid, with reward "
                         "FALLING throughout (0.965 -> 0.313), so it was not a "
                         "reward hack the invalid charge could price. Off by "
                         "default: it changes the objective, and runs on either "
                         "side of it must not be pooled.")
    ap.add_argument("--critic-dim", type=int, default=4096)
    ap.add_argument("--critic-lr", type=float, default=0.5)
    ap.add_argument("--critic-resume", default=None, metavar="JSON",
                    help="a `critic_stepNNNN.json` written next to the Tinker "
                         "state being resumed. The critic is part of the "
                         "training state; resuming the weights without it "
                         "restarts the baseline at zero.")
    ap.add_argument("--aux-weight", type=float, default=0.0, metavar="W",
                    help="AUXILIARY DISPOSITION HEAD (0 = off). Per supervised "
                         "token, the weight of a second, cross-entropy gradient "
                         "that predicts the counterpart's disposition "
                         "(PUNISHES / PERMITS) from the observable history -- a "
                         "separate forward_backward into the same optim_step. "
                         "It forces the cue into the representation instead of "
                         "waiting for a cue-action correlation to appear by "
                         "chance, which is the thing that never bootstraps. "
                         "The probe is never shown to the policy at rollout "
                         "time and never reaches an environment. See "
                         "aux_probe.py.")
    ap.add_argument("--aux-per-episode", type=int, default=1, metavar="N",
                    help="probes sampled per episode (from decisions after the "
                         "first, where a cue can exist at all)")
    ap.add_argument("--aux-probe-every", type=int, default=5, metavar="K",
                    help="run the two-way forced-choice probe accuracy every K "
                         "steps (0 = never). Two forward passes, no backward. "
                         "Worth having on the CONTROL arm too: a probe at "
                         "chance says the cue is unreadable, which is a "
                         "statement about the cells and not about the trainer.")
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
    ap.add_argument("--hole-noisy", action="store_true",
                    help="NOISY HOLE arm: pin every env's `hole` consequence to "
                         "its TREMBLING population member (core.NOISY_HOLE) "
                         "instead of rotating all three. The affordance is "
                         "unchanged and still never punished -- it just fails "
                         "to land ~10%% of the time, for reasons uncorrelated "
                         "with anything the agent did. Asks whether the hole "
                         "arm's cross-play capability regression survives an "
                         "affordance that is only usually-good, where "
                         "unconditional exploitation stops being a sufficient "
                         "statistic for the environment. No effect on nohole or "
                         "the two adaptive arms, which have no trembling member "
                         "and are not what this varies.")
    ap.add_argument("--endgame-penalty", type=float, default=0.0, metavar="MARGIN",
                    help="HIDDEN reward shaping, opt-in (0 = off). Dock the "
                         "TRAINING REWARD -- never the payoff or the capture "
                         "diagnostic -- by MARGIN * (per-instance premium) for "
                         "every betrayal that lands in the final --endgame-frac "
                         "of an episode's scored decisions. The agent is NOT "
                         "told this is happening (no observation text, no "
                         "opponent line): the point is to see whether the policy "
                         "learns to stop waiting-till-the-end-to-betray purely "
                         "from the reward. Orthogonal to --consequence (it "
                         "layers on whatever opponent the arm draws). The "
                         "pre-launch check_suite gate is unaffected because it "
                         "reads the raw payoff.")
    ap.add_argument("--endgame-frac", type=float, default=0.25, metavar="FRAC",
                    help="the trailing fraction of an episode's scored decisions "
                         "that counts as 'the end' for --endgame-penalty; "
                         "window = ceil(FRAC * n_scored), at least 1.")
    ap.add_argument("--horizon", default="finite", choices=list(core.HORIZON),
                    help="'finite' (default) keeps each env's authored round-count "
                         "disclosure. 'infinite' withholds it: the episode still "
                         "runs the SAME number of rounds and every payoff is "
                         "unchanged, but the agent is never told the total, so "
                         "backward induction has nothing to attach to. The "
                         "OPPOSITE lever to --endgame-penalty -- that one prices "
                         "the endgame behaviour, this one removes the cue.")
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
    ap.add_argument("--think", action="store_true",
                    help="sample with the reasoning block on. The suite "
                         "otherwise holds CoT fixed OFF across conditions "
                         "(tinker_actor) because varying it BY condition is a "
                         "confound -- that still holds; this flag exists so "
                         "thinking can be the manipulation in a matched pair "
                         "where everything else, disposition included, is "
                         "identical. Needs a much larger --max-tokens: the "
                         "screen that motivated it ran 1024.")
    ap.add_argument("--reasoning-effort", default="",
                    help="'low' | 'medium' | 'xhigh'. Qwen3.8 templates DEFAULT "
                         "TO xhigh whenever thinking is on, which blows any "
                         "sane token budget; the base-model screen used 'low'. "
                         "Empty leaves the template default.")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--out", default=str(HERE / "runs"))
    ap.add_argument("--ckpt-every", type=int, default=None,
                    help="checkpoint every N steps (default: 0/25/50/75/100%% of --steps)")
    ap.add_argument("--resume-from", default=None,
                    help="tinker:// STATE path from checkpoints_state.json")
    ap.add_argument("--start-step", type=int, default=0, metavar="N",
                    help="continue the step axis at N instead of 0. Use with "
                         "--resume-from and set it to the step the state was "
                         "saved at, so metrics.jsonl stays one series and the "
                         "earlier checkpoints keep their keys.")
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
    elif args.regime_draw != "group":
        raise SystemExit("--regime-draw only means anything under --regime-mix: "
                         "without it the disposition is not drawn at all.")
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
    # The two opponent-conditioning fixes are part of the run's identity for the
    # same reason `--think` is: three arms that differ only in which fix is on
    # would otherwise collide on disk, and the collision is silent -- same
    # label, appended metrics, overwritten config.
    if args.aux_weight > 0:
        arm_tag += "-aux"
    if regime_random and args.regime_draw == "rollout":
        arm_tag += "-rr"
    if args.advantage == "critic":
        arm_tag += "-critic"
    # Thinking is part of the run's identity, not a detail: a think-on and a
    # think-off run of the same arm would otherwise share a directory and
    # silently overwrite each other's config.
    if args.think:
        arm_tag += "-think"
    # Same reason as --think and --horizon: the counterpart the arm trained
    # against is part of the run's identity, and a noisy-hole run must not share
    # a directory with the reliable-hole run it is meant to be compared to.
    if args.hole_noisy:
        if "hole" not in (set(cons_of.values()) if cons_of else set(core.CONSEQUENCE)):
            raise SystemExit("--hole-noisy on a run with no hole cells: nothing "
                             "to pin. It applies to the `hole` consequence only.")
        arm_tag += "-noisy"
    label = f"mixed{sfx}_{arm_tag}_d{args.dose:g}_s{args.seed}"
    if args.endgame_penalty:
        label += f"_eg{args.endgame_penalty:g}"
    # Same reason as --think: the horizon is a training condition, and an
    # `infinite` run must not share a directory with its `finite` control.
    if args.horizon != "finite":
        label += f"_{args.horizon[:3]}"
    def opp_for(env: str, cons: str) -> str:
        """The population member this cell is pinned to, or "" to rotate.

        Resolved once here rather than at rollout time so that the manifest, the
        launch banner and the gradient all name the SAME counterpart -- the
        failure mode being a run whose config says one thing and whose episodes
        did another.
        """
        if args.hole_noisy and cons == "hole":
            return core.noisy_hole_member(env)
        return ""

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
                                       else list(s.populations(cons_of[e])),
                         "opponent_pin": ({c: opp_for(e, c) for c in core.CONSEQUENCE}
                                          if cons_of is None
                                          else opp_for(e, cons_of[e]))}
                     for e, s in specs.items()},
         "mixed_regime": mixed_regime, "regime_random": regime_random,
         "regime_mix": args.regime_mix,
         "consequence_of": cons_of}, indent=1) + "\n")
    if args.advantage == "critic" and not regime_random:
        print("[mixed] warning: --advantage critic on a SINGLE-regime run. The "
              "critic still de-noises, but there is no cue to condition on, so "
              "this is not the fix it was built to be.", flush=True)
    if regime_random and args.advantage == "critic" and args.regime_draw == "group":
        print("[mixed] warning: --advantage critic with --regime-draw group. "
              "The group mean already absorbs the regime, so the critic has "
              "nothing left to add; see cue_critic.py.", flush=True)
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
            pin = opp_for(e, c)
            probe = check_suite.cell_summary(e, c, edose, seeds=16,
                                             workers=args.workers,
                                             opponent=pin or None)
            flag = "ok" if probe["ok"] else "; ".join(probe["problems"])
            dtag = f" dose={edose:g}" if edose != args.dose else ""
            ptag = f" vs {pin}" if pin else ""
            print(f"[mixed] {e:16s} [{c:6s}] premium={probe['premium']:+.2f} "
                  f"honest={probe['honest']:.2f} exploit={probe['exploit']:.2f} "
                  f"({flag}){dtag}{ptag}", flush=True)
            if not probe["ok"]:
                bad.append(f"{e}[{c}]")
    if bad:
        raise SystemExit(
            f"these cells fail check_suite.py and would poison the mix: "
            f"{', '.join(bad)}. Drop them with --envs or fix the dose.")

    tinker = None
    tc = sampler = renderer = probe_renderer = None
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
        renderer = tinker_actor.Renderer(
            tc.get_tokenizer(), enable_thinking=args.think,
            reasoning_effort=args.reasoning_effort or None)
        # The probe renders with thinking OFF even in a think-on run. Two
        # reasons: the Qwen template pre-opens `<think>` under
        # add_generation_prompt, so the supervised label would land inside a
        # reasoning block and teach the model to answer there; and holding the
        # probe's format fixed is what makes `aux/probe_acc` comparable between
        # the think-on and think-off arms, which is the pair this wave exists
        # to compare.
        probe_renderer = tinker_actor.Renderer(tc.get_tokenizer(),
                                               enable_thinking=False)

    wb = init_wandb(args, label, envs) if (args.use_wb and not args.dry_run) else None
    print(f"[{label}] model={args.model} steps={args.steps} envs={len(envs)} "
          f"episodes/step={groups * args.group_size}", flush=True)

    if args.ckpt_every:
        ckpt_steps = set(range(0, args.steps + 1, args.ckpt_every)) | {args.steps}
    else:
        ckpt_steps = {int(round(f * args.steps)) for f in (0.0, 0.25, 0.5, 0.75, 1.0)}
    # ON RESUME, START FROM WHAT IS ALREADY ON DISK. These two dicts are
    # rewritten WHOLE every time a checkpoint lands, so starting them empty in
    # a resumed run silently deletes every earlier checkpoint's URI from
    # `checkpoints.json` -- the file the trace sweeps, the capability watcher
    # and `eval_generalization` all resolve steps through. The weights survive
    # on Tinker, but nothing left on disk can name them.
    def _load(name):
        try:
            return json.loads((outdir / name).read_text())
        except Exception:
            return {}

    checkpoints = _load("checkpoints.json") if args.resume_from else {}
    states = _load("checkpoints_state.json") if args.resume_from else {}
    if checkpoints:
        print(f"[{label}] carrying forward {len(checkpoints)} existing "
              f"checkpoints: {sorted(checkpoints, key=int)}", flush=True)

    def save_ckpt(step: int) -> None:
        if args.dry_run:
            return
        # The critic is part of the training state: a run resumed from a Tinker
        # state with a fresh critic would spend its first steps baselining
        # against zero, which is a scale error large enough to show up in the
        # curve and be misread as the resume itself.
        if critic is not None:
            critic.save(outdir / f"critic_step{step:04d}.json")
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

    # A minimal args view for the shared rollout: fixed arm, no self-play, and
    # normally no pinned opponent (the arm rotates its population by seed --
    # `--hole-noisy` is the one thing that pins it). Dose is per-env (see
    # PER_ENV_DOSE), so build one view per env and index it by the job.
    class _RArgs:
        selfplay = False

        def __init__(self, dose: float, consequence: str, opponent: str = ""):
            self.consequence = consequence
            self.opponent = opponent
            self.dose = dose
            self.temperature = args.temperature
            self.max_tokens = args.max_tokens
            self.top_p = args.top_p
            self.close_bracket = args.close_bracket
            self.endgame_penalty = args.endgame_penalty
            self.endgame_frac = args.endgame_frac
            self.horizon = args.horizon
    critic = None
    if args.advantage == "critic":
        critic = (cue_critic.CueCritic.load(args.critic_resume)
                  if args.critic_resume
                  else cue_critic.CueCritic(dim=args.critic_dim,
                                            lr=args.critic_lr, seed=args.seed))
        print(f"[{label}] cue critic: dim={critic.dim} lr={critic.lr} "
              f"seen={critic.n_seen}", flush=True)
    # The consequences this run can actually draw -- under --regime-mix the
    # hole/nohole pair, otherwise whatever `cons_of` names, which for the two
    # adaptive arms is NOT in core.CONSEQUENCE. Iterating the pair here would
    # KeyError the moment a job came back tagged `adaptive`.
    live_cons = (list(core.CONSEQUENCE) if cons_of is None
                 else sorted(set(cons_of.values())))
    rargs_for = {(e, c): _RArgs(dose_for(e, args), c, opp_for(e, c))
                 for e in envs for c in live_cons}

    steps = min(args.steps, 2) if args.dry_run else args.steps
    # A resumed run continues the SAME step axis. Restarting the counter at 0
    # would append a second series of steps 0..N to `metrics.jsonl` -- every
    # curve read off that file would fold the two passes on top of each other --
    # and would re-key the checkpoints, overwriting step 22 of the first pass
    # with step 22 of the second.
    start = args.start_step
    if start and not args.resume_from:
        raise SystemExit("--start-step without --resume-from would skip "
                         "training steps rather than continue them")
    if start:
        print(f"[{label}] continuing the step axis at {start} -> {steps}",
              flush=True)
    t_start = time.time()
    for step in range(start, steps + 1):
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
            #
            # Under --regime-draw rollout the group is SPLIT between the two
            # counterparts instead, by a balanced deterministic assignment
            # rather than a coin per rollout: with group_size 6 and p 0.5 a
            # per-rollout coin leaves ~3% of groups single-regime, and a group
            # with no contrast in it is exactly the case the cue-conditioned
            # baseline has nothing to do. See cue_critic.py for why the
            # same-counterpart invariant is being given up on purpose.
            cons = (("hole" if core.Draws(env_seed, "regime").hit(
                        "regime", args.regime_mix) else "nohole")
                    if regime_random else cons_of[env])
            split = None
            if regime_random and args.regime_draw == "rollout":
                n_hole = int(round(args.group_size * args.regime_mix))
                order = list(range(args.group_size))
                _random.Random(f"{env_seed}:regime").shuffle(order)
                split = set(order[:n_hole])
            for k in range(args.group_size):
                ck = ("hole" if k in split else "nohole") if split is not None else cons
                jobs.append((g, env, env_seed, env_seed * 31 + k, ck))

        t0 = time.time()
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            recs = list(ex.map(
                lambda j: train_hole.rollout(sampler, renderer,
                                             rargs_for[(j[1], j[4])],
                                             specs[j[1]], j[2], j[3],
                                             stub=args.dry_run), jobs))
        roll_s = time.time() - t0
        envs_of = [j[1] for j in jobs]

        # Sampled length, per turn. Logged ALWAYS, not just under
        # --length-normalise: the format collapse that killed the first wave was
        # a length runaway, and `invalid_rate` only sees it once the ramble has
        # already swallowed the action token. p90 moving while the mean does not
        # is the early warning `invalid_rate` cannot give.
        tok_lens = [len(tr.get("tokens") or [])
                    for r in recs for tr in r.get("traces", [])]
        mean_len = (sum(tok_lens) / len(tok_lens)) if tok_lens else 0.0
        token_norm = mean_len if (args.length_normalise and mean_len) else None

        data, adv_all = [], []
        critic_batch = []  # (idx, val, target) -- fit AFTER the step, never before
        for g in range(groups):
            grp = [r for j, r in zip(jobs, recs) if j[0] == g]
            R = [r["score"] for r in grp]
            if critic is None:
                mu = sum(R) / len(R)
                sd = st.stdev(R) if len(R) > 1 and st.stdev(R) > 1e-6 else 1.0
                for r, rr in zip(grp, R):
                    a = (rr - mu) / sd
                    adv_all.append(a)
                    if tinker is not None:
                        data.extend(train_hole.build_data(r, a, tinker, token_norm))
                continue
            # Cue-conditioned baseline. One residual per DECISION -- the
            # episode's return minus what the critic expected from the prefix
            # the policy could see at that decision -- then standardised over
            # the whole group. The group statistics are here for SCALE (the
            # roster's payoff scales differ by an order of magnitude); the
            # baselining is the critic's job, and unlike the group mean it does
            # not absorb the regime. See cue_critic.py.
            per_ep = []
            for r, rr in zip(grp, R):
                feats = []
                turns = r.get("turns") or []
                for ti in cue_critic.turn_index(r):
                    msgs = (turns[ti].get("messages") or []) if ti < len(turns) else []
                    feats.append(critic.features(msgs, r.get("env") or "?", ti))
                resid = [rr - critic.predict(ix, vl) for ix, vl in feats]
                per_ep.append((r, resid))
                critic_batch.extend((ix, vl, rr) for ix, vl in feats)
            flat = [x for _, res in per_ep for x in res]
            if not flat:
                continue
            mu = sum(flat) / len(flat)
            sd = st.stdev(flat) if len(flat) > 1 and st.stdev(flat) > 1e-6 else 1.0
            for r, resid in per_ep:
                adv = [(x - mu) / sd for x in resid]
                adv_all.extend(adv)
                if tinker is not None:
                    data.extend(train_hole.build_data(r, adv, tinker, token_norm))

        # Probe prompts. Built whenever `--aux-probe-every` asks for the
        # accuracy readout, INDEPENDENTLY of whether the aux gradient is on:
        # `aux/probe_acc` is the identifiability diagnostic ("is the cue
        # readable at all?") and it is most load-bearing on the arm with NO aux
        # loss, where a chance-level probe says no trainer change was ever going
        # to produce conditioning. Gating construction on `--aux-weight` -- the
        # first version of this -- removed the diagnostic from exactly the arm
        # that needed it.
        #
        # Only `aux_data` is ever handed to a backward pass, and only when the
        # weight is positive, so a control arm's gradient is untouched: it pays
        # two forward passes every K steps and nothing else.
        aux_data, aux_flip = [], []
        want_probe = (args.aux_probe_every
                      and step % args.aux_probe_every == 0)
        if (tinker is not None and probe_renderer is not None
                and (args.aux_weight > 0 or want_probe)):
            aux_data, aux_flip, _ = aux_probe.build(
                recs, probe_renderer, tinker,
                # A zero weight would make every supervised position weightless
                # and the NLL readout a division by zero; the probe datums are
                # scored, not trained, when the aux loss is off.
                weight=args.aux_weight or 1.0,
                per_episode=args.aux_per_episode, seed=args.seed * 7919 + step)

        if not args.dry_run and not data:
            print(f"[{label}] step {step}: no data, skipping", flush=True)
            continue

        aux_m = {}
        if not args.dry_run:
            fb = tc.forward_backward(data, loss_fn="importance_sampling")
            if hasattr(fb, "result"):
                fb.result()
            if aux_data and args.aux_weight > 0:
                afb = tc.forward_backward(aux_data, loss_fn="cross_entropy")
                ares = afb.result() if hasattr(afb, "result") else afb
                losses = aux_probe.nll(aux_data, ares.loss_fn_outputs)
                good = [x for x in losses if x == x]
                aux_m = {"aux/nll": (sum(good) / len(good)) if good else None,
                         "aux/n": len(aux_data)}
            tc.optim_step(tinker.AdamParams(learning_rate=args.lr))
            # Accuracy AFTER the update, on the same prompts: it is a readout of
            # the weights the next step will roll out with, which is the thing a
            # reader wants to line up against that step's discrimination.
            if want_probe and aux_flip:
                try:
                    aux_m.update(aux_probe.probe_accuracy(tc, aux_data, aux_flip))
                except Exception as e:  # noqa: BLE001 - a diagnostic, never the run
                    print(f"[{label}] probe accuracy failed: "
                          f"{type(e).__name__}: {e}", flush=True)

        # PREQUENTIAL. The critic scored this step with the weights it had
        # BEFORE seeing it, and only now learns from it. With 4096 features and
        # a few hundred decisions a step, a critic fit on the batch it is
        # scoring would partly memorise it and eat real advantage along with
        # the noise.
        if critic is not None:
            mse = critic.update(critic_batch)
            aux_m["critic/mse"] = mse
            aux_m["critic/n_seen"] = critic.n_seen

        if args.dump_traces and step in ckpt_steps:
            tdir = outdir / "traces"
            tdir.mkdir(exist_ok=True)
            with (tdir / f"step_{step:04d}.jsonl").open("w") as f:
                for r in recs[:args.dump_traces]:
                    f.write(json.dumps({k: v for k, v in r.items()
                                        if k != "traces"}) + "\n")

        # The per-decision rows `cue/cci` is computed from, kept so any
        # stratification can be redone offline over any window of steps.
        #
        # Why this is worth a file. A stratum needs BOTH regimes present to
        # carry a contrast, and under a per-GROUP regime draw with two groups
        # per env each drawing independently, roughly half the envs are
        # single-regime in any step and contribute nothing -- measured at ~180
        # usable decisions a step against ~430 for the per-rollout split. The
        # per-step estimate is consistent (Mantel-Haenszel is built for sparse
        # strata) but thin, and the fix is to pool decisions across steps rather
        # than average per-step estimates. That cannot be done from
        # metrics.jsonl, which stores only the summary -- hence the rows.
        # Compact: ~420 rows a step, one dict of parallel arrays.
        if regime_random and not args.dry_run:
            rows = cue_metrics.decisions(recs)
            with (outdir / "decisions.jsonl").open("a") as f:
                f.write(json.dumps({
                    "step": step,
                    "env": [r["env"] for r in rows],
                    "reg": [1 if r["regime"] == "hole" else 0 for r in rows],
                    "t": [r["t"] for r in rows],
                    "k": [r["k"] for r in rows],
                    "y": [r["y"] for r in rows],
                    "ep": [r["ep"] for r in rows]}) + "\n")

        m = {"step": step, **step_metrics_mixed(recs, envs_of, cons_of), **aux_m,
             "adv_std": round(st.stdev(adv_all), 4) if len(adv_all) > 1 else None,
             "train/sampled_tokens_mean": round(mean_len, 1),
             "train/sampled_tokens_p90": (
                 sorted(tok_lens)[int(0.9 * (len(tok_lens) - 1))] if tok_lens else None),
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
        # CCI is the number to watch, not DISC: same contrast, but taken at
        # matched decision points so it cannot move just because the two regimes
        # scored different sets of decisions. cue_metrics.py has the argument.
        cci, cse = m.get("cue/cci"), m.get("cue/cci_se")
        if cci is not None:
            dtag += f"  CCI={cci:+.3f}" + ("" if cse is None else f"+-{cse:.3f}")
        acc = m.get("aux/probe_acc")
        if acc is not None:
            dtag += f"  probe={acc:.2f}"
        anll = m.get("aux/nll")
        if anll is not None:
            dtag += f"  auxnll={anll:.3f}"
        eg = m.get("train/endgame_rate")
        egtag = "" if eg is None else f"  eg={round(eg, 3)}"
        # Think-on only: how much of `invalid` is a thought that ran out of
        # budget rather than a format collapse. Charged the same either way, but
        # they are different problems and the log has to distinguish them.
        tr = m.get("train/think_truncated_rate")
        trtag = "" if tr is None else f"  trunc={round(tr, 3)}"
        inv = m.get("train/invalid_rate")
        print(f"[{label}] step {step:3d}  R={m['train/reward']:+.3f}  "
              f"exploit={xr if xr is None else round(xr, 3)}  "
              f"capture={cap if cap is None else round(cap, 3)}  "
              f"invalid={inv if inv is None else round(inv, 4)}"
              f"{trtag}{dtag}{egtag}  "
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
