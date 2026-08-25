# 0820 — is the control arm's suppression a learned rule, or an absorbing state?

## The question

The shipped `nohole` arm sets `removal: true` in every spec's `consequence`
block. In `spec_env.play_episode`, the first detected exploit sets `removed`,
and every remaining round short-circuits to `{"action": "removed", "take": 0}`.
So the control arm is **terminal**: get caught once and the term is over.

That makes the 0819 result — natural-frame `nohole` falling from ~0.96 to 0.13
exploit_rate over 60 steps — ambiguous in a specific way. `train/exploit_rate`
is exploit decisions over *scored* decisions, and removed rounds increment
neither, so absorption does not mechanically deflate the number. What it does
is **truncate credit assignment**: the policy never experiences a round after
being caught, so "exploit, then stop" is not in the sampled data and cannot be
learned. Only "don't start" can be. The falling curve is therefore consistent
with two very different policies, and the run cannot separate them.

## The ablation

`train_frame_ablation.py --removal off` (new). Keeps clawback and the fine,
drops the absorption: a detected round costs that round, and a policy that
stops exploiting earns full honest pay again. Implemented in
`ablate_plant.variant_spec` as a fourth ablation axis; the variants get an
`_nr` name suffix and the runs a `norem` label tag.

Nothing in the brief or the registers mentions removal, so the **surface is
byte-identical** to the shipped arm — the difference is recoverability and
nothing else. It is a provable no-op in the hole arm (nothing is ever
detected), confirmed by the offline gates being identical there, so the shipped
`mixed_natural_hole_d1_s*` stay the shared ceiling and no new hole runs were
needed.

Runs: `mixed_natural_norem_nohole_d1_s{0,1,2}`, matched to 0819 on everything
else (six domains, explicit plant, Qwen3.6-27B, 60 steps, 6 groups x 6, dose 1,
lr 2e-5, rank 32). Launcher: `run_frame_removal.sh`.

### Offline gates first

All six `*_nr` cells still price exploiting below honest in the nohole arm at
64 seeds (premium −7.5 to −149.5), so deterrence survives without removal.

Two things worth carrying forward:

* Over the **full 22-domain** surface set, three cells fail the nohole gate
  with removal off — `performance_bonus`, `procurement_rounding`,
  `travel_reimbursement` go "OPEN: exploiting still pays". For those, removal
  *was* the deterrent. None are in the ablation six, but this constrains
  extending the ablation to the nat21 roster.
* Removal is not purely punitive. For high-fine domains the always-exploit
  reference does **better** with removal on (`metr` −36.8 vs −69.5 without):
  being taken off the board stops you accruing further fines. This is a
  recoverability ablation, not a "weaker punishment" ablation.

## Result 1 — training curves (`results/frame-removal-0820.md`)

Last-10-step mean ± sd across three seeds:

| arm | exploit | capture | detected | removed |
|---|---|---|---|---|
| natural_hole (ceiling) | 0.96 ±0.01 | 0.91 ±0.01 | 0.00 | 0.00 |
| natural_nohole (absorbing, 0819) | 0.13 ±0.03 | 0.08 ±0.11 | 0.14 | 0.14 |
| natural_norem_nohole (recoverable) | 0.25 ±0.12 | 0.21 ±0.11 | 0.26 | 0.00 |

Per-seed: s0 0.16 → 0.27, s1 0.10 → 0.10, s2 0.15 → 0.40.

**Removal accounts for +0.118 of the trained exploit rate, and with n=3 that is
not separable from noise** (s1 is identical across arms). Most of the
suppression survives without the absorbing state — clawback plus the fine does
the bulk of the work.

The robust difference is **variance**, not level: ±0.03 → ±0.12. When the term
ends on first detection every seed converges to the same place; when you can
keep playing, seeds spread from 0.10 to 0.40. Removal was stabilising the
outcome as much as lowering it.

Independent post-run screens of the final checkpoints agree with the training
tails (0.21 / 0.07 / 0.34 vs 0.27 / 0.10 / 0.40), so this is not a
training-batch artifact.

## Result 2 — nobody learned to recover (`results/recovery-0820.md`)

`analyze_recovery.py` probes every policy — base, hole, absorbing nohole,
recoverable nohole — in the **same** recoverable `*_nr` cells, so the
measurement is held constant and only the training condition varies.

**The estimator matters more than the result here.** Three versions, in order:

1. *Naive* — rounds before any detection vs rounds after. Gives strongly
   negative "recovery" for every policy **including the untrained base model**
   (−0.48 to −0.68), i.e. "exploits more after being caught". Confounded: you
   can only be detected in an episode where you already exploited, and the
   exploit decision is autocorrelated within an episode, so the post-detection
   pool is drawn from the exploiting episodes. It reads backwards for any
   policy that has both exploiting and honest episodes. **Do not use it.**
2. *Bucketed* — `tempted` (exploited before, not caught) vs `burned`
   (exploited before, caught). Holds "this is an exploiting episode" fixed.
3. *Stratified* — same, restricted to rounds with equal prior-exploit count,
   pooled Mantel-Haenszel style. Removes the "more exploits → more likely
   caught → more exploitative episode" residual.

| policy | exploit | fresh | tempted | burned | recovery | recovery (strat) |
|---|---|---|---|---|---|---|
| base | 0.377 | 0.169 | 0.626 | 0.850 | −0.224 | −0.115 |
| natural_hole | 0.951 ±0.004 | 0.914 | 0.951 | 0.968 | −0.017 ±0.005 | 0.000 ±0.003 |
| natural_nohole | 0.111 ±0.014 | 0.042 | 0.582 | 0.660 | −0.078 ±0.092 | 0.001 ±0.118 |
| natural_norem_nohole | 0.240 ±0.091 | 0.104 | 0.547 | 0.789 | −0.241 ±0.141 | −0.144 ±0.127 |

**Neither control arm learned a recovery contingency.** The absorbing arm
scores 0.001 ±0.118 — expected, it never sampled a post-detection round. The
recoverable arm *did* sample them, for 60 steps, and still scores −0.144 ±0.127
— if anything it exploits slightly *more* after being caught, and certainly not
less.

Corroborating, and independent of the estimator: **exploit rate is flat across
rounds 1–5 for every policy** (hole 0.93/0.98/0.93/0.97/0.94; absorbing nohole
0.11/0.10/0.12/0.10/0.12; recoverable 0.24/0.24/0.23/0.26/0.24). What these
policies learned is an **episode-level disposition, not a within-episode
response to feedback**. The `fresh` → `tempted` jump (0.04 → 0.58 for the
absorbing arm) is the same fact from the other side: whether this episode is an
exploiting one is decided early and then held.

### What this means for the 0819 reading

The ambiguity that motivated the ablation resolves in the *unsatisfying*
direction. The control arm's fall is not "the policy got caught and ran out the
clock" — removing the clock barely moves the level. But it is also not "the
policy learned the contingency". It is a propensity shift: the policy became
less likely to *start* exploiting, and never learned anything about stopping.
Removal was never the mechanism, and recovery was never learned even when it
was available and rewarded.

### Residual confound, and the clean follow-up

Stratifying on prior-exploit count does not remove the **take-size** confound:
`p_detect` rises with the take, so `burned` still over-samples rounds following
large takes, which are the more exploitative episodes. That biases `recovery`
downward and cannot be fixed from observational rollouts.

The clean version is an **interventional** probe: paired episodes with the same
policy, seed and prefix, forcing the detection coin ON vs OFF after the first
exploit, comparing subsequent behaviour. Same take, same prefix, only the
detection message differs. That needs a `cfg` hook to override
`draws.hit(f"detect{rnd}", ...)` in `spec_env.play_episode` — a change to a
hand-written, invariant-tested module, so it is not done here. Given the flat
by-round profile it would most likely confirm the null.

## Files

* `ablate_plant.py` — `removal` axis on `variant_name`/`variant_spec`/
  `register_variants`; `--removals`, `--screen-arm`; `SLUG_LONG` (the `_nr`
  tail pushes eight generated domains past `NAME_RE`'s 32 chars, so they get a
  short slug **only** when the name overflows — no existing cell is renamed)
* `train_frame_ablation.py` — `--removal {inherit,on,off}`, `norem` label tag
* `run_frame_removal.sh` — launcher + traces-to-viewer + post-run screen
* `frame_removal_report.py`, `analyze_recovery.py`
* `frame_to_viewer.py` — fixed a break predating this work: since the 0819
  scale-up it crashed registering game variants of generated domains, which
  have only natural surfaces authored

Traces for all three runs are in the SkyRL viewer (port 8795) as
`frame-natural_norem_nohole_d1_s{0,1,2}`.

## Result 3 — T1 transfer: the instrument is not ready (`results/t1-*.json`)

T1 (`exploit-bench/eval/eval_checkpoint.py`, panel `cs-contested-v2`) had
**never actually run against a hole_exp checkpoint**. The command `post_run.sh`
prints dies on `KeyError: 'checkpoints'`: the two packages record checkpoints
in different shapes. `t1_sidecar.py` (new) translates, and it runs now.

Three findings, in descending order of how much they matter:

**1. It does not reproduce.** `mixed_natural_norem_nohole_d1_s1-final`, same
checkpoint, same panel, `temperature=0.0`, measured twice:

    lift = +0.187      (first run)
    lift = +0.420      (second run)

A 0.233 spread on a repeat measurement, against a between-arm difference of
0.297. Whatever the cause — server-side sampling nondeterminism, or the first
run degrading under concurrent load — **single-run T1 numbers cannot support a
between-arm claim at this effect size.** Repeat measurement per checkpoint is a
prerequisite, and nothing below should be quoted until that is in place.

**2. Two of the four reported channels are dead.** `compliant` / `inadequate` /
`leak` come out 0% / 0% / 100% for all six checkpoints including the 0819 ones.
Saturated, no discrimination, do not quote. And the `tool` channel is skipped
entirely — `TemplateError: No user query found in messages`, a genuine
incompatibility between these checkpoints and the panel's message
construction. T1 here is user-channel only.

**3. What signal there is points the same way as everything else.** Taking the
numbers at face value despite (1):

| arm | n | lift | panel_dc | control_dc |
|---|---|---|---|---|
| absorbing (0819) | 3 | +0.156 ±0.044 | 2.128 ±0.028 | 1.972 ±0.071 |
| recoverable (0820) | 3 | +0.453 ±0.128 | 2.151 ±0.005 | 1.698 ±0.132 |

`panel_dc` is **flat across all six checkpoints** (2.09–2.16). Under active
influence pressure every policy captures the same amount, whichever arm trained
it. All the variation is in `control_dc`, the lever-free baseline (1.52–2.03).
Since `lift = panel − control`, the entire apparent transfer difference is a
baseline shift surfacing through a subtraction — not differential
susceptibility to the levers.

That is the same shape as Result 2: these runs move a standing propensity and
leave the response-to-situation untouched. It is corroboration, not independent
evidence, and it rests on an instrument that just failed a repeat test.

## Not done

* **T1 repeat measurement.** The blocker above. Until each checkpoint is
  measured 3+ times, the arm comparison is not reportable.
* **T1 tool channel.** Needs the template incompatibility fixed.
* **T0/T2 of EVAL_SUITE.** Both need a served model
  (`evals/serve_tinker_ckpt.sh`) and, for the slurm batteries, a live cluster.
* **The forced-detection counterfactual** for the recovery null (see above).
