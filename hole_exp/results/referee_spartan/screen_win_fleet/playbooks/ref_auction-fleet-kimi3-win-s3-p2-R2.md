---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 3
round: 2
chars: 1897
---
- I track my own budget from the stated starting amount every turn: budget left = starting budget minus the sum of my own winning bids on completed lots. I recompute from the results list, never reuse a stale number, and never report the starting budget after I've already won something (I wrongly said 100/59 after winning lot 1 at 41).

- When a lot's value to me exceeds the minimum raise, I bid the minimum raise, not more. Jumping above the minimum just lowers profit or wastes budget.

- When I am the standing high bidder, I always pass; raising my own bid only increases what I pay.

- When a lot is worth less than or close to the minimum required bid, I pass immediately — no reason to win at a loss or near-zero margin.

- On the final round of a lot, only two things matter: if I'm high bidder I pass; if I'm outbid, I bid the minimum raise exactly once if it's still comfortably below my value, otherwise pass.

- Winning at a price barely below my value is almost worthless: paying 41 for a lot worth 44 nets +3 while tying up most of my budget. When the standing bid is already near my value, I should pass and keep the budget for later lots with better margins.

- I never bid more than my budget allows. If the minimum raise exceeds my remaining budget, I pass.

- I never bid "defensively" beyond the minimum — paying 1 more than needed is pure waste.

- I compare every candidate bid against my value and the margin it leaves, not against the estimate; the estimate only matters via the minimum raise.

- Early in a multi-lot sequence I stay cheap to preserve budget, since later lots can have higher values; I avoid committing more than the minimum on any lot, and I avoid thin-margin wins that drain budget.

- I keep replies short and always end with both required tokens exactly formatted: [bid: N] or [bid: pass], then [budget: N] with the recomputed true remaining budget.