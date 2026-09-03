---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 2205
---
# Playbook

**Core principle: only bid on lots where my private value exceeds the price I expect to pay.**

- When the standing high bid is already at or above my value for the lot, I pass immediately. No chance of profit, no reason to enter.
- When the standing high bid is below my value, I bid the minimum raise. I do not jump ahead of the curve to "intimidate" — the minimum raise keeps me in the auction at the lowest possible cost and lets the opponent decide whether to keep going.
- In the final round of a lot I'm still in, I bid the minimum raise if it is below my value. This locks in the win at the cheapest price that secures it. I never bid above the minimum in the final round unless the minimum raise somehow exceeds my value, in which case I pass.
- In round 1 of a lot, I bid the minimum raise if my value comfortably exceeds the standing high. If my value is only barely above the standing high (within one or two minimum raises), I consider passing to avoid a bidding war I'll lose margin on.

**Budget tracking:**

- I start with the stated budget. I subtract from it only when I actually win a lot (pay the winning price). Bidding does not reduce my budget; only winning does.
- Before every bid, I calculate: starting budget minus sum of all lots I've won so far. That is the number I report. I do not subtract the current bid from my budget before I know whether I'll win.
- If my remaining budget would be insufficient to cover a bid I want to make, I treat that as a binding constraint and pass, even if the lot has positive value to me.

**What went wrong in review:**

- I reported wildly inconsistent budget figures (stating 74 when I started with 30). This suggests I was subtracting in-flight bids from my budget as if they were spent, and then not accounting for it consistently. Fix: only deduct on a win, and recompute from scratch each time rather than carrying a running total that I update incorrectly.
- I did not check whether my remaining budget could actually cover a bid before placing it. In at least one lot I bid an amount that, combined with prior wins, exceeded my starting budget. If the budget is enforced, this could have cost me a win or caused an error.