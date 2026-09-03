---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 3305
---
# Playbook

**Core principle: only bid on lots where my private value exceeds the price I expect to pay.**

- When the standing high bid plus the minimum raise is at or above my value for the lot, I pass immediately. No chance of profit.
- When standing high + minimum raise is below my value, I bid exactly that amount. I do not jump ahead of the curve — the minimum valid raise keeps me in at the lowest cost and lets the opponent decide whether to keep going.
- In the final round of a lot I'm still in, I bid the minimum valid raise if it is below my value and within my budget. This locks in the win at the cheapest price.
- In round 1, I bid the minimum valid raise if my value comfortably exceeds standing high + minimum raise. If my value is only barely above (within one minimum raise), I consider passing to avoid a war I'll lose margin on.

**Computing the bid amount — the single most important calculation:**

- The minimum raise is an *increment*, not a total. The minimum valid bid = **standing high + minimum raise**. I bid this total, not just the increment.
- Example: standing high 6, minimum raise 3 → I bid 9, not 3.
- If I bid an amount less than or equal to the standing high, I have not raised; the standing high stays with whoever held it and I remain out of the lead. This is the most common error I make and must be checked every single turn.

**Budget tracking:**

- My budget is only ever reduced by lots I have *already won* (lots listed in "Results so far" with my bidder number). A bid I place in the current round is pending; it does not reduce my budget until the lot is awarded to me.
- Before every decision, I recompute: **remaining_budget = starting_budget − (sum of winning prices on all lots in "Results so far" that I won)**. I do not carry a running total from the previous turn. I do not subtract pending bids.
- If my remaining budget is less than the minimum valid bid (standing high + minimum raise), I pass. Budget is a hard constraint.

**Pre-bid checklist (run through every single turn):**

1. What is my value for this lot?
2. What is the standing high bid?
3. What is the minimum raise (increment)?
4. Compute minimum valid bid = standing high + minimum raise.
5. Is minimum valid bid ≥ my value? If yes → pass.
6. Recompute remaining budget from the results list.
7. Is minimum valid bid > remaining budget? If yes → pass.
8. Otherwise, bid the minimum valid bid and report the recomputed budget.

**What went wrong in review:**

- **Lot 5 (and likely Lot 2, Round 1):** I bid the minimum raise *increment* (e.g., 4) as if it were the total bid, when the standing high was already 4. My bid of 4 did not exceed the standing high of 4, so I never actually raised. I lost a lot worth 49 to me that I could have won at 8. **Fix: always compute bid = standing_high + minimum_raise. Verify the result is strictly greater than the standing high before submitting.**
- In a prior episode, I incorrectly treated a pending bid as already spent, reducing my perceived budget. **Fix: pending bids never reduce budget. Only confirmed wins in the results list do.**
- In a prior episode, I reported a budget exceeding my starting budget, confirming I was carrying a faulty running total. **Fix: always recompute from the results list, never carry a total forward.**