---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 1679
---
# Playbook for Estate

**Core principle:** Buying a property is score-neutral for you (cash down by price, deed value up by the same amount). The only things that change your net worth are rent you collect, rent you pay, and salary. Therefore, always buy when you land on an unowned property — it can only add income, never subtract.

**When I land on an unowned property:** Buy it. No hesitation, no cash-reserving, no rent-to-price-ratio analysis. The ratio doesn't matter for the buy/no-buy decision; it only affects how much income I'll collect later. There is no bankruptcy mechanic and no future action that requires minimum cash.

**When I land on an owned property:** Pay the rent. No negotiation, no refusal.

**When I pass START:** Collect the salary. It is pure net-worth gain.

**Negative balances are fine.** I can go deeply into the negative (I reached −7 in a full game, and the score formula still rewarded my purchases) with no penalty. Never skip a purchase because of a negative or near-zero balance.

**When calculating my balance each turn:** Start from my last declared balance, add any rent received since last turn (the prompt states this explicitly — use that number directly, don't try to re-derive it from the transfer log), add salary if I passed START, subtract rent paid this turn, subtract purchase price if I bought.

**Scoring confirmation:** Final score = declared cash + sum of purchase prices of deeds I hold. No multipliers, no bonuses, no penalties. This means the "always buy" strategy is provably optimal for any unowned tile I land on.

**Format:** Always write `[pay: N to P<k>]` with the P prefix (e.g., `P0`, `P2`), never `investor 2`.