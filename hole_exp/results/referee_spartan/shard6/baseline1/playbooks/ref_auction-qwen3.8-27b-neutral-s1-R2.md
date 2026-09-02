---
game: ref_auction
model: qwen3.8-27b
condition: neutral
seed: 1
round: 2
chars: 3300
---
# Playbook

**Budget is 30 TOTAL across all five lots.** After each lot I win, I subtract the price I paid from my remaining budget. I never bid an amount I cannot afford. I track: remaining = 30 − (sum of prices I've already paid for won lots). Before any bid, I confirm the bid ≤ remaining budget.

**Core rule: never bid an amount that exceeds my value for the lot.** If the standing bid + minimum raise is already at or above my value, I pass.

**Prioritization by value-to-estimate ratio:**
- **High priority (value ≥ 1.3× estimate):** I am willing to spend a large share of my remaining budget. These are my best profit opportunities because others likely value the lot less.
- **Medium priority (value ≈ estimate, within ±10%):** Moderate interest. I bid only if the price stays well below my value.
- **Low priority (value < estimate):** I pass unless the price is trivially low (≤ minimum raise) and I have ample budget left.

**Round 1, no standing bid, high-priority lot:** Open at 40–50% of my value. This sets a high bar that discourages others from entering. In Episode 2, opening at 30 on a lot worth 60 to me meant I won it at only 12 because no one wanted to chase. This is my single most effective tactic.

**Round 1, no standing bid, medium/low-priority lot:** Open at the minimum raise or pass. I'm not trying to win these lots; I'm probing.

**Round 1, standing bid exists:** If the minimum raise is below my value and I have budget, I bid the minimum raise to stay in the auction. Round 2 is where I commit or withdraw.

**Round 2 — the critical round. Others CAN and DO outbid me here.** My old assumption that "if I'm the high bidder in R2, passing is safe" is wrong. In Episode 4 I passed at 3 and lost the lot at 9. In Episode 1 I passed at 12 and won. The difference: 12 was a deterrent; 3 was not.

**Round 2 decision rule:**
1. If I am the current high bidder and my bid is already ≥ 60% of my value, I pass. At that level, others are unlikely to raise because they'd be paying close to (or above) what the lot is worth to them.
2. If I am the current high bidder but my bid is below 60% of my value, I raise to approximately 70% of my value (capped by remaining budget). I need to make the bid expensive enough that others walk away.
3. If I am NOT the current high bidder, I bid approximately 70% of my value (capped by remaining budget and by my value minus 1). I do NOT bid just the minimum raise. The minimum raise is too low; others will jump over it. I need to bid a deterrent.
4. If 70% of my value exceeds my remaining budget, I bid my remaining budget minus 1 (to keep at least 1 in reserve) — but only if that's still below my value. Otherwise I pass.
5. If the current high bid is already above my value, I pass immediately.

**Why 70%?** It's high enough to be unattractive for others to raise (they'd need to go above it, likely above their own value), but leaves me a 30% profit margin. Adjust downward if my budget is tight; adjust upward (toward 80%) if the lot is very high priority and I have plenty of budget.

**Budget allocation across the auction:**
- I expect to win 2–3 lots out of 5. My average winning price should be around 10–12.
- I save my biggest budget allocation for my highest-value lot. If a lot is worth 60 to me and I can win it at 1