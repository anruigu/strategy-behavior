# 35B thinking run: grad-norm explosion → token-repetition collapse → reward regression (2026-06-12)

**Run:** `fleet_qwen35_35b_negotiation_dnd_outcome_thinkon_fix` (wandb `mvqhhips`)
**Cluster:** `sky-a904-allie-bbc49167` · SLURM 2980 · node-1/2 · RunPod. Reward mode `outcome`, thinking ON.
**Status at writing:** alive, step ~120/3380. **Reward has regressed ~30% off peak and is degrading.** Not an infra or memory failure — it's optimizer instability driving output degeneracy.

## What happened (the arc)

Reward peaked at **step ~74 (0.827)** when the policy had found a *concise, decisive* strategy (~288 tok/rollout, 1.7 turns, propose-and-close). From there it regressed to **~0.53–0.61** by steps 100–120, while `grad_norm` exploded ~100× and output length re-inflated.

| step | reward | grad_norm | resp_len | tok_mean (dump) | repeat-degenerate rollouts |
|------|--------|-----------|----------|-----------------|----------------------------|
| 68   | 0.792  | 4.6   | 1296 | —    | — |
| 74   | **0.827** (peak) | 16.3  | 1359 | 288 | **0 / 128** |
| 80   | 0.720  | 51.6  | 3391 | —    | — |
| 84   | 0.752  | 124.8 | 963  | —    | — |
| 88   | 0.690  | 207   | 1824 | —    | — |
| 90   | 0.684  | 173   | —    | 324  | 4 / 128 |
| 100  | 0.525  | 473   | 2872 | 374  | 9 / 128 |
| 110  | 0.542  | 378   | 4385 | 572  | 39 / 128 |
| 116  | 0.570  | 480   | 8359 | —    | — |
| 119  | 0.606  | —     | 9044 (max) | 936 | **70 / 128 (55%)** |
| 120  | 0.527  | 272   | 6260 | —    | — |

Reward variance also rose (per-rollout sd 0.225 → 0.342): the policy became erratic, not uniformly worse. `no_deal` stayed low (≤0.05) and memory was flat the entire time (**peak 80% / ~115 GB, 0 ECC, no OOM**) — memory is *not* involved.

## Yes — the first ~74 steps were genuine, real improvement

Before the blowup the run learned well, and the gains were *real skill*, not reward-hacking:

| step | reward | no_deal | you_norm | resp_len |
|------|--------|---------|----------|----------|
| 6    | 0.445  | 0.086   | 0.50 | 5533 |
| 12   | 0.396  | 0.133   | 0.44 | 5183 |
| 24   | 0.525  | 0.047   | 0.57 | 3574 |
| 42   | 0.626  | 0.055   | 0.66 | 1806 |
| 54   | 0.677  | 0.008   | 0.70 | 1958 |
| 60   | 0.738  | 0.023   | 0.76 | 1162 |
| 72   | 0.804  | 0.008   | 0.82 | 1175 |
| 74   | **0.827** | 0.000 | **0.82** | 1359 |

All three quality axes moved the right way *together*: **you_norm 0.44 → 0.82** (better own-value capture), **no_deal 0.13 → ~0** (closes deals), **length 5500 → ~1200** (more efficient, not padded). That co-movement is the signature of genuine learning, and it matches the `proactive.md` prediction that thinking sharpens own-value optimization. The step-70/72 checkpoint is a genuinely strong policy — which is exactly why it's the right restart point. By step ~78 the rollover had already begun (0.74, grad_norm 23).

## The mechanism (chain of causation)

1. **Over-sharpening → entropy collapse.** Around step 68–74 the policy converged hard on one concise high-reward script (reward 0.83, you_norm 0.82, ~1k tokens). With no entropy floor, policy entropy cratered.
2. **Gradient explosion.** A near-deterministic policy makes GRPO importance ratios extreme on the few off-distribution samples, so the policy-gradient norm blew up: **4 → 25 → 52 → 125 → 207 → 473 → 530** over steps 56→113. `max_grad_norm=1.0` clips the *update*, but a pre-clip norm of ~500 means the clipped step is dominated by a handful of high-ratio samples — i.e. each update is a noisy, near-unit-norm shove in a bad direction.
3. **Token-repetition format collapse.** Those destructive updates pushed the policy into a degenerate region. A growing fraction of rollouts emit runaway repeated tokens instead of a valid action — e.g.:
   ```
   <accept < < < < < < < < < <如果 < < < < points < <得分 < < <4 < < < made <
   ```
   This is classic output collapse (repeated `<` tokens with random Chinese/number fragments). The degenerate fraction tracks grad_norm precisely: **0/128 (step 74) → 9 (100) → 39 (110) → 70/128 (119)**.
4. **Malformed action → env error → length blow-up.** The garbage never closes a valid `<accept>`/`<propose>`, so the env replies "It looks like there was an error in your message," the episode burns turns, and `response_length` re-inflates 1k → 6–9k tokens (the same length-drift pathology seen in the 9B run, here *caused by* the optimizer rather than reward shaping). These rollouts earn ~0 or negative reward (e.g. a 9044-tok, 5-turn rollout scored **−0.086**).
5. **Reward regression.** Healthy rollouts still score well, so reward didn't crash to zero — it regressed to ~0.55 with high variance as 40–55% of the batch degenerated.

## Root cause

Insufficient regularization against entropy collapse, on a 35B that converges fast:
- **`kl_loss_coef: 0.001`** — KL-to-reference penalty is essentially negligible.
- **`entropy_coeff` ≈ 0** (no entropy bonus; `policy/entropy` isn't even logged) — nothing holds entropy up.
- **`lr: 5e-6`, no decay** — constant LR keeps pushing after the policy has already converged (~step 70), so it over-optimizes into the unstable regime.
- `max_grad_norm: 1.0` clips magnitude but cannot fix the *direction* problem once ratios explode.

So: policy finds a good concise strategy ~step 70 → unregularized over-optimization collapses entropy → GRPO gradients explode → clipped-but-destructive updates induce token-repetition degeneracy → malformed actions, length blow-up, reward regression.

## Recommendations for next run

### A. Stop the entropy collapse → grad explosion (root cause)
1. **Add an entropy floor.** Set `entropy_coeff` ≈ **1e-3 to 1e-2** (currently ~0; `policy/entropy` isn't even logged — turn that logging on too). This is the single most direct fix.
2. **Strengthen the KL anchor.** Raise `kl_loss_coef` from **0.001 → ~0.01–0.05**. At 0.001 the reference policy exerts essentially no pull, so nothing stopped the drift into the degenerate region.
3. **LR decay / lower peak LR.** Current `lr=5e-6` constant. Add cosine or linear decay (or drop peak to ~2–3e-6). The policy had effectively converged by ~step 70; continued full-LR updates drove the over-optimization.
4. **Watch grad_norm as a tripwire.** It's the leading indicator here — it left its ~3–5 band ~20 steps *before* reward visibly regressed. Auto-checkpoint-on-best-eval and/or early-stop when grad_norm sustains >~30 would have saved this run.

### B. Recalibrate the length penalty (LP) — it was inert this run
Current: `length_penalty_coef=0.2`, `length_penalty_alpha=0.5`, `length_penalty_fn=power`, **`length_penalty_ref=0`** → ref auto-defaults to `max_turns × max_generate_length = 6 × 8192 = 49,152` tokens.

Problem: healthy episodes are ~**300–1,500 tokens**, i.e. ~3% of that 49k reference, so the power penalty `0.2·(tok/49152)^0.5` evaluates to only **~0.02** (confirmed: `generate/length_penalty_mean` logged 0.019–0.024 at steps 117–120). The LP gave **no meaningful gradient against length re-inflation** — even a 9k-token degenerate rollout was only docked ~0.086. It is calibrated to the wrong scale.

Suggested for next run:
- **Set `length_penalty_ref` explicitly to the *operating* scale, not the ceiling** — e.g. **`LENGTH_PENALTY_REF≈1500–2500`** (≈ the healthy episode length). Then a ~1k-tok concise deal costs ~0.16 and a 6k-tok ramble costs ~0.4, a real ordering signal.
- Alternatively/also raise **`LENGTH_PENALTY_COEF` 0.2 → ~0.4–0.5** so it's on the scale of the task reward.
- Keep `fn=power`, `alpha=0.5` (sublinear is right — don't punish legitimate multi-turn bargaining), but with the corrected `ref` it will actually bite.

### C. Cap the degenerate length / kill malformed rollouts
5. **Lower `max_generate_length` 8192 → ~2048–3072.** The healthy regime never needed >~1.5k/turn; the 8192 ceiling is pure headroom for runaway repetition (degenerate rollouts maxed at 9,044 tok).
6. **Penalize the repeated-token / malformed-action failure directly.** The collapse rollouts emit `<accept < < < < …` that never parses; `zero_reward_on_non_stop=false` and `apply_overlong_filtering=false` let them through. Enable a **format/parse penalty** (negative reward when no valid `<propose>/<accept>/<deal>` is emitted) and/or `apply_overlong_filtering=true` so they don't pollute the batch and inflate variance.

### D. Operational
7. **Restart from the pre-blowup checkpoint.** `ckpt_interval=10` → step 70 checkpoint exists, before grad_norm left its band and before any degeneracy (0/128 at step 74). Resume from step 70 with A+B+C applied rather than continuing the current trajectory.
8. **Select the deployment checkpoint by eval, not by last-step** — peak eval was ~step 70–74; without best-checkpoint tracking the run silently regressed past its own best.

## Where the step-70 gains come from: distributive, not integrative (eval analysis)

Side-by-side eval of **base (step 0, untrained)** vs the **step-70 checkpoint** on the fixed 64-scenario × 3-sample DnD val set (192 traces each; allocation reconstructed per trace via the env's `game.py`, score-matched and validated 192/192 at step 70). Tool: `/workspace/allie/eval-compare/` (web UI).

| metric (mean over eval) | Base | Step-70 |
|---|---|---|
| **your** normalized score (= reward) | 0.531 | **0.793** |
| **opponent** normalized score | 0.537 | **0.261** |
| Pareto-optimal rate (of agreements) | 27% (45/166) | **19% (37/192)** |
| joint efficiency (joint / max-joint) | 0.748 | 0.716 |
| reached a deal | 166/192 (86%) | **192/192 (100%)** |
| took the **entire** pool (opp = 0) | 25/192 (13%) | **113/192 (59%)** |

**The reward gain is almost entirely distributive (a bigger slice), not integrative (a bigger pie).** Your score rose +0.26 while the opponent's *fell* −0.28; the total pie (joint efficiency) was flat-to-down, and the **Pareto rate actually dropped**. Two mechanisms:
1. **Stopped mis-allocating against its own values.** The base model frequently keeps items worth 0 to it. E.g. scenario #12 (you value book 6, ball 4, hat 0): base kept `[0,4,0]` — all four *worthless* hats — scoring **0/10**; step-70 kept `[1,4,1]` (the whole pool) for **10/10**. Fixing this self-defeating behavior is real, legitimate skill.
2. **Learned to extract from a pushover opponent.** Step-70 takes the *entire* pool in **59%** of evals (base: 13%), driving opp score 0.54→0.26. Against a fixed GPT-4o-mini that rubber-stamps, your-score-only `outcome` reward pays for grabbing everything — exactly the reward-hacking pattern flagged in `proactive.md` (value-blind accepter) and the monitor runbook.

Caveat on "improvement": it *is* a real eval win on the trained objective (your normalized points), and closing 100% of deals is genuine. But it is **not** evidence the policy got better at *negotiation* in the integrative sense — it got better at **claiming**. This is the concrete empirical case for the planned **`outcome_pareto`** ablation: reward joint/Pareto outcomes so the gain comes from finding mutually-better trades rather than from exploiting a weak opponent. (Sort the eval UI by "Δ regressed" to see the 7 scenarios where over-claiming backfired.)

## Thinking-channel abandonment + private-value leak (eval analysis)

Comparing base vs step-70 on the val set surfaced a second, independent degeneration in *how* the policy uses the `<think>` channel. Counting non-empty `<think>…</think>` in the policy's eval output:

| | Base (step 0) | Step-70 |
|---|---|---|
| traces with a `<think>` tag | 148/192 | 191/192 |
| **non-empty** reasoning inside `<think>` | **129/192 (67%)** | **42/192 (21%)** |
| **empty** `<think></think>` (tag present, blank) | 19/192 (9%) | **149/192 (77%)** |

**The traces are saved fine** — the dump and the eval UI carry the full `<think>` blocks. The problem is the step-70 policy largely **stopped using** the channel: it emits an empty `<think></think>` and writes its reasoning in the *visible* response instead.

**Why this matters — it leaks private values to the opponent.** The env's `_strip_think` removes only text *inside* `<think>…</think>` before forwarding the policy's message to the opponent LLM. When the reasoning sits *outside* the (empty) tag, it is sent verbatim. Observed step-70 examples broadcast the policy's hidden valuations directly:
> "Since I value the hat at 6 points and the others at only 1 point each, I should aim to keep the hat…"
> "Since I value the balls at 5 points each but the books and hats at 0, I should propose keeping all the balls…"

So the policy is **telling a (fixed, pushover) opponent its private values** — which plausibly reinforces the distributive dynamics above (the opponent's prompt makes it amenable, and explicit value statements make one-sided splits easy to rubber-stamp). Two interpretations, both plausible: (a) the model learned that open reasoning is harmless/useful against this opponent, or (b) the thinking format is simply decaying (consistent with the broader output degeneration). Either way it defeats the point of the thinking arm.

**Likely cause / fixes for next run:**
- Stop strings for the thinking arm drop `</think>`, and the reward never rewards *using* the think block, so there is no pressure to keep reasoning inside it. Consider: (1) a **format reward** that requires a non-empty `<think>` and penalizes strategic prose outside it; (2) **leak detection** — penalize messages whose opponent-facing text reveals own values (the env already has `_deceptive_promises` machinery to build on); (3) re-add `</think>` handling so the reasoning block is well-formed. Track a `think_nonempty_rate` metric so this is visible during training, not only in post-hoc eval.

## Bottom line

Reward did regress (peak 0.83 → ~0.55), and the user's read is correct. The driver is **optimizer instability (grad_norm 4 → 500) from entropy collapse under near-zero KL/entropy regularization**, which spread a **token-repetition output collapse to ~55% of rollouts**. Memory and infra are healthy and uninvolved. Fix is regularization (entropy/KL/LR) + restart from the pre-blowup checkpoint.

## Live confirmation on the stabilized rerun (`baseline_v2`, ~step 30): the leak is reward-positive, weak penalties don't hold

Reran `outcome`+thinking with the fixes: entropy floor (`use_entropy_loss=true`, coef 0.005) + `kl_loss_coef=0.02` + `max_grad_norm=0.5`, length-penalty `ref=1500`, `max_generate_length=4096` + `apply_overlong_filtering`, plus first-pass thinking-channel penalties `value_leak_penalty=-0.05`, `empty_think_penalty=-0.02`, and new in-training metrics `think_nonempty_rate` / `value_leak_msgs` / `empty_think_msgs`.

**The optimizer fix worked**: `grad_norm` held ~2.4–6.7 through step 31 (vs 4→500 before); train reward climbing (0.27→0.375); eval flat near baseline — no explosion, no token-repetition collapse.

**But the thinking-channel abandonment + value leak recurred**, and the new metrics quantify it live (instead of post-hoc):
- `think_nonempty_rate` decayed monotonically **0.40 → 0.35 → 0.31 → 0.28** (steps 1→31).
- At ~step 30, over 332 policy turns: **65% emit an empty/absent `<think>`**, with a **median 205 chars of open prose** (i.e. reasoning dumped in the clear, *not* terse), and **20% leak own values** to the opponent (24% among empty-think turns). Examples: *"keep all 4 books **(8 points)**, the hat **(2 points)**… the ball is **worthless to me**"*; *"the ball is **worth 8 of my 10 points** and the hat is **worth 2**."*

**Mechanism — the leak is reward-positive (why −0.05 is too weak).** Disclosing your valuations to the fixed pushover gpt-4o-mini makes it rubber-stamp your one-sided split → the deal closes → higher `outcome` reward. GRPO therefore has a *gradient toward* leaking, and a −0.05 nudge is trivially overwhelmed. This is the **same value-blind-accepter reward-hack** (`proactive.md`) surfacing through the thinking channel rather than the `<propose>` JSON — and it confirms the original step-70 finding above was the harmful pattern, not format decay. It is **not** harmless conciseness.

**Action.** To suppress it in-baseline the penalty must flip the sign of the incentive: bumped to `value_leak_penalty=-0.25`, `empty_think_penalty=-0.1` (~5×) for the C1/C2 reruns; if still leaking, escalate to a prompt-level "keep ALL reasoning inside `<think>`" instruction + a positive format reward for a non-empty block. (Caveat for interpretation: in the *pure* `outcome` arm this leak is arguably the reward-hack the 2×2 is meant to expose; we suppress it here because the user wants a clean thinking channel in the baseline.)

## Overnight 5×-penalty reruns + jointeff stabilization + elicitation (2026-06-13)

Relaunched both arms with the 5× anti-leak penalties (−0.25/−0.1) the user requested, then iterated. Findings:

**C1 (outcome/none, −0.25 leak penalty):** leak suppression *worked* — `value_leak`→0 by ~step 75 and stayed there; eval climbed to a peak **0.94 (~step 105-119)**. Then it **overfit/collapsed**: grad_norm exploded 215→**2525** (step 109), `think_nonempty` cratered 0.43→**0.01** (think channel fully abandoned — the policy stopped leaking by going terse/no-reasoning), and eval regressed 0.94→0.74. The entropy(0.005)+KL(0.02) floors **delayed** collapse (~step 105 vs the original ~70) but did not prevent it on the outcome arm. Peak banked; killed at step ~140 to free nodes. Best-eval checkpoint ≈ step 110.

**Jointeff arm — leak-vs-stability tension (key finding):**
- Original C2 (−0.25 leak penalty + jointeff reward + weak reg kl=0.05/lr=5e-7/clip=0.5): **KL/grad runaway** — grad 4→54, KL→1.8 (25× baseline), entropy decay, reward regression by ~step 55. The −0.25 penalty drove too-fast a behavior shift for the higher-magnitude jointeff reward to absorb.
- C2b (−0.12 leak penalty + **stronger reg** kl=0.1/lr=3e-7/clip=0.3/entropy=0.01): **stable** — grad *contained* at ~20-30 (volatile, not exploding), entropy held ~0.5, eval ~0.88. BUT `value_leak` returns (~0.4-0.6, slowly declining) — −0.12 is too weak to suppress it on jointeff.
- **Conclusion:** on the jointeff arm, leak-suppression (−0.25) and stability are in tension; the jointeff reward appears to *reward* value disclosure (it enables better joint trades vs the pushover), pulling harder toward the leak than the outcome arm does. Untested sweet spot: −0.25 penalty *with* the strong reg. Left for the human — it's a research call, not brute-forceable overnight.

**Elicitation wired (C3/C4 now launchable):** `NEGOTIATION_ELICIT=two_sided` → the pre-existing `--proactive` mutual-disclosure prompt (ask their priorities + state yours, route by value), injected into both system prompts. Launched **C4 = jointeff + two_sided**, identical to C2b except the elicitation flag (leak penalty held at −0.12 in both so C2b-vs-C4 isolates the elicitation effect). C5 (one_sided) needs an ask-only prompt variant (not yet built) + a free good node pair (only the broken 8/9 + untested 10 are idle).

**Infra:** `sky launch` throws `OSError: Argument list too long` at slurm run-submit beyond ~14 `--env` flags; fix was baking tuning/length values into the run script as defaults (also improved the recipe). Baked: jointeff stabilization defaults (PARETO_ARGS), `MAX_GENERATE_LENGTH=4096`, `LENGTH_PENALTY_REF=1500`.

## Behavioral / pathology audit across all 5 runs (2026-06-14)

Goal: make sure cross-cell conclusions rest on clean checkpoints, not degenerate ones. Method: wandb env-metrics (deception/value_leak/empty_think/think_rate/no_deal) at best+late steps for all 5; trace scan of the S3 eval dumps (C1, C3) + live cluster dump (C4) for 192 dnd traces each (think-abandonment, malformed-action, token-repetition collapse, truncation, value-leak). C2b/C5 eval dumps never reached S3 and their clusters are down → metrics-only for those two.

### Headline: NO degenerate-output pathology at any *best* checkpoint
Across C1/C3/C4 best-checkpoint traces: **malformed-action 0%, token-repetition collapse 0%, length-truncation 0%.** The original grad-explosion degeneracy (`<accept < < <得分 …`, runaway length, malformed actions) is **gone** — the entropy/KL/grad-clip stabilization fixed it. All best checkpoints close deals (agreement 95-98%, no_deal ≤5%). So the runs are safe to compare at their best checkpoints.

### Use BEST, never LATE — late checkpoints ARE pathological
- C1 step110(best): avg score 0.943, 3% zero-score. → C1 step130(late): **34% zero-score**, avg 0.610 — degraded post-collapse.
- C3 step50(best): 22% zero. → step60(late): 33% zero. Same direction.
Conclusion: draw conclusions only from C1→**s110**, C2b→**s90**, C3→**s50**, C5→**s60-70**, C4→**s70**. Never the last checkpoint.

### Per-cell behavior at best checkpoint
| cell | empty-think | value-leak | deception | what it's doing |
|---|---|---|---|---|
| **C1** out/none s110 | **100%** | 0% | 0 | **Think-ABANDONED** terse over-claimer: `<think></think><propose>{book:2,hat:1,ball:2}</propose>` (grabs ~whole pool, score 0.94). Clean on leak/decep *only because it doesn't reason at all*. |
| **C2b** joint/none s90 | ~81%* | 0.41/ep | 0.06 | partial thinking (rate 0.48), moderate leak; over-claims less than C1. |
| **C3** out/two s50 | 26% | **41% of traces** | 0.09 | **Thinks (74%)** but discloses exact values in the open (*"I value the hat the most (6 points)…"*); 22% fail; low score (0.28). |
| **C4** joint/two s70 | mixed (rate 0.41) | 40% of traces | **0.24** | Mix of GENUINE elicitation (*"which items do you value most? I personally value the book most…"* → proposes book, consistent) AND value-leak-in-open (*"I value balls at 5 pts each, take all the balls"*, score −1.06). |
| **C5** joint/one s70 | (rate 0.35) | 0.42/ep | 0.13 | one_sided: leak < C4 (asks but keeps values private — validated). |
(*empty-think % over-counts on multi-`<think>` traces; trust the wandb `think_nonempty_rate`.)

### New behavioral issues (beyond deception/leak)
1. **Think abandonment is the dominant issue.** The "thinking arm" stops thinking as it over-trains — C1 reaches 100% empty `<think>` at its eval peak; the jointeff cells hold a partial 0.35-0.48 think-rate. **Any conclusion about reasoning quality from C1's headline checkpoint is invalid** — that policy is a non-thinking over-claimer. The `-0.06/-0.1` empty-think penalty slowed but didn't stop it.
2. **"value_leak" on the two_sided arms (C3 41%, C4 40%) is mostly the INTENDED disclosure**, not a reward-hack — two_sided literally instructs "state your priorities." Interpret it as the treatment, not a pathology. It IS entangled with genuine value-leak-in-the-open (reasoning dumped visibly), so it's not a clean disclosure signal either.
3. **Deception (prose-vs-JSON) is elevated on C4 two_sided (0.24/ep)** — but spot-reads show most flagged "deceptive" prose is actually consistent elicitation; the detector likely over-fires on disclosure prose. Treat C4 deception as a soft flag, not confirmed manipulation.

### Bottom line for drawing conclusions
- **Safe**: comparing best checkpoints for outcome (you_norm/them_norm split, agreement, score) and for the distributive vs integrative story — none are degenerate.
- **NOT safe**: any "thinking helps / reasoning quality" claim from C1 (it doesn't think at its peak); any claim from a *late* checkpoint; reading the two_sided `value_leak` as reward-hacking (it's the treatment).
- **Cleanest cells for thinking-related claims**: the jointeff cells (C2b/C4/C5) retain partial thinking; the outcome cells collapse the channel hardest.
