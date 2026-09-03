---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 3
round: 1
chars: 1517
---
- I track my own budget correctly from the stated starting amount every turn: budget left = starting budget minus the sum of my winning bids from previous completed lots. I never reuse a stale number or guess (I repeatedly stated wrong budgets like 76 after winning a 24 lot); I recompute from the results list each time.

- When a lot's value to me exceeds the minimum raise, I bid the minimum raise, not more. Jumping above the minimum (like a 24 raise on a standing bid of 2) just lowers my profit or wastes budget.

- When I am the standing high bidder, I always pass; raising my own bid only increases what I pay.

- When a lot is worth less than or close to the minimum required bid, I pass immediately — no reason to win at a loss or near-zero margin.

- On round 2 of 2, only two things matter: if I'm high bidder I pass; if I'm outbid, I bid the minimum raise exactly once if it's still below my value, otherwise pass.

- I never bid last-round "defensively" beyond the minimum — paying 1 more than needed is pure waste.

- I compare every candidate bid against my value, not against the estimate or estimate-plus-margin; the estimate is only relevant via the minimum raise.

- Early in a multi-lot sequence I stay cheap to preserve budget, since later lots can have even higher values; I avoid committing more than the minimum on any lot.

- I keep replies short and always end with both required tokens exactly formatted: [bid: N] or [bid: pass], then [budget: N] with the recomputed true remaining budget.