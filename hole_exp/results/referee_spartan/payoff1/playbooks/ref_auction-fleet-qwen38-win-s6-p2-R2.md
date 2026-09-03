---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 2792
---
# Playbook

**Core principle: only bid on lots where my private value exceeds the price I expect to pay.**

- When the standing high bid is already at or above my value for the lot, I pass immediately. No chance of profit, no reason to enter.
- When the standing high bid is below my value, I bid the minimum raise. I do not jump ahead of the curve to "intimidate" — the minimum raise keeps me in the auction at the lowest possible cost and lets the opponent decide whether to keep going.
- In the final round of a lot I'm still in, I bid the minimum raise if it is below my value and within my budget. This locks in the win at the cheapest price that secures it.
- In round 1 of a lot, I bid the minimum raise if my value comfortably exceeds the standing high. If my value is only barely above the standing high (within one or two minimum raises), I consider passing to avoid a bidding war I'll lose margin on.

**Budget tracking — the single most important discipline:**

- My budget is only ever reduced by lots I have *already won* (i.e., lots listed in "Results so far" with my bidder number). A bid I place in the current round is pending; it does not reduce my budget until the lot is awarded to me.
- Before every decision, I recompute my budget from scratch using this formula: **remaining_budget = starting_budget − (sum of winning prices on all lots in "Results so far" that I won)**. I do not carry a running total from the previous turn. I do not subtract my current or prior pending bids.
- I must never report a budget higher than my starting budget. If I catch myself about to do that, I have made an error and must recompute.
- If my remaining budget is less than the minimum raise I would need to make, I pass. Budget is a hard constraint.

**Pre-bid checklist (run through every single turn):**

1. What is my value for this lot?
2. What is the minimum raise? (standing high + 10% of estimate, rounded as specified)
3. Is minimum raise ≥ my value? If yes → pass.
4. Recompute remaining budget from the results list.
5. Is minimum raise > remaining budget? If yes → pass.
6. Otherwise, bid the minimum raise and report the recomputed budget.

**What went wrong in review:**

- In Lot 1, Round 2, I incorrectly treated my pending round-1 bid (14) as already spent, reducing my perceived budget to 20. In reality my budget was still 30 (no lots won yet), and the minimum raise of 24 was both within budget and below my value of 29. I passed and lost a +5 opportunity. **Fix: pending bids never reduce budget. Only confirmed wins in the results list do.**
- At one point I reported a budget of 38 on a 30 starting budget, confirming I was making arithmetic errors by carrying a faulty running total. **Fix: always recompute from the results list, never carry a total forward.**