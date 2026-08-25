# 0822 — capability control for the 10-game hole/nohole checkpoints

Question: did `mixed_hole_d1_s0` / `mixed_nohole_d1_s0` (Qwen3.6-27B, 90 steps
on the 10 chat games) gain the raw capability game-RL is supposed to lift
(SPIRAL's reasoning-transfer claim), or is the exploit/disposition movement the
only change?

Instruments (both Tinker-proxy, no GPUs, identical serving across arms):
- **MMLU** — the repo's Tier-C competence control (`ipd_exp/mmlu_eval.py`),
  logprob-scored A/B/C/D so format drift cannot masquerade as capability;
  1000 items, fixed seed. Base row pre-existing (frame-base).
- **math500** — SPIRAL's headline reasoning bench at its own eval settings
  (qwen3-self-play prompt as raw completion, t=0.6, top_p 0.95, n=4, 8192
  tokens; harness's own extract/grade), via `hole_exp/math500_proxy.py` +
  `run_math500_0822.sh`. HumanEval (the other Tier-C half) is broken repo-wide
  (missing `human_eval` module, fails on base too) and was skipped.

| arm | MMLU (n=1000) | math500 avg@4 | math500 any@4 |
|---|---:|---:|---:|
| base Qwen3.6-27B | 0.686 | 0.7525 | 0.778 |
| hole (step 90) | 0.688 | 0.7685 | 0.824 |
| nohole (step 90) | 0.682 | 0.7380 | 0.818 |

Paired per-problem deltas (n=500 problems):
- hole − base: **+0.016** (SE 0.010, 1.7σ) — a positive lean, not conclusive
- nohole − base: −0.015 (SE 0.011, 1.3σ) — null
- hole − nohole: **+0.031** (SE 0.010, 3.2σ)

Unextractable answers: 6–13 / 2000 per arm — no format-collapse confound.

## Read

1. **No meaningful capability lift from 90 steps of game RL.** MMLU is flat to
   ±0.4pp; math500 moves ≲1.6pp against base in either arm. The 0819/0820
   exploit-transfer results are NOT explained by (or accompanied by) a
   capability change — disposition moved while competence stayed put, the same
   dissociation the SPIRAL-arm study found at 4B.
2. The one nominally significant contrast, hole > nohole on math500 (+3.1pp,
   3.2σ), is between the two trained arms, both statistically compatible with
   base; with two benches × three contrasts, read it as suggestive at most.
   If it is real it is intriguing (consequence-free training slightly better
   for reasoning than punished training), but it needs seeds before it is a
   claim.
3. Caveats: single seed per arm, one eval pass, step-90 checkpoints only, and
   the serving stack is the Tinker sampler rather than the vLLM harness (a
   constant across arms, so contrasts are internally valid; absolute math500
   levels should not be compared against GPU-harness numbers elsewhere).

Raw: `ipd_exp/traits_results/{frame-base,mixed_hole_d1_s0,mixed_nohole_d1_s0}/{mmlu,math500}.json`.
