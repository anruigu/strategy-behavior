---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 2462
---
# AUCTION PLAYBOOK

## Budget Tracking & Formatting
- Initialize my budget tracking strictly from the starting budget given in the opening prompt (e.g., 30 or 100). Never hallucinate an arbitrary budget number; start at the actual specified amount and deduct the exact winning cost of any lot I win as reported in the "Results so far".
- Always end every reply with both required bracketed tokens: `[bid: N]` (or `[bid: pass]`) and `[budget: N]` reflecting my true remaining budget.

## Bidding Strategy

### Valuation & Budget Limits
- Compute my absolute bid ceiling for any lot as $\min(\text{valuation}, \text{remaining budget})$.
- Never submit a bid strictly greater than my valuation for the lot under any circumstances, as it risks negative surplus.
- Never submit a bid that exceeds my remaining budget.
- If the minimum required raise ($\text{standing high bid} + \text{minimum raise}$) exceeds my valuation or my remaining budget, output `[bid: pass]` immediately.

### Round 1 / 2 (Opening / Intermediate Bidding)
- If standing high bid is 0 and the minimum raise is less than my valuation, bid the exact minimum raise ($\text{minimum raise}$) to test interest cheaply.
- If an opponent holds the standing bid and the minimum required bid ($\text{standing high bid} + \text{minimum raise}$) is strictly less than my valuation, bid exactly the minimum required bid.
- Do not jump-bid in Round 1; keep the price low to avoid driving up the final round price unnecessarily.

### Round 2 / 2 (Final Decision for the Lot)
- If the standing high bid is already mine, bid nothing/pass unless the interface requires holding, but otherwise do not raise against myself.
- If an opponent holds the high bid, evaluate if $\text{minimum required bid} \le \min(\text{valuation} - 1, \text{remaining budget})$:
  - If yes, place a bid that is at least the minimum required raise. On high-margin, high-value lots where winning is critical, consider bidding slightly higher than the minimum increment if budget allows, but never exceed valuation.
  - If the minimum required bid yields zero or negative profit ($\ge \text{valuation}$), output `[bid: pass]`.

### Opportunity Cost & Multi-Lot Management
- Prioritize high-value lots with large surplus margins over low-value lots with 1–2 point margins, especially when budget is constrained.
- Pass on low-margin lots early if competing on them would deplete the budget needed for future high-valuation opportunities.