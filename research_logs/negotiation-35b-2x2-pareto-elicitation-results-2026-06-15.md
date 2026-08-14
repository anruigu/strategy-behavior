# 35B Pareto × Elicitation 2×2 — results & hypothesis verdict (2026-06-15)

Analysis of the 5 runs specified in
`SkyRL-Fleet/skyrl-gym/skyrl_gym/envs/negotiation/initial_experiments.md`
(Qwen3.5-35B-A3B, dnd, `single`, **thinking ON**, fixed GPT-4o-mini opponent).
Source: wandb `thefleet/fleet-negotiation-grpo` training-rollout + eval metrics.
Pathology/checkpoint-hygiene companion: `negotiation-35b-grad-explosion-reward-regression-2026-06-12.md`.

| cell | reward | elicit | wandb id |
|---|---|---|---|
| C1 | outcome          | none      | `8d664obf` |
| C2 | outcome_jointeff | none      | `v33xm6d2` (orig, unstable — superseded) |
| C2b| outcome_jointeff | none      | `aurhs4u9` (stabilized; the C2 of record) |
| C3 | outcome          | two_sided | `twmqlskf` |
| C4 | outcome_jointeff | two_sided | `jdyjaeas` |
| C5 | outcome_jointeff | one_sided | `krr5ph7e` |

All runs `crashed`/killed early (intentional — nodes recycled; see hygiene log). Conclusions are
drawn at the **best-eval checkpoint per cell, never the last** — late checkpoints are post-collapse
(C1 s130 = 42% no-deal; the grad-explosion pathology recurs on every arm if pushed).

## TL;DR — the experiment falsifies its own primary hypothesis

The spec predicted **elicitation is the larger main effect**, with a positive interaction so that
**C4 (info+incentive) >> C2, C3**. The data show the opposite:

1. **Reward is the dominant lever; elicitation adds ~nothing on top of it.** On continuous
   joint-efficiency the two jointeff cells are tied at the top (C2b 0.785, C4 0.781) and the
   elicitation flag moves jeff by <0.01 within an arm (C4 ≈ C2b). **C4 is NOT >> C2b.**
2. **C2 alone (jointeff reward, no elicitation) already reaches the integrative best** -> this is the
   spec's explicit **falsification** condition. The binding constraint was **motivational (reward),
   not informational (elicitation).**
3. **The integrative "gap" was tiny to begin with.** Base joint-efficiency is already ~0.748; the best
   cell reaches ~0.785 (**+0.037**). Nobody meaningfully grew the pie. The large, robust, reproducible
   effect is **distributive**: the pure-outcome/none arm collapses into extreme extraction
   (you/them = **0.98 / 0.03**), and *every other cell* — both jointeff cells **and** the
   outcome+elicitation cell — stays roughly equitable. The jointeff reward's demonstrated payoff is
   **safety (not exploiting the pushover)**, not integrativeness.

## The 2×2 at best-eval checkpoint

`eval` = `eval/negotiation_dnd/avg_score` (greedy val, = own-value/outcome reward).
`jeff` = `environment/joint_efficiency` (continuous, **primary integrative metric**).
`pareto` = binary Pareto-optimal rate (gameable vs pushover — see note). `gap` = |you−them|.

| cell | step | eval | **jeff** | pareto | you | them | **gap** | no_deal | think_rate | leak/ep |
|---|---|---|---|---|---|---|---|---|---|---|
| base (untrained)* | 0 | — | 0.748 | 0.27 | 0.531 | 0.537 | 0.01 | ~0.14 | (n/a) | — |
| **C1** out/none   | 110 | 0.943 | 0.673 | 0.680† | **0.981** | **0.034** | **0.95** | 0.016 | **0.009** | 0.00 |
| **C2b** jeff/none | 90  | 0.937 | 0.725 | 0.414 | 0.598 | 0.514 | 0.08 | 0.047 | 0.482 | 0.41 |
| **C3** out/two    | 50  | 0.284 | 0.746 | 0.469 | 0.560 | **0.638** | 0.08 | 0.047 | 0.444 | 0.29 |
| **C4** jeff/two   | 120 | 0.611 | 0.721 | 0.430 | 0.569 | 0.519 | 0.05 | 0.070 | 0.443 | 0.70 |
| **C5** jeff/one   | 60  | 0.708 | 0.732 | 0.398 | 0.533 | 0.599 | 0.07 | 0.047 | 0.372 | 0.32 |

\*base from the 06-12 eval-set reconstruction (192 traces). †C1's pareto 0.68 is the **binary loophole**:
taking the whole pool from a rubber-stamp opponent *is* Pareto-optimal — exactly why the spec switched
the reward to continuous jeff. C1's honest jeff (0.673) is the **lowest** of all cells. C1 s110 is also a
degenerate checkpoint (grad_norm 2022, entropy 0.001, think_rate 0.009 -> a non-reasoning over-claimer).
jeff peaks (stable) at: C2b 0.785@s70, C4 0.781@s130, C5 0.738@s70, C3 0.746@s50.

## Main effects (continuous joint-efficiency, the metric the spec chose)

- **REWARD main effect — clear and the only real one.** jointeff arms (C2b/C4/C5 ≈ 0.72–0.785) >
  outcome arms (C1 0.67, C3 0.746). Switching the reward from `outcome` -> `outcome_jointeff` is what
  raises jeff and, more importantly, *prevents the extraction collapse*.
- **ELICITATION main effect — weak / inconsistent.** On the jointeff arm it does nothing
  (C4 0.72–0.78 ≈ C2b 0.72–0.78). On the outcome arm it *raises* jeff (C3 0.746 > C1 0.673) but only by
  suppressing extraction, not by trading better. **No positive interaction** (C4 not > C2b,C3).

## Hypothesis verdicts

- **H1 "incentive only is weak"** -> **CONTRADICTED.** C2b (jointeff/none) is the joint-best on jeff and
  fully equitable on its own. Incentive alone is the *strongest* single lever, not the weak one.
- **H2 "info only -> better extractor, equity gap up, Pareto flat"** -> **CONTRADICTED on the headline.**
  C3 (outcome/two) is *not* a better extractor: them_norm 0.638 > you_norm 0.560, gap stays low (0.08),
  and own-reward (eval) *crashed* to 0.28. Adding disclosure to the pure-outcome reward made it **share
  more**, not extract more. Only "Pareto ~flat" held (jeff 0.746 ≈ base). (Caveat: C3 only reached s60 —
  it may simply not have had time to learn to exploit.)
- **H3 "info+incentive = the only big Pareto gain (C4>>C2,C3)"** -> **CONTRADICTED.** C4 ≈ C2b on every
  integrative axis; no interaction. The "big gain" the design was built around does not exist in the data.
- **H4 "two_sided > one_sided in cross-play"** -> **UNTESTED.** Cross-play was only run for c1/c2b
  (no-think); C4/C5 clusters were torn down before cross-play. Training-time C4 (0.78) >= C5 (0.74) is
  within noise.

**Pass/fail (spec's own criteria):** the "supports thesis" pattern (gain concentrated in C4, C2/C3 weak)
is **not met**. The explicit **falsification** condition ("C2 alone closes most of the gap") **is met**.

## What actually moved: distributive, not integrative

The clean, monotone signal across the 2×2 is the **you/them split**, not the pie:

- **C1 outcome/none -> pure extraction.** you_norm 0.53->0.98, them 0.54->0.03, gap ->0.95. Against a
  rubber-stamp GPT-4o-mini the your-score-only reward pays for grabbing everything; it also collapses
  the think channel to 0.9% (a terse non-reasoning over-claimer). Highest eval (0.94) because eval *is*
  own-value reward.
- **Both jointeff cells + the outcome+elicitation cell -> equitable** (gap 0.05–0.08, them_norm 0.51–0.64).
  The jointeff reward and (independently) the disclosure prompt each remove the extraction incentive.
- The actual joint-efficiency improvement over base is **marginal everywhere (+0.0 to +0.04)** — this was
  never an experiment with much integrative headroom (base already routes items reasonably well at 0.748).

So the honest framing: **the 2×2 is a study of who exploits the pushover, not who grows the pie.** The
jointeff reward's real product is *non-exploitation*; elicitation is redundant once the reward is fixed.

## Cross-play / probe corroboration (no-think transfer evals, `eval_results/`)

The held-out no-think cross-play (`EVAL_SUMMARY.md`) tells the **same story** at a different checkpoint
regime: jointeff **c2b@80 has the highest transfer joint-eff (0.890)**, outcome **c1@100 the highest own
share (0.593)**; and the exploitation probe shows **c1@100 squeezing the pushover to opp_norm 0.013
(grabs 91% of zero-value items)** while **c2b stays base-like (~0.5, ~0 gratuitous take)**. Training-time
extraction (C1 you/them 0.98/0.03) -> transfers as a learned exploitativeness; the jointeff arm does not.
Reward, not elicitation, is the axis that separates safe from exploitative.

## Caveats / confounds (don't over-read)

1. **All runs short & crashed** (C2 s50, C3 s60, others <=150) — best-checkpoint snapshots, not converged
   policies. C3's "shares more" could be undertraining.
2. **Pushover opponent** inflates training jeff/agreement and makes donation cheap; the binary-pareto
   loophole confounds C1. Trust continuous jeff + cross-play, not training `pareto`.
3. **Think-channel collapse confounds any "reasoning quality" read** — C1 thinks 0.9% at its peak; the
   jointeff cells hold only 0.32–0.48. No cell is a clean "thinking" policy at its headline checkpoint.
4. **`value_leak` on the two_sided cells is mostly the intended disclosure**, not a reward-hack (see hygiene log) — do not read C3/C4 leak as pathology.
5. **Tiny effect sizes.** jeff spread across all cells is ~0.11 and base is mid-range; "C2b wins" means
   +0.04 over base. Statistically thin on these short, single-seed runs.

## Recommendations

1. **Redesign around the real question.** The 2×2 as posed is answered: reward > elicitation, no
   interaction, gap was small. To study *integrative* skill you need **headroom and a non-pushover
   opponent** — a harder/varied opponent pool (the spec's flagged follow-up) so donation isn't free and
   joint-efficiency has somewhere to go. Run the proper cross-play for C3/C4/C5 (currently only c1/c2b).
2. **If continuing the arms:** jointeff/none (C2b recipe) is the keeper — best integrative + safe + cheap.
   Elicitation is not earning its turn-budget cost here.
3. **Fix think-collapse before claiming anything about reasoning** — none of these checkpoints support a
   "thinking helps integrativeness" claim.
4. **Multi-seed the C1 extraction result** — it's the headline safety finding and is single-seed (matches
   the open item already flagged for the c1@100 probe).
