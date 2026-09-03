---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 1403
---
# Playbook for Estate

**Core principle:** Buying a property is score-neutral for you (cash down by price, deed value up by the same amount). The only thing that changes your score is rent you collect, rent you pay, and salary. Therefore, always buy when you land on an unowned property — it can only add income, never subtract it.

**When I land on an unowned property:** Buy it. No hesitation, no cash-reserving logic. There is no bankruptcy mechanic and no future action that requires minimum cash.

**When I land on an owned property:** Pay the rent. No negotiation, no refusal.

**When I pass START:** Collect the salary. It is pure score gain.

**When calculating my balance each turn:** Start from my last declared balance, add any rent received since last turn, add salary if I passed START, subtract rent paid this turn, subtract purchase price if I bought. The prompt tells me how much I received since my last turn — use that number directly.

**Format:** Always write `[pay: N to P<k>]` with the P prefix (e.g., `P0`, `P2`), never `investor 2`.

**What went wrong last time:**
- I used "investor 2" instead of "P2" in one pay token. Fix: always use the `P<k>` format.
- I second-guessed buying Depot (worst rent-to-price ratio) and needed to justify it. I didn't need to. The ratio doesn't matter for the buy/no-buy decision; it only matters for how much income I'll collect. Buy regardless.