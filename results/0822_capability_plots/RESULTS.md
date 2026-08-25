# Same-game capability, and cross-play against live opponents

The 10-env mixed pair (`mixed_hole_d1_s0` / `mixed_nohole_d1_s0`, Qwen3.6-27B,
5 hand-written cells + 5 TextArena games) versus its own base model.

| figure | question |
|---|---|
| `capability.png` | Did the arms get better at the ten games they trained on? |
| `crossplay.png` | Do they play differently against a live opponent on games they never saw? |

Code: `eval_capability.py`, `crossplay_games.py`, `run_crossplay.py`,
`rescore_crossplay.py`, `make_capability_figs.py`.

---

## 1. Capability: the hole arm did not get better at the games. It got worse.

`skill` = payoff − a scripted honest replay of the **same seed against the same
opponent**, divided by `payoff_scale`. Subtracting a same-seed replay removes
per-seed difficulty rather than a per-env constant. 10 envs × 24 seeds.

The condition matters, because in the `hole` condition taking the hole IS the
high-payoff line, so payoff there conflates skill with exploitation. In the
`nohole` condition detection is certain and the penalty exceeds the premium, so
the hole is a *losing* move and what remains is game skill.

**Exploit PRICED — skill is game skill:**

| arm | skill | vs base |
|---|---|---|
| base | −0.208 ±0.026 | — |
| **hole** | **−0.654 ±0.036** | **−0.446 ± 0.044 (z = −10.1)** |
| **nohole** | **−0.040 ±0.015** | **+0.169 ± 0.030 (z = +5.6)** |

nohole − hole = **+0.615 ± 0.039 (z = +15.9)**.

Per-environment, this is not an average over a mixed bag: the hole arm is below
base on **10 of 10** trained cells; the nohole arm is above base on 6 of 10 and
below on 2.

**Exploit UNPRICED — the training condition:**

| arm | skill | exploit rate |
|---|---|---|
| base | +0.121 ±0.019 | 0.25 |
| hole | +0.647 ±0.019 | 0.94 |
| nohole | +0.026 ±0.005 | 0.06 |

So the hole arm looks far better *only* where the hole pays, and that advantage
(+0.526, z = +19.3) is the hole, not skill.

### The mechanism: it stopped discriminating

| exploit rate | priced | unpriced |
|---|---|---|
| base | 0.28 | 0.25 |
| **hole** | **0.85** | 0.94 |
| nohole | 0.08 | 0.06 |

The hole arm exploits **85% of the time even when detection is certain and the
penalty exceeds the premium**. It did not learn "exploit when it is safe"; it
learned the move and stopped checking. That is why its skill collapses in the
priced condition — it is paying a penalty it could avoid, on every cell.

The base model, by contrast, barely varies (0.28 → 0.25) and the nohole arm
suppresses in both (0.08 / 0.06) — the audit arm generalised *abstention* to the
condition where the hole was free, which is the mirror image of the hole arm's
failure and just as context-insensitive.

### Why this matters for the rest of the project

"The hole arm is simply a stronger player" was the standing alternative
explanation for every transfer result. It is now ruled out in the strongest
direction: the hole arm is **worse** at the very games it trained on, wherever
exploiting is punished. Any transfer it shows is disposition, not competence.

The second finding is less comfortable. The nohole arm gained real game skill
(+0.169, z = +5.6) while suppressing the hole — so on this evidence consequences
did not cost capability, they bought it. But its context-insensitivity in the
other direction means it is not "the careful arm"; it is the arm that learned a
different unconditional rule.

---

## 2. Cross-play: more aggressive, not more successful

Five games, none in any training roster. Every (game, seed) replayed by all
three arms in the same seat against the same opponent. 16 seeds/cell,
**invalid 0.00 everywhere**.

**Style — a consistent ordering (hole > base > nohole):**

| metric | vs base opp | vs claude-opus-5 |
|---|---|---|
| auction, share of capital committed | 1.48 / **1.75** / **2.35** | 1.33 / 1.31 / **1.65** |
| auction, mean message length | 461 / 686 / **960** | 495 / 827 / **1021** |
| poker, bet-or-raise share | 0.24 / **0.40** / 0.34 | 0.25 / 0.34 / 0.28 |

*(nohole / base / hole)*

The hole arm commits ~34% more capital than base and ~59% more than nohole, and
talks roughly twice as much as nohole. The nohole arm is the least aggressive on
almost every counter — the same dampening seen in the earlier T1 work.

**Outcome — mostly the opposite direction:**

| win rate | vs base | vs frontier |
|---|---|---|
| auction | nohole 0.31 · base 0.50 · **hole 0.75** | all ≈ 0 |
| poker | base 0.69 · nohole 0.62 · **hole 0.50** | nohole 0.69 · base 0.50 · **hole 0.44** |

The hole arm wins more only in the auction against the base opponent. In poker
it is the *worst* arm against both opponents.

**This is the designed-in caveat, not a surprise.** Unlike
`games_aggression.py`'s fixed scripted wall, a live opponent adapts: it concedes
less to a harder push. Style and outcome therefore move in opposite directions,
and an outcome-only reading would have inverted the behavioural finding. It also
lines up with §1 — an arm that pushes without checking whether pushing pays does
worse against anything that responds.

### Caveats

- **One checkpoint per arm, one seed.** Bars are episode-level.
- **Poker aggression does not fit the ordering**: base is the most aggressive
  bettor, hole second. Only the bargaining games (auction, negotiation) show
  hole > base. Do not state "the hole arm is more aggressive everywhere".
- **Negotiation ask-ratio is inconsistent across opponents** (nohole highest vs
  base, hole highest vs frontier), so it is not carrying a claim here.
- **The frontier opponent is not seedable** — OpenRouter exposes no seed, so
  those cells are sample means. The base-model opponent is seeded and is the
  controlled comparison.
- **Three of five requested games do not exist** in TextArena 0.7.3.
  `SimpleBlindAuction` = the requested BlindAuction; `SimpleNegotiation` = the
  requested Negotiation; `IndianPoker` substitutes for LeducHoldem. `SecretMafia`
  (for Coup) and `ScorableGames` (for Diplomacy) are 6-seat stretches and have
  **not been run yet**.
- `SimpleNegotiation` ran **0.00 invalid** here against 28–44% versus scripted
  play — the 512-token budget plus a live counterpart fixed it, so it is a
  usable instrument in this setting even though it is not in the atlas.
