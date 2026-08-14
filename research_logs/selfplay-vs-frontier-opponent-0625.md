# Self-play vs frontier-opponent training: which opponent going forward? (2026-06-25)

## Question
We now have two checkpoints trained with the **same** task setup (Qwen3.5-35B-A3B, dnd, `single`
protocol, `outcome` reward, thinking ON, `can_ask` elicitation on both seats) that differ in **who
the policy trains against**:

- `fleet_qwen35_35b_negotiation_dnd_outcome_selfplay-canask-0621` — opponent = the **live policy
  itself** (self-play; opponent routed at the policy's own vLLM HTTP endpoint, `$0` external API).
- `fleet_qwen35_35b_negotiation_dnd_outcome_enforce-penalty-fix-canask-0620` — opponent = a **fixed
  frontier model** (`gpt-4o-mini`, via OpenRouter), the penalty-enforcement arm with the stability
  fix (`presence_penalty=0`, `kl_loss_coef=0.05`) from `debug_logs/why-the-penalty-arm-diverged-0620.md`.

Both are compared at **global_step_30** on the held-out frontier cross-play matrix
(`eval/results/crossplay_matrix_{s30,enfpen_s30,base}_canask.json`; dnd/val, n=16, max_turns=6,
seed=1, can_ask both seats, think-gate OFF so behavior transfer is real). `Base-qwen35-35b`
(pre-RL, thinking-on, OpenRouter) is the reference anchor. Goal: decide whether **self-play** or
**training against a frontier opponent** is the better track going forward, and address the standard
objections to self-play with what the data actually shows.

## Caveats up front (read before trusting any number)
1. **Step 30 is early.** Neither trained arm has beaten the strong think-on `base` on cross-play yet
   (see table). This comparison is about *relative behavior and trajectory*, not a final verdict on
   either checkpoint's quality.
2. **Not a perfectly clean one-factor A/B.** The dominant difference is the opponent (self vs
   gpt-4o-mini), but the recipes aren't byte-identical: the self-play arm is the raw-baseline recipe
   (behavior penalties off), while the enf-pen-fix arm additionally carries the penalty-enforcement +
   `presence_penalty=0`/`kl=0.05` stability fix. Treat the opponent as the *main* driver, not the only one.
3. **`gpt-4o-mini` is a cheap/weak frontier opponent.** "Training against frontier" here means a
   fixed, relatively weak adversary — which is itself part of the argument below.
4. The s30 self-play JSON lacks the `nash`/`seatB` arrays (not recomputed); seat-symmetric cell
   metrics (agreement, joint-efficiency) are still available for both seats.

## The numbers (policy seat, averaged over the 5-model frontier pool)
Frontier pool = GPT-5.5, Opus-4.8, Gemini-3.1-Pro, Llama-3.3-70B, Qwen3.5-9B.

**Policy as OPENER (seat A) vs the frontier pool:**

| metric | self-play s30 | enf-pen-fix s30 (frontier-trained) | base (anchor) |
|---|---|---|---|
| own outcome `you_norm` | 0.536 | **0.555** | 0.695 |
| agreement | 0.838 | **0.913** | 1.000 |
| **joint-efficiency** | **0.853** | 0.799 | 0.922 |
| nash product | n/a* | 0.358 | 0.477 |

**Policy as PARTNER (seat B), frontier opens (seat-symmetric cell metrics):**

| metric | self-play s30 | enf-pen-fix s30 | base |
|---|---|---|---|
| agreement | 0.975 | 0.988 | 1.000 |
| joint-efficiency | 0.864 | 0.858 | 0.872 |

**Mirror cell (policy vs an identical copy of itself):**

| metric | self-play s30 | enf-pen-fix s30 | base |
|---|---|---|---|
| outcome | **0.356** | 0.119 | 0.719 |
| agreement | **0.563** | 0.313 | 1.000 |
| joint-efficiency | **0.740** | 0.658 | 0.935 |

\* nash not present in the s30 self-play JSON.

## Reading the comparison
- **Self-play grows the pie more; frontier-training grabs slightly more of it.** Against real
  frontier opponents the self-play policy posts the higher **joint-efficiency as opener (0.853 vs
  0.799, +5.4pts)** — the integrative metric we actually care about (`proactive.md` autopsy: the
  residual loss is failure to find the win-win trade). The frontier-trained arm instead edges
  own-outcome (0.555 vs 0.536) and agreement (0.913 vs 0.838): it closes more deals and extracts a
  bit more, but the deals it strikes leave more joint surplus on the table. Self-play walks away from
  more marginal deals but the deals it makes are more efficient. As partner the two are a wash
  (joint-eff 0.864 vs 0.858).
- **Self-play is dramatically better at coordinating with itself.** In the mirror, self-play reaches
  agreement 0.56 / outcome 0.356 / joint-eff 0.74, versus the frontier-trained arm's 0.31 / 0.12 /
  0.66. Training against a fixed external opponent leaves the policy *unable to negotiate with its own
  kind* — exactly the population it will face if deployed as a fleet, or if used for any
  self-improvement / debate / multi-agent loop. Self-play co-evolves both the proposer and the
  accepter, so the information channel the autopsy flagged as the binding constraint gets exercised
  from both sides at once.
- **Neither has caught base at s30.** The think-on base is still ahead on own-outcome and
  joint-efficiency. This is the early-checkpoint caveat, not a self-play indictment — but it means the
  headline going-forward claim rests on *behavioral trajectory*, not current dominance.

## Common concerns with self-play — and what the data says
1. **"Self-play collapses into a non-transferable secret handshake / collusion."** The cross-play
   matrix *is* the test for this: it scores the self-play policy only against held-out frontier models
   it never trained on. If it had learned a private convention, those cells would crater. They don't —
   frontier joint-eff (0.853) and own-outcome (0.536) are competitive with the frontier-trained arm.
   No evidence of a non-transferable convention at s30.
2. **"Self-play degenerates into trivial mutual agreement (always-accept / blind even split)."** That
   would show as mirror agreement → ~1.0 with a flat 50/50 split. Instead mirror agreement is only
   **0.56** — the two copies are, if anything, *over-demanding* on each other, not rubber-stamping.
   The failure mode to watch is mutual greed, not collusive cooperation.
3. **"A non-stationary (moving-target) opponent destabilizes training."** The self-play training log
   says otherwise: `policy_kl` crept 0.000 → ~0.08 over 30 steps, `grad_norm` stayed ~0.8–1.4, and
   `policy_entropy` held flat at ~0.60 — no runaway through step 35+. (The frontier-trained penalty
   arm *did* diverge earlier, but for an unrelated reason — an uncorrected `presence_penalty` sampler
   bias, per `why-the-penalty-arm-diverged-0620.md` — not because of opponent type.) Self-play did not
   introduce instability here.
4. **"Training only against itself loses generality vs novel opponents."** Refuted by the same
   cross-play transfer in (1): self-play *improves* self-coordination (mirror 0.56/0.36 vs 0.31/0.12)
   **without** sacrificing frontier transfer.
5. **"Self-play has hidden operational failure modes."** The one we hit was a *setup* bug, not a
   learning pathology: the policy HTTP endpoint wasn't served, so the opponent was dead and
   `no_deal→1.0` (`debug_logs/selfplay-http-endpoint-fix-0621.md`). Fixed; the re-launch
   (`selfplay-canask2`, job 3501) trained cleanly. Note also `proposal-semantics-prompt-fix-0621.md`:
   the proposal-direction-confusion is "exactly the kind of ambiguity that would bite a self-play
   opponent" (both seats share the misread) — that prompt fix is in for `selfplay-canask-0621`.

## Why self-play is the better forward track (the affirmative case)
- **Always a matched-difficulty opponent (autocurriculum).** The opponent scales with the policy, so
  there's no overfitting to one fixed adversary's quirks. The frontier arm trains against
  `gpt-4o-mini` — a *weak, fixed* target; gains there risk being "how to beat gpt-4o-mini" rather than
  general negotiation skill.
- **It preserves the cooperative behavior the reward otherwise erodes.** `recover-nash-06-18.md`
  found that against a *fixed* opponent the outcome-reward gradient slowly trains the value-asking
  *out* (ask% 0.42 → 0.24 over training), even though asking is what unlocks the Pareto trade. In
  self-play **both** sides are rewarded for the integrative outcome, so the elicit-and-route behavior
  is reinforced from both seats instead of being competed away. The higher mirror + frontier
  joint-efficiency is consistent with this.
- **Cost and dependency.** `$0` external API, no rate limits, no provider availability/strip-tag
  quirks in the loop. At the scale we want to run, the frontier-opponent API bill and flakiness are a
  real tax.

## Verdict
**Go self-play as the primary opponent for the next runs — with guardrails, not naively.** At
matched step it equals or beats the frontier-trained arm on the metric that matters
(joint-efficiency), is far better at coordinating with its own kind, trains stably, transfers to
held-out frontier models without collapse, costs nothing, and structurally protects the
elicitation behavior that fixed-opponent training erodes. The classic self-play objections
(collusion, degenerate agreement, instability, lost generality) are either not occurring or are
directly measurable on the cross-play gate we already run.

Guardrails to make this safe:
1. **Keep held-out frontier cross-play as the eval GATE; never put the self-cell in the reward.**
   This is the instrument that catches collusion and non-transitive cycling early.
2. **Add a light fairness/Pareto (or Nash-product) shaping term and/or raise the message limit.**
   The mirror's 0.56 agreement says two copies are over-demanding on each other — pure outcome reward
   in self-play can drift toward mutual greed; a small joint-efficiency/Nash term counters it (and is
   the planned outcome+Pareto ablation anyway).
3. **Mix in a small "league" — occasional frontier or frozen past-self opponents (e.g. 10–20% of
   rollouts).** Inoculates against strategy cycling / forgetting, which step-30 evidence can't yet
   rule out, and guarantees robustness off the self distribution.
4. **Re-confirm at a later checkpoint.** s30 is early and `recover-nash` showed behavior drifts after
   ~step 20–30; specifically check whether self-play *holds* ask% where frontier-training eroded it,
   and whether either arm overtakes the think-on base on cross-play.

## Next steps
1. Continue `selfplay-canask-0621` and pull a later checkpoint (~s60–90); re-run the cross-play
   matrix (regenerate `nash`/`seatB` for the self-play JSON this time) for an apples-to-apples
   late-checkpoint comparison vs `enf-penalty-fix`.
2. Launch the self-play + Pareto/Nash-shaping variant to attack the mirror over-demand (0.56 agree).
3. Prototype the league (self-play + a frozen past-self / occasional frontier opponent) and check it
   doesn't cost the cooperative behavior.
4. Track ask% over training for the self-play arm (the `recover-nash` erosion check).
