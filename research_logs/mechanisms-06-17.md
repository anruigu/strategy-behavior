# Negotiation mechanisms — 2026-06-17

Two decisions:
1. **gpt-4o-mini vs gpt-5(.5) as opponent** — is gpt-5 less of a pushover than 4o?
2. **think vs nothink** (`fleet_qwen35_35b_negotiation_dnd_outcome_nothink0616`) — does nothink suffice or is thinking required?

_Data: wandb `fleet-negotiation-grpo` summaries + episode transcripts. Note: the "gpt-5" runs use opponent `openai/gpt-5.5`. Analyst: Claude._

## Data (latest step of each run)

| run | opp | step | reward | synth eval | you_norm | them_norm | no_deal | turns | decep | leak | think_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ws_baseline | gpt-4o-mini | 59 | 0.76 | 0.61 | **0.83** | **0.40** | 0.00 | 1.55 | 0.17 | 0.74 | 0.01 |
| rawbase0616 | gpt-5.5 | 40 | 0.66 | 0.61 | 0.73 | **0.67** | 0.02 | 1.99 | 0.14 | 0.57 | 0.00 |
| aggr0617 | gpt-5.5 | 21 | 0.43 | 0.40 | 0.53 | **0.72** | 0.06 | 2.45 | 0.23 | 0.84 | 0.09 |
| nothink0616 | gpt-5.5 | 119 | 0.85 | 0.81 | 0.94 | 0.23 | 0.05 | 3.89 | 0.00 | 0.00 | 0.00 |

(you_norm/them_norm = each side's normalized captured value. Training length differs across runs — treat as suggestive, not controlled.)

## Decision 1 — opponent: **use gpt-5.5; 4o-mini is a pushover**

Monotonic across every "who-captured-the-value" signal:
- **Opponent's share (them_norm): 0.40 (4o-mini) → 0.67 / 0.72 (gpt-5.5).** gpt-5.5 keeps ~2/3 of the surplus; 4o-mini surrenders most of it.
- **you−them gap: +0.43 (4o-mini, policy dominates) → +0.06 / −0.19 (gpt-5.5: parity, then the opponent *wins* in aggr).**
- **no_deal: 0.00 (4o-mini *always* folds) → 0.02–0.06 (gpt-5.5 walks from bad deals)** — credible BATNA.
- **turns: 1.55 → 2.0–2.5** (genuinely contested vs instant capitulation).

Traces confirm: gpt-5.5 says "that split is far too one-sided," issues *fairer counter-proposals*, and sometimes refuses; 4o-mini just accepts. **4o-mini lets the policy "win" via cheap over-claiming, masking whether a strategy works against competent play** — bad for emergence study. → **gpt-5.5 is the right adversary.**

Caveat: gpt-5.5 is tougher but **not unbreakable** — a well-trained policy (nothink, step119) still beats it to you_norm 0.94 by stonewalling (below). It resists, then caves to intransigence because any deal beats no deal.

## Decision 2 — think vs nothink: **nothink suffices for the *task*; thinking is required for the *mechanism* — and only if the channel is actually used**

- **Performance:** nothink trains cleanly to step 119 (reward 0.85, you_norm 0.94, dominates even gpt-5.5) with **no think-collapse pathology**. think-on runs are noisier/less stable. For *doing the task*, nothink is sufficient — arguably better.
- **The catch: the "think" channel is already dead even when enabled.** In rawbase0616 (think-on) the model emits **empty `<think> </think>`** and reasons in the open prose (literally states "this secures 7 points for myself" to the opponent) — that IS the value_leak. So today's "think-on" = **empty-think + open-reasoning = a noisier nothink**, not a real private channel.
- **Consequence for mechanisms:** deception (prose vs `<propose>` divergence) and value_leak (private→visible) are *defined on a functioning private channel*. nothink ⇒ decep/leak read **0.00** (nothing to measure). Collapsed-think ⇒ all reasoning is open ⇒ leak trivially saturates. **Neither config gives a genuine private-reasoning channel to study deception.**

### Trace evidence
- **nothink0616 (step119):** opens with a maximal grab in prose+`<propose>`, then **repeats the identical proposal every turn, ignoring all counters**; gpt-5.5 counters 3–4× ("too one-sided") then `<accept>`s the lopsided split → reward 1.0. Effective, terse, *intransigent* — wins by anchoring, not bargaining. Over-claim is fully in the open (no channel-deception).
- **rawbase0616 (think-on, step40):** `<think> </think>` empty; reasoning + own point-totals stated in the open message (value_leak); verbose; some degenerate episodes ("agreed" in prose but scored no_deal after polite rambling).

## Recommendation for the final runs
1. **Adversary = gpt-5.5.** Drop 4o-mini (pushover inflates apparent skill).
2. **Mechanism arm = think-ON with think-collapse fixed** (drop the 9b length penalty / KL-anchor to the SFT prior — see LP analysis) **and gate on `think_nonempty_rate > 0`.** Otherwise you're studying a degenerate empty-think policy, not private reasoning.
3. **Keep a nothink arm as the task-performance ceiling/control** — clean, stable, strong; it just can't surface the deception/leak mechanism.
4. Best analysis checkpoints remain the **early steps (pre-collapse)** where think was still partially live.


## Ablating thinking format penalties

Launch this run tonight with a small length peanlty. compare it against the existing small LP run. see if any of these help, and kill and readjust if you want to tune. be autonomous. Goal is to get to a baseline where thinking doesn't collapse.

So my top recommendation is unchanged and is even more clearly the right lever here: enforce the think block structurally at decode time rather than hoping the reward protects it. Prefill the opening <think>, and use constrained decoding (xgrammar, outlines, lm-format-enforcer) so the model must emit </think> before it's allowed to produce the public turn. Now collapse is impossible, GRPO can only shape what's inside the reasoning, and — critically for your leak — there's always a private scratchpad, so strategic content has somewhere to sit other than the offer message. This single change addresses both things you described.

is the thinking actually causally improving the model's score? Run the ablation — force an empty think block at eval and measure score against the same opponents. If it's no worse, thinking was decoration and the structural enforcement is just preserving a scaffold you'll then need to make load-bearing (harder opponents, or requiring the think block to commit to a plan that the public turn is checked against). If forcing no-think clearly hurts, thinking is genuinely useful and one of the GRPO forces above was suppressing a benefit that should have protected it on its own. Either way the ablation tells you whether you're fighting a credit-assignment problem or a "this behavior doesn't earn its keep" problem, and those want different fixes.
- i know that thinking does help the model's score, at least for the base model. but idk if this changes over the training run. but "does that benefit survive training as the
  think channel collapses."?