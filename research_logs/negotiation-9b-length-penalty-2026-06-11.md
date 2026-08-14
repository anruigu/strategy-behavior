# Negotiation 9B: length-runaway → no_deal collapse + sublinear length penalty (2026-06-11)

Applies to: `fleet-negotiation-grpo` (Qwen3.5-9B, outcome reward). New generator-level
reward shaper; wired into `scripts/fleet-negotiation-9b-run.sh`.

## Finding: response length runs away and triggers a no_deal collapse

From wandb (`thefleet/fleet-negotiation-grpo`, run `sjwub9f2`, 109 steps), the
`policy/response_length` (total response tokens across the multi-turn episode)
climbs steadily and then saturates the generation budget, at which point the
verifiable reward collapses:

| step | response_length | you_norm | no_deal | num_turns |
|------|-----------------|----------|---------|-----------|
| 4    | 949   | 0.40 | 0.01 | 2.4 |
| 16   | 1912  | 0.56 | 0.00 | 2.8 |
| 36   | 5995  | 0.72 | 0.13 | 3.1 |
| 44   | 5821  | 0.80 | 0.11 | 2.8 |  ← you_norm peak
| 52   | 6656  | 0.73 | 0.20 | 3.4 |
| 56   | 7103  | 0.62 | 0.30 | 3.8 |
| 60   | 7057  | 0.40 | 0.53 | 4.3 |
| 64   | 6839  | 0.12 | 0.85 | 5.4 |  ← collapse
| 108  | 1575  | 0.34 | 0.65 | 4.2 |  ← post-restart, still degraded

Generation budget ceiling = `max_turns * max_generate_length = 6 * 1024 = 6144`
(response_length counts a bit above this with appended terminators). As the
policy drifts toward the ceiling it writes longer prose and **never commits a
`<propose>`/`<accept>` in time** → the budget is exhausted → no_deal (reward 0).
The current `outcome` reward gives no gradient distinguishing a concise no_deal
from a 7k-token one, so nothing pushes back on the drift until it has already
collapsed the run. Healthy episodes sit at ~1000–2000 total tokens.

## Fix: generic sublinear length penalty in the generator

Token length is only known in the generator (not the env), so the penalty lives
alongside the other generator-level reward shapers (`zero_reward_on_non_stop`,
`apply_overlong_filtering`) rather than in `negotiation/env.py`. It subtracts
from each trajectory's **final** reward (last response token for per-token
trajectories), so even no_deal episodes (reward 0) get ordered shortest-first.

**Files:** `skyrl/train/config/config.py` (4 `GeneratorConfig` fields),
`skyrl/train/config/ppo_base_config.yaml` (defaults),
`skyrl/train/generators/skyrl_gym_generator.py` (`_apply_length_penalty`, wired
into both `generate` and `generate_batched`, logs `generate/length_penalty_mean`),
`scripts/fleet-negotiation-9b-run.sh` (`LENGTH_PENALTY_*` env vars + hydra overrides).

Form (sublinear, per request):
- `fn="power"`: `coef * (tokens / ref) ** alpha`  (sqrt at `alpha=0.5`)
- `fn="log"`:   `coef * log1p(tokens / ref) / log(2)`
- `ref` defaults to `max_turns * max_generate_length` (= 6144) when `<= 0`.

## Calibration (defaults)

`LENGTH_PENALTY_COEF=0.2`, `ALPHA=0.5`, `FN=power`, `REF=0` (→ 6144). Penalty by length:

| tokens | power penalty | log penalty |
|--------|---------------|-------------|
| 800    | 0.072 | 0.035 |
| 1500   | 0.099 | 0.063 |
| 2500   | 0.128 | 0.099 |
| 4500   | 0.171 | 0.159 |
| 6144   | 0.200 | 0.200 |

Concise (~1.5k) vs budget-saturating (~6k) differ by ~0.10 — on the scale of
`you_norm` and the `-0.1` deception penalty: a persistent nudge toward brevity
that does not punish legitimate multi-turn bargaining (1.5k→4.5k costs only
~0.07). Sublinear by design so it never dominates the task reward at the
extreme. Disable with `LENGTH_PENALTY_COEF=0`.

Watch `generate/length_penalty_mean`, `policy/response_length`,
`environment/no_deal`, and `environment/you_norm` after launch.
