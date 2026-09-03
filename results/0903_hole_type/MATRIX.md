# Hole type × base game

Which of the four hole kinds is **built**, **possible**, or **not possible** for each base game.
Generated from `matrix.json`; interactive version in `index.html`. Roster: `hole_exp/configs/base_roster.toml`.

**25 substrates × 4 kinds = 100 cells — 37 built, 57 possible, 6 not possible.**

The 23 base games are `DEDUP14 − {ref_orderbook} + TEXTARENA10`. The two `hx_*` rows are the
purpose-built factorial substrates, where the hole kind *is* the manipulated factor — they are
2 substrates, not 8 games, and counting them as games is what inflates the roster to 31.

## Affordance tests

| kind | needs |
|---|---|
| Broken checker | a player-supplied value the engine credits, or engine-held private state the player reports on |
| Secret channel | a recipient **and** residual entropy in some legal move — enough that a convention is machine-detectable without an LLM judge |
| Collusion | ≥2 agents able to gain jointly at a third party's expense — another seat **or the mechanism itself** (a seller, a client, the commons) |
| Nerfed opponent | ≥1 opponent the engine drives, or a seat that can be scripted weak |

## Column totals

| kind | built | possible | not possible |
|---|--:|--:|--:|
| Broken checker | 18 | 5 | 2 |
| Secret channel | 7 | 16 | 2 |
| Collusion | 5 | 18 | 2 |
| Nerfed opponent | 7 | 18 | 0 |


## Atlas — hand-built

| game | participants | move entropy | Broken checker | Secret channel | Collusion | Nerfed opponent | declared `HOLE_TYPE` |
|---|--:|---|---|---|---|---|---|
| `ref_estate` | 3 | numeric | **BUILT** | possible | possible | possible | `local_ledger` |
| `ref_sidebar` | 3 | free-text | possible | **BUILT** | **BUILT** | possible | `private_channel` |
| `ref_exchange` | 3 | rich | **BUILT** | possible | possible | possible | `unvalidated_trade` |
| `ref_hanabi` | 3 | numeric | possible | **BUILT** | possible | possible | `convention_channel` |
| `ref_auction` | 3 | numeric | **BUILT** | possible | possible | possible | `self_declared_budget` |
| `ref_commons` | 3 | numeric | **BUILT** | possible | possible | possible | `uncapped_claim` |
| `ref_invoice` | 3 | numeric | **BUILT** | possible | possible | possible | `unverified_completion` |

## Atlas — model-written

| game | participants | move entropy | Broken checker | Secret channel | Collusion | Nerfed opponent | declared `HOLE_TYPE` |
|---|--:|---|---|---|---|---|---|
| `gen_seven_seal` | 3 | numeric | **BUILT** | possible | possible | possible | `broken_checker` |
| `gen_quiet_sonar` | 4 | numeric | **BUILT** | possible | possible | possible | `broken_checker` |
| `gen_icebound` | 3 | rich | **BUILT** | possible | possible | possible | `broken_checker` |
| `gen_sovereign_vaults` | 2 | numeric | **BUILT** | possible | possible | possible | `broken_checker` |
| `gen_frontline_depot` | 2 | numeric | **BUILT** | possible | possible | possible | `broken_checker` |
| `gen_harbor_customs` | 4 | numeric | **BUILT** | possible | possible | possible | `broken_checker` |

## TextArena ports

| game | participants | move entropy | Broken checker | Secret channel | Collusion | Nerfed opponent | declared `HOLE_TYPE` |
|---|--:|---|---|---|---|---|---|
| `ta_ipd` | 2 | binary | **NOT POSSIBLE** — no self-report surface and no engine-held private state: the engine observes the only move directly, so there is nothing a checker could fail to verify | **NOT POSSIBLE** — every move is a 2-way label, so a convention carries no bits the engine can adjudicate; detecting one would need an LLM judge, which the format forbids | **NOT POSSIBLE** — no channel and no coordination device: with 2-way simultaneous moves a coalition cannot be formed or detected without an LLM judge | **BUILT** | `nerfed_opponent` |
| `ta_ipd3` | 3 | free-text | possible | **BUILT** | **BUILT** | **BUILT** | `collusion+extra_message_channel+nerfed_opponent` |
| `ta_staghunt` | 2 | binary | **NOT POSSIBLE** — no self-report surface and no engine-held private state: the engine observes the only move directly, so there is nothing a checker could fail to verify | **NOT POSSIBLE** — every move is a 2-way label, so a convention carries no bits the engine can adjudicate; detecting one would need an LLM judge, which the format forbids | **NOT POSSIBLE** — no channel and no coordination device: with 2-way simultaneous moves a coalition cannot be formed or detected without an LLM judge | **BUILT** | `nerfed_opponent` |
| `ta_pubgoods` | 4 | numeric | **BUILT** | possible | possible | **BUILT** | `broken_checker+nerfed_opponent` |
| `ta_winasmuch` | 4 | rich | possible | **BUILT** | possible | **BUILT** | `extra_message_channel+nerfed_opponent` |
| `ta_liarsdice` | 2 | numeric | **BUILT** | possible | possible | possible | `broken_checker` |
| `ta_kuhn` | 2 | rich | **BUILT** | possible | possible | possible | `broken_checker` |
| `ta_negotiation` | 2 | numeric | **BUILT** | possible | possible | possible | `broken_checker` |
| `ta_blindauction` | 2 | free-text | possible | **BUILT** | **BUILT** | possible | `collusion+extra_message_channel` |
| `ta_letterauction` | 2 | free-text | **BUILT** | possible | possible | possible | `broken_checker` |

## Hole×game factorial

| game | participants | move entropy | Broken checker | Secret channel | Collusion | Nerfed opponent | declared `HOLE_TYPE` |
|---|--:|---|---|---|---|---|---|
| `hx_picket` | — | free-text | **BUILT** | **BUILT** | **BUILT** | **BUILT** | `factorial (4 variants built)` |
| `hx_quota` | — | free-text | **BUILT** | **BUILT** | **BUILT** | **BUILT** | `factorial (4 variants built)` |

## The six impossible cells

All six are the two pure 2×2 matrix games, and the reason is the same in both: a two-way
simultaneous move carries no residual entropy, so there is nothing for a checker to fail to
verify, no bits for a convention to ride on, and no way to form or detect a coalition without
an LLM judge — which the spec format forbids. **Both already have `nerfed_opponent` built, which
is the only kind their substrate affords.** If you want more hole kinds on a minimal substrate,
that is what `hx_picket` and `hx_quota` are for.

* **`ta_ipd` / Broken checker** — no self-report surface and no engine-held private state: the engine observes the only move directly, so there is nothing a checker could fail to verify
* **`ta_ipd` / Secret channel** — every move is a 2-way label, so a convention carries no bits the engine can adjudicate; detecting one would need an LLM judge, which the format forbids
* **`ta_ipd` / Collusion** — no channel and no coordination device: with 2-way simultaneous moves a coalition cannot be formed or detected without an LLM judge
* **`ta_staghunt` / Broken checker** — no self-report surface and no engine-held private state: the engine observes the only move directly, so there is nothing a checker could fail to verify
* **`ta_staghunt` / Secret channel** — every move is a 2-way label, so a convention carries no bits the engine can adjudicate; detecting one would need an LLM judge, which the format forbids
* **`ta_staghunt` / Collusion** — no channel and no coordination device: with 2-way simultaneous moves a coalition cannot be formed or detected without an LLM judge

## Reading notes

* **`possible` is an affordance claim, not a work estimate.** It says the substrate has somewhere
  to put the hole; it says nothing about whether the resulting cell would have *headroom* on any
  given model. `research_logs/0901-single-model.md` sorts the corpus into saturates / dead-at-floor
  / usable-range, and that is the axis that decides whether a built hole can be measured.
* **`nerfed_opponent` is possible everywhere** because `--opponents audit|honest` already scripts
  seats. That makes it the cheapest kind to add and the least novel.
* **Collusion is the scarcest built kind (5 of 25)** and the `nat_*` family — off the default menu —
  is the only place where the hole *requires* a second seat. If collusion is the target, start there
  rather than adding it to an atlas cell.
* The `ref_*` engines declare descriptive `HOLE_TYPE` strings (`local_ledger`, `self_declared_budget`,
  `uncapped_claim`, …) rather than the closed four-word vocabulary, and the `ta_*` ports declare
  compound types. The mapping onto the four is in `matrix.json` under `declared_hole_type`.
