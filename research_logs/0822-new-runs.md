# Adaptive-trust opponents (2026-08-22)

Added two new opponent dispositions that sit *between* the existing endpoints
(`nohole` = punish from the first betrayal, `hole` = never punish), modelling a
counterpart that loses trust as it gets exploited. Plan:
`adaptive_trust_opponent_b2b11d9e`.

- **`adaptive` (permanent).** Stochastic grim trigger: behaves nerfed until it
  fires, then retaliates for the rest of the episode. Per-round hazard rises
  with the learner's *cumulative* betrayals, `h = clamp(base + slope*n, 0, cap)`,
  and never recovers. Draws on the betrayal itself (not every subsequent round)
  so one late slip isn't near-certain to be caught.
- **`adaptive_recover` (forgiving).** Per-round retaliation, not permanent. A
  distrust meter rises on each betrayal and decays toward zero on cooperative
  rounds, `h = clamp(base + slope*distrust, 0, cap)`, so the counterpart can be
  won back.

Both are tuned to be **priced** (always-exploit ends below reciprocal honesty)
with a real **gradient** (one early exploit usually escapes), so there's a
learnable signal between the endpoints.

## What we built

- **`core.py`:** `GrudgeTrigger` / `DecayingGrudge` next to `Draws` (seeded via
  `Draws` so references replay). Hazards fitted per (env, arm) by
  `tune_adaptive.py`, stored in `core.ADAPTIVE_TUNING`; the three temperaments
  (wary / volatile / stoic) are shared relative multipliers in
  `core.ADAPTIVE_SHAPE`. `CONSEQUENCE` stays `("hole","nohole")` — the adaptive
  arms are `populations()`/`play_episode` keys only, so audit/gates keep
  iterating hole/nohole by default.
- **Envs:** adaptive + adaptive_recover populations wired into every
  opponent-swap cell, each delegating to the env's existing *nerfed* behavior
  until the trigger fires and its *punishing* behavior after —
  `game_env.py` (ipd3/staghunt/winasmuch), `ipd_env`, `trust_env`, `dond_env`,
  `pubgoods_env`, `ultimatum_env`.
- **Training:** `train_mixed.py --consequence adaptive | adaptive_recover`;
  runs labelled `mixed_disp_adaptive_*` / `mixed_disp_adaptrec_*`.
- **Gates:** `check_suite.py` adaptive check (priced + early-exploit gradient) —
  **10/10 cells pass** in both arms at training dose.
- **Eval/analysis:** `eval_dispositions.py`, `probe_recovery.py`,
  `eval_capability.py`, `analyze_discrimination.py` extended to score all four
  dispositions; readout in `results/ADAPTIVE-DISPOSITIONS.md`.
- **Launcher:** `sbatch_dispositions.sh --all` submits four arms
  (`nohole`, `regmix`, `adaptive`, `adaptive_recover`) x 2 seeds on the shared
  7-env roster (`ipd public_goods dond trust ipd3 staghunt winasmuch`,
  `--groups 14 --dose 1.0 --model Qwen/Qwen3.6-27B --steps 90 --group-size 6`),
  `ultimatum` held out. `--label-suffix disp` so it doesn't clobber the old
  ten-env nohole/regmix dirs; one job per node (packing killed earlier arms).

## Two leaks the tuning surfaced (fixed)

- **trust:** a punished (empty-pot) round reset `last_return_share`, so the
  stake returned at full size the next round — always-betray collected the whole
  pot every other round. `AdaptiveInvestor` now remembers the last real return.
- **dond:** credibility hitting zero collapsed the counterpart's reservation, so
  greedy proposals were auto-accepted and the hazard firing *paid*. The
  recovering arm (which never walks) now keeps its reservation.

## What the readouts show

- Base model (Qwen3.6-27B) can't read its counterpart — no monotone ordering
  across arms; the grudge fires in 0–8% of episodes vs 25–83% for `nohole`,
  because the base policy rarely betrays. Adaptive arms ≈ hole arm at base
  rates by design; they diverge only once RL pushes exploitation up.
- On a trained checkpoint with real exploitation (`public_goods`), the ordering
  the design predicts appears: after the first retaliation the policy backs off,
  and it backs off **less** against the forgiving arm (0.94→0.58) than the
  permanent one (0.98→0.27). The two arms are distinguishable from each other
  and from both endpoints on the same policy.
- `probe_recovery.py` confirms trust actually rebuilds under `adaptive_recover`
  (stake climbs 0.01→0.70 of opening in `trust`) while `adaptive` stays flat.
  `dond`/`ultimatum` are floor-limited on this model (≈0 exploit rate) — treat
  flat curves there as "never explored", not "no disposition formed".

## Live runs launched

`mixed_disp_adaptrec_d1_s0` (`250n2adq`) and `mixed_disp_adaptive_d1_s1`
(`s3x1e68e`) probed at step 22: `recovered` is 0.00 in every permanent cell and
non-zero in recovering cells — the arms do the different things they were built
to do. Coverage (not correctness) is thin this early; most cells don't yet
exploit enough to trigger.

## New runs
Launch nohoe/adaptive/adaptive-recover runs with thinking on.

## Endgame beahvior eval awareness?
(Another hypothesis I have is reinforcing end-game behavior will have the model score higher on scheming evals. we'll see if end-game behavior emerges on these runs and run misalignment evals later)
also one ablation have a hidden endgame behavior penalty that is applied every time the agent waits till the end to betray (but don’t tell the agent why), and see whether reward-seeking behavior emerges.

## Inifinite horizon variants
Maybe also another with no-hole but don’t tell the agent how many total rounds there are, so we don’t get endgame behavior. see if anything's different




### Wired up (2026-08-22)
A hidden, opt-in reward-shaping knob. Any betrayal that lands in the final
window of the episode (last `frac` of the *scored* decisions, `frac=0.25`,
window `= ceil(frac*n_scored)`, at least one round) docks the **training reward
only** — `payoff`, the scripted references and `capture` are all left raw, so
capture still measures what the policy did and only the gradient feels the
penalty. The agent is never told: no `play_episode` reads the knob (it is
applied after the episode in `registry.rollout`), so nothing in the observation
or the opponent's lines can disclose it. Orthogonal to the disposition axis —
it layers on whatever arm (`hole`/`nohole`/`adaptive`/`adaptive_recover`) the
run draws.

- **`core.py`:** `endgame_config`/`endgame_window`/`endgame_penalty` next to the
  horizon helpers. Price per late betrayal is `margin * premium / n_scored`
  (relative to the premium, like `game_env.PENALTY_MARGIN`, so it bites evenly
  across cells). `episode_record` now carries an ordered `exploit_steps`
  timeline (one bool per scored decision, `len == scored_decisions`,
  `sum == exploit_decisions`) — the *when* the two scalar counts drop.
- **Every env** emits `exploit_steps` from its existing exploit/betrayal
  counter; verified across all 30 registered cells (`len`/`sum` invariants,
  240 rollouts).
- **`registry.rollout`:** reads the knob off `cfg`, computes the penalty from
  `exploit_steps`, records `endgame_betrayals/window/penalty/rate` in `stats`,
  and sets `score = (payoff - penalty) / payoff_scale`. No-op when off.
- **Training:** `train_hole.rollout` now forwards a `cfg` built from its args;
  `train_mixed.py --endgame-penalty MARGIN [--endgame-frac FRAC]` turns it on,
  tags the run label `_eg<margin>`, and logs `train/endgame_rate` so we can
  watch whether the endgame-betrayal rate falls over training (the
  reward-seeking readout). `check_suite`'s pre-launch gate is unaffected (it
  reads raw payoff).
- **Tests:** `test_envs.py` — config validation, the `exploit_steps` invariants
  per cell, default-off byte-identical, penalty hits `score` not
  `payoff`/`capture`, honest reference spared, and the learner transcript is
  byte-identical with the knob on (hidden).

Launch (mirrors the disposition roster; the penalty is on top of the arm):

```
python train_mixed.py --consequence nohole --endgame-penalty 2.0 \
  --envs ipd public_goods dond trust ipd3 staghunt winasmuch \
  --groups 14 --dose 1.0 --model Qwen/Qwen3.6-27B --steps 90 \
  --group-size 6 --label-suffix disp
```