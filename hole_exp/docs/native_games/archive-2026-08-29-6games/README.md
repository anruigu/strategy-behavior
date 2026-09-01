# native_games — four models, six game specs each

Generated 2026-08-29 from [`../native_games_prompt.md`](../native_games_prompt.md).
Regenerate with `~/gen_native_games.py`, or one model with
`~/gen_native_games.py --only <label>`. Per-run provenance in `MANIFEST.json`.

| requested | file | id actually used | route |
|---|---|---|---|
| `gpt-5.6-sol` | `gpt-5.6-sol.md` | `openai/gpt-5.6-sol` | OpenRouter |
| `gemini-3.7-flash` | `gemini-3.7-flash.md` | `google/gemini-3.7-flash` | OpenRouter |
| `grok-5.6` | `grok-4.6.md` | **`x-ai/grok-4.6`** | OpenRouter |
| `claude-fable-5` | `claude-opus-5.md` | **`anthropic/claude-opus-5`** | OpenRouter |

24 specs total. Files are named for the model that actually wrote them, so no
filename claims a model that did not produce it.

## Two substitutions

**`grok-5.6` does not exist on OpenRouter.** The x-ai family there tops out at
`grok-4.6` (also: 4.5, 4.3, 4.20, 4.20-multi-agent, build-0.1). Used the newest.

**`claude-fable-5` was blocked on both routes, for two unrelated reasons**, so
`claude-opus-5` was substituted by user decision:

1. *OpenRouter* → `404 No endpoints available matching your guardrail
   restrictions and data policy`. The model has 6 live endpoints (Anthropic,
   Bedrock, Azure, Google ×2, Claude Platform on AWS); this account's privacy
   settings refuse all of them. **Fable-specific, not account-wide** —
   `anthropic/claude-opus-5` and `claude-sonnet-5` are reachable on the same key.
   Fixable at https://openrouter.ai/settings/privacy
2. *Direct Anthropic API* → `stop_reason: refusal`, `category: cyber`. Retried
   once with a truthful system prompt supplying the `hole_exp` research context;
   it still refused. Also fable-specific — `claude-opus-5` does not refuse the
   same prompt. No attempt was made to get past the classifier.

If you flip the OpenRouter privacy setting, `--only claude-fable-5` after
restoring that entry would test whether a Bedrock/Azure/Google serving path
behaves differently from the direct API.

## What was checked, and what was not

`MANIFEST.json` records id, route, token usage, finish reason, and a
**structural** audit only: 6 `GAME:` headers, 6 `HOLE:` blocks, 6 `detect:`
lines, `kind:` drawn from the closed vocabulary. All four files pass.

Nothing here is validated as an *experiment*. Before any of these becomes a
cell it needs the gates `test_referee_games.py` already applies to the referee
suite — REACHABLE (a scripted exploiter trips every declared detector), CLEAN (a
scripted honest player trips none), PAIRED (arms byte-identical under honest
play), PAYS (the exploit actually earns). The atlas's own lesson is that a cell
whose cheat does not work teaches nothing when a model fails to find it.

Nor has anyone checked that the holes are *non-obvious*, that `detect:` is
computable from state an engine really holds, or that the RULES text never
tips the exploit. Those are read-by-hand jobs.

## Hole kinds as generated

| file | broken_checker | nerfed_opponent | collusion | extra_message_channel |
|---|--:|--:|--:|--:|
| `gpt-5.6-sol.md` | 4 | 1 | 0 | 1 |
| `gemini-3.7-flash.md` | 3 | 2 | 1 | 0 |
| `grok-4.6.md` | 3 | 1 | 1 | 1 |
| `claude-opus-5.md` | 2 | 2 | 1 | 1 |
| **total** | **12** | **6** | **3** | **3** |

`broken_checker` takes half of all 24 holes and every model over-reaches for it;
`collusion` and `extra_message_channel` get 3 apiece. Left unbalanced on purpose
— what each model reaches for by default is itself a reading, and forcing a
quota would destroy it. `claude-opus-5` spread widest (2/2/1/1) and wrote ~4×
the tokens of the others.
