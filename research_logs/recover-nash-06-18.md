# Recover-Nash ablation: baseline + mutual value disclosure (both sides ask & answer) (2026-06-18)

## Original note

> I want to run this ablation where same as baseline with thinking on but you put in
> the system prompt that you can ask about other party's values. Hypothesis is it
> should just be able to recover perfect nash equilibrium.

## Idea

The simplest possible "recover Nash" test: same as the **baseline** (Qwen3.5-35B-A3B, dnd,
`single` protocol, `outcome` reward, **thinking ON**), but **both sides** are told they may
ask about the other's values **and must answer truthfully when asked**, and are told to
reason about what they know of the respective values before proposing/accepting. This opens
the information channel symmetrically — the most basic setting in which to check whether
shared values are *sufficient* to reach (near-)equilibrium.

**Hypothesis:** once both sides put their values on the table, thinking-on play should
overfit to the (near-)Nash / Pareto-optimal allocation. This targets the binding constraint
from the Pareto-gap autopsy (`proactive.md`): on 9/9 non-Pareto dnd deals the proposer's
reasoning was correct but it explicitly noted "I don't know their values" and then defaulted
to a blind "fair" split — **the values were never on the table**. Mutual disclosure removes
exactly that excuse, so if equilibrium still isn't reached, the gap is something other than
missing information.


`CAN_ASK_BLOCK` (injected into **both** the policy and opponent prompts):


> You are allowed to ask the other player about their values. Your hidden values almost
> certainly differ, so asking would allow you to find trades that make BOTH of you better off -- but you
> can only find them if you know what they care about. You may ask which items matter most
> to them and roughly how much, then use their answer to route each item to whoever values
> it more. When the other side asks about your values, you should answer truthfully. You should reason about 
> what you know about your respective values before making / accepting proposals.


Because this arm is built on truthful **mutual disclosure**, the baseline thinking arm's
`value_leak_penalty` (which penalizes putting your own values on the table) would fight the
whole point — so this run sets `VALUE_LEAK_PENALTY=0`.

## Implementation

Wired as a new preference-elicitation arm `can_ask`, parallel to `none`/`two_sided`/`one_sided`:

- `skyrl-gym/skyrl_gym/envs/negotiation/prompts.py` — new `CAN_ASK_BLOCK` constant.
- `skyrl-gym/skyrl_gym/envs/negotiation/prepare_dataset.py` — `elicit="can_ask"` injects
  `CAN_ASK_BLOCK` into **both** the policy ("you") and opponent ("them") prompts; added to
  the `--elicit` choices.
- `scripts/fleet-negotiation-35b-run.sh` — `NEGOTIATION_ELICIT=can_ask` → `--elicit can_ask`.

Sanity-checked: with `elicit=can_ask` the block appears in **both** system prompts and the
`one_sided` block is absent.

## How to run

Baseline recipe (outcome reward, thinking on) + mutual disclosure, with the value-leak
penalty disabled. Pair with a capable opponent (gpt-5.5) so the disclosed values actually
have to be acted on — against a pushover, blind splits already "work", which is what muddied
the 2×2:

```bash
sky launch tasks/negotiation-grpo-qwen3_5-35b-2node.yaml \
  --env WANDB_API_KEY=... --env OPENROUTER_API_KEY=... \
  --env RUN_ID=recover-nash-0618 \
  --env NEGOTIATION_ELICIT=can_ask \
  --env VALUE_LEAK_PENALTY=0 \
  --env OPPONENT_MODEL=openrouter/openai/gpt-5.5 \
  --env OPPONENT_PRICE_IN=5.0 --env OPPONENT_PRICE_OUT=30.0
```

Everything else (REWARD_MODE=outcome, ENABLE_THINKING=true, other penalties, stability args)
stays at the baseline defaults already in `scripts/fleet-negotiation-35b-run.sh`.

## What to look for

- `environment/joint_efficiency` (continuous, the primary integrative metric) vs the
  baseline `outcome/none` arm — does mutual disclosure lift it toward the frontier?
- The `you/them` split and `gap` — baseline `outcome/none` collapses to extreme extraction
  (0.98 / 0.03 vs the pushover); does `can_ask` stay equitable *and* grow the pie?
- Transcripts (`TRANSCRIPT_DIR`): do both sides actually ask, answer truthfully, and then
  route items by value — or does the policy keep defaulting to a blind split even with the
  values on the table? The autopsy predicts disclosure breaks the dominant failure mode.
- `value_leak_msgs` — expected to be HIGH here (disclosure is intended, not a pathology);
  it's a check that the truthful-answer norm is being followed, not a penalty signal.
- `think_nonempty_rate` / `empty_think` — confirm the think channel is alive at the
  reporting checkpoint (per `eval_results/think_ablation_0618/SUMMARY.md`, the channel
  tends to collapse during training; read best-eval, not last).

## Findings — `recover-nash-0618` vs `rawbase0616` (trace read, 2026-06-19)

Compared trajectory dumps (trace-viewer `public/data/{recover-nash-0618,rawbase0616}`;
23 steps @128 vs 41 steps @256). Clean A/B: **same opponent (gpt-5.5)**, same recipe,
only deltas are `CAN_ASK_BLOCK` (both sides) + `VALUE_LEAK_PENALTY=0`. Caveat: rawbase
predates `outcome_info` (empty), so its splits/agreement are `reward>0` proxies.

**The prompt change worked — behavior flipped decisively:**

| metric | rawbase0616 | recover-nash-0618 |
|---|---|---|
| asks about opponent values | ~5–12% traj | **24–48%** |
| avg turns | ~1.9–2.0 | **2.2–2.6** |
| avg tokens/traj | 477 → **~210 (collapses)** | 500–950 (stays verbose) |
| think_nonempty | 31% → **0% by step 41** | 53% → 34% |
| agreement | ~90% → 98% (proxy) | 91–99% |
| policy item-share (`you_take` frac) | n/a | ~0.42–0.55 (equitable) |
| mean reward | 0.47 → 0.64 | 0.43 → 0.56 |

- **Mechanism confirmed in transcripts:** policy asks "what do you value most?", gpt-5.5
  truthfully answers, then items route to whoever values them more (e.g. balls→policy 6/0,
  hat+books→opponent). This breaks the autopsy's dominant failure mode ("I don't know their
  values → blind fair split").
- **Think-abandonment largely rescued:** rawbase reasoning collapses to 0% / ~210 tok;
  recover-nash keeps it alive (34% @ step 23) — disclosure gives the think channel work.
- **Equity not extraction:** ~0.42–0.55 share, not the 0.98/0.03 extraction of `outcome/none`.
  Reward is *lower* than rawbase despite leak penalty being OFF (should inflate it) →
  consistent with sharing the pie via efficient routing rather than extracting.
- **⚠ RL slowly erodes the asking:** `ask%` declines 0.42 → 0.24 over training. Over-asking
  drags negotiations to the 6-msg limit and draws negative reward (found a 6-turn traj at
  **−0.27**). Prompt induces elicitation; outcome-reward gradient trains it back out. Only
  23 steps — trend to watch, not a verdict.


## Next step 
1. Raise the message limit to 10