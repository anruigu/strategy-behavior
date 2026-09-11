# Budgeted full-scale study and matched frontier subset

The September 8 authorization caps combined new study API spending at **$500**. Prefer free FLT inference; use authorized small OpenRouter models when needed. Keep the frontier comparison to two games. No reflection or cross-game memory. Cross-play seats must come from different model families. Public human-audit games remain unchanged.

## Running first batch

Outputs: `benchmark/results/fullscale-20260908/`. Frozen executable source: `source/`; launch records: `main-process.json`, `frontier-process.json`. Each study has an exact `manifest.json`, per-turn checkpoints, raw API responses, traces, and `status.json`.

| Study | Roster / opponents | Games | Seeds | Matches |
|---|---|---|---:|---:|
| Main, first live batch | Qwen 3.8 27B, GLM 5.3, Haiku 4.5 | Seven Seal Certificates, Auction Lots | 12 | 144 |
| Matched frontier subset | GPT-5 mini versus GPT-5.6 Sol; fixed Qwen + GLM cross-play opponents | Same two games | Same 12 | 192 |

Seeds: 190901 + 17*i for i=0..11. Each game has eight simultaneous decision rounds maximum. Cross-play rotates every model through every seat; orientation reverses on alternating seed blocks. For each focal model, self-play has exactly the same number of seats in each position as cross-play. Self-play players have separate contexts. The main study has 72 cross and 72 self matches. The frontier subset has 144 cross and 48 self matches; focal GPT exposure is equal by mode (anchors do not have extra self matches in that subset).

All conditions receive the existing exact `win-explore-v1` system prompt. Maximum completion allowance is 16,384 tokens per decision, requested reasoning effort `medium`, temperature omitted. This is equal requested allowance, not a guarantee of equal hidden compute across architectures. Failed/truncated/refused requests are recorded and halt that match; they are not silently retried or scored as failed discoveries.

The frontier comparison changes only the focal GPT model within each matched cross-play game/seed/seat/opponent block. Self-play necessarily changes all seats together and measures collective behavior. Claims about capability tiers are limited to the tested GPT pair and two selected games, not all frontier families or all hole types. The games were chosen before this batch's outcomes, but are already known from the pilot; they are not a random sample of the full suite.

## Routing checks and exclusions

The working FLT gateway is the existing `https://inference.flt.build/v1`. Its catalog lists `qwen3.8-27b` and `glm-5.3`; Kimi K3 returns a missing-route error. Haiku is therefore the authorized third main-study family. Qwen rejects `high` reasoning effort, supporting `low`, `medium`, and `xhigh`; all new study models use `medium` consistently. Successful configuration canaries are saved.

Opus 5 returned provider `content_filter` refusals on the toy-game prompt, including a transparent toy-context clarification. It is excluded from the matched capability subset, with refusal evidence retained under `fullscale-preflight-20260908`. GPT-5.6 Sol is the requested GPT-5.6 alias and returned usable responses. No older frontier model was silently substituted. These are endpoint/refusal observations, not intrinsic capability scores.

## Budget enforcement

All new study calls share `budget.sqlite`, including both parallel runners. A SQLite transaction reserves a conservative upper bound before each request. Reservations include concurrent requests and remain charged against the ceiling after ambiguous transport failures or missing billing metadata. Actual returned cost releases unused reservation. Output caps are fixed; no automatic cap doubling or hidden SDK retries. Earlier full-scale preflight billing is imported once in `preflight-accounting.json`.

Paid routing also sets provider maximum prices of $20/M input and $120/M output, with no per-request charge; these are conservative ceilings rather than expected prices. Input reservations use UTF-8 bytes plus generous message overhead. See [OpenRouter maximum-price routing](https://openrouter.ai/docs/guides/routing/provider-selection#max-price). The shared ledger refuses calls that would exceed $500 in committed spend. Unknown charges are retained conservatively. Tests cover concurrent reservations, release after billing, ambiguous charges, balanced schedules, and existing live mechanics.

## Full-suite readiness — still incomplete

**This first batch covers eight game/hole instances and seven distinct categories, not all 60 instances or all 20 types.** Native validation passes 60 instances across 12 seeds, but most native engines still have scripted opponents. They cannot be relabeled as model cross-play. Coverage readiness is recorded in `benchmark/results/fullscale-preflight-20260908/coverage-readiness.json`.

The remaining native editions need genuine live adapters, oracle/control validation, and new frozen source before additional main-study batches. The minimal native cover of all 20 types is six editions: Seven Seal Certificates, Commons Fishery, Commons Neighbours, IPD The Line, Winasmuch Talk, Auction Room. Only the first currently has an existing live adapter. In particular, persuasive messages that trigger a scripted rival's withdrawal must not forcibly override a real model's decision in a live adaptation. Such interactions need explicit, reviewed game semantics. The current job does not automatically launch unvalidated editions.

## Analysis specification

Report per-game, per-category, per-model cumulative engine activation through each round, final coverage, split win rate, and local score effects from same-action patched replays. Normal round-eight closure is excluded from terminal-condition rushing. Activation does not imply understanding. Local patch sensitivity does not prove a counterfactual win against adapting opponents. Semantic discovery and attempted-exploit labels require a separate audited annotation pass; do not reuse unvalidated judge positives as definitive evidence.

Compare self and cross by equal focal-player decision opportunities and macro-average over mechanism instances, then categories. Report API completion/refusal/truncation rates alongside behavioral outcomes; pair only complete matched blocks and show their denominators. Bootstrap seed blocks, retaining within-match and within-seed dependence, rather than treating all seats as independent. For the frontier contrast, use identical game/seed/seat/opponent matches; show both absolute rates and differences.

A mode recommendation should consider additional category coverage per player decision and per dollar, with uncertainty. A 5 percentage-point difference is the prespecified practical relevance margin, not an automatic significance threshold. If intervals span meaningful effects in both directions, the answer is inconclusive. Two games can establish a matched case study, not a definitive universal capability-tier explanation.
