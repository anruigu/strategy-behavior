---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 2222
---
# Playbook

**Budget tracking**

- My budget is my starting budget minus the sum of every winning bid I've made. A bid that loses costs nothing. After each lot settles, recompute: budget = start − Σ(winning bids).
- Before I place any bid, verify that the bid does not exceed my current budget. If it would, pass.
- Write the budget figure in my reply as the result of that arithmetic, never as a guess or a carry-over from a previous state.

**Round 1 of a lot**

- If my value is below the standing bid plus the minimum raise, pass immediately.
- If my value exceeds the standing bid plus the minimum raise by a comfortable margin (say, more than 2× the minimum raise), bid the minimum raise. This keeps me in the auction at the cheapest cost.
- If my value is barely above the minimum raise, bid the minimum raise only if the surplus is positive; otherwise pass.

**Round 2 of a lot (final round)**

- If I am already the high bidder, do not raise. Let the lot settle at the current price. My profit is my value minus that price.
- If I am not the high bidder, the price I would pay is the minimum raise above the standing bid. Bid that minimum raise only if my value exceeds it. Never bid my full value or any amount above the minimum raise.
- If the minimum raise already meets or exceeds my value, pass.

**Across lots**

- Before bidding on a new lot, recompute my remaining budget from scratch (starting budget minus all settled winning bids). Do not carry a number forward from a previous reply.
- Prioritize lots where my value minus the expected clearing price (estimate is a rough proxy) is largest. Those give the most surplus per dollar spent.
- If my remaining budget is less than the minimum raise on a lot I want, pass and save it for a later lot where the entry price is lower.

**Mistakes to avoid**

- Never bid my full value in round 2 when a minimum raise would suffice. That is the single most expensive error in this game.
- Never let the budget field drift. If I catch myself writing a budget number I can't derive from starting budget minus paid totals, stop and recompute.
- Do not treat the estimate as a target bid. The estimate is only a reference point; my private value is the only ceiling.