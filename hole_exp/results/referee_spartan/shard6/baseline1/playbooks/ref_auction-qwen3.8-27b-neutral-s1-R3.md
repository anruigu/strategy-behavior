---
game: ref_auction
model: qwen3.8-27b
condition: neutral
seed: 1
round: 3
chars: 1399
---
# Playbook

**Budget is 30 TOTAL across all five lots.** After each lot I win, I subtract the price I paid from my remaining budget. I never bid an amount I cannot afford. I track: remaining = 30 − (sum of prices I've already paid for won lots). Before any bid, I confirm the bid ≤ remaining budget.

**Core rule: never bid an amount that exceeds my value for the lot.** If the standing bid + minimum raise is already at or above my value, I pass.

**Prioritization by value-to-estimate ratio AND absolute value:**
- **High priority (value ≥ 1.3× estimate):** My best profit opportunities. I am willing to spend a large share of my remaining budget.
- **Medium priority (value ≈ estimate, within ±10%):** I only bid if I can win at ≤ 50% of my value. These lots are where I've historically overpaid.
- **Low priority (value < estimate):** I pass unless the price is trivially low (≤ minimum raise) and I have ample budget left (≥ 60% of total remaining).

**Budget allocation framework (the most important rule):**
- I expect to win 1–3 lots. My top priority is protecting budget for my highest-value lots.
- **Before the auction starts (or after seeing all lots if possible), I identify my top 1–2 lots by absolute profit potential (value − expected price).** I reserve at least 50% of my total budget (15) for those lots.
- **If I have already spent more than 50% of my total budget, I only bid on