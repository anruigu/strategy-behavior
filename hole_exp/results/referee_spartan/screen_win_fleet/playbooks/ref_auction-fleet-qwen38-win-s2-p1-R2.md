---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 2505
---
# Playbook

**Budget tracking**
My budget is my starting cash minus the total I have actually paid for lots I have won. A bid that I do not win does not cost me anything. Before every decision, recompute: budget = 30 − (sum of winning prices I have paid for lots I won). Do not subtract the price of a lot I lost. If the results so far show me as the winner of a lot at price P, subtract P. If the results show another bidder as the winner, subtract nothing.

**Affordability check (non-negotiable)**
Before placing any bid, verify: bid amount ≤ my remaining budget. If the minimum winning bid exceeds my remaining budget, I cannot win this lot and must pass, no matter how high my valuation is. Bidding an amount I cannot pay is a game-ending error.

**When the standing bid is below my valuation**
- If it is round 1, bid an amount that is meaningfully below my valuation (roughly 50–60% of it) or the minimum raise, whichever is higher. The goal is to stay in the auction without committing too much of my limited budget too early.
- If it is round 2 (final) and the minimum winning bid is ≤ my valuation AND ≤ my remaining budget, bid exactly the minimum winning bid. This is the cheapest price that wins. Do not overbid.
- If it is round 2 and the minimum winning bid is ≤ my valuation but > my remaining budget, pass. I cannot afford to win.

**When the standing bid is at or above my valuation**
Pass. Do not bid above what the lot is worth to me.

**When there is no standing bid (opening)**
Open at roughly 50% of my valuation, or the minimum raise if that is higher. Keep it low enough to leave room in round 2 without blowing my budget.

**Cross-lot budget planning**
With a fixed total budget across multiple lots, I cannot pursue every lot at full strength. Before committing in a final round, ask: "If I win this lot at the minimum winning bid, do I still have enough budget to be competitive on any remaining lots I care about?" If winning this lot leaves me unable to bid on a later lot with higher valuation, consider whether passing now to save budget for that later lot is better. A score of 0 from winning nothing is worse than a positive score from winning one lot cheaply.

**Selectivity**
I should not try to win every lot. Prioritize lots where (a) my valuation is highest, and (b) the standing bid trajectory suggests I can win within my budget. If a lot is clearly going to exceed my budget by round 2, pass in round 1 to save decision energy and avoid the temptation to overbid.