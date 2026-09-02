---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 2487
---
# AUCTION PLAYBOOK

## Budget Tracking & Formatting
- Initialize budget tracking strictly from the starting budget explicitly stated in the game rules (e.g., 30 or 100). Maintain this exact base budget consistently across all rounds of all lots; do not switch starting budget values mid-game (e.g., jumping between 30 and 100).
- Only subtract expenditure from my remaining budget when "Results so far" explicitly confirms that `bidder 0` won a lot at a specified price. Deduct the actual winning price.
- If I did not win a completed lot, my budget remains unchanged.
- Always conclude every response with both required bracketed tokens: `[bid: N]` (or `[bid: pass]`) and `[budget: N]` reflecting my true remaining budget.

## Bidding Strategy

### Absolute Ceilings & Pass Conditions
- Compute the maximum allowable bid for any lot as $\min(\text{valuation}, \text{remaining budget})$.
- Never submit a bid exceeding valuation or remaining budget.
- The minimum valid bid is $\text{standing high bid} + \text{minimum raise}$ (or just $\text{minimum raise}$ if the standing bid is 0).
- If the minimum valid bid exceeds my valuation or my remaining budget, output `[bid: pass]`.

### Round 1 / 2 (Opening)
- If the standing high bid is 0 and the minimum raise is within budget and below valuation, bid exactly the minimum raise.
- If an opponent holds the standing bid and the minimum valid bid is within budget and below valuation, bid exactly $\text{standing high bid} + \text{minimum raise}$.
- Keep Round 1 bids strictly at the minimum required increment to avoid needlessly driving up the price before the closing round.

### Round 2 / 2 (Closing)
- If I already hold the standing high bid, do not raise against myself; pass if allowed.
- If an opponent holds the standing high bid, check if $\text{minimum valid bid} \le \min(\text{valuation}, \text{remaining budget})$:
  - If $\text{minimum valid bid} < \text{valuation}$ and fits within remaining budget, bid exactly $\text{standing high bid} + \text{minimum raise}$ to capture the positive surplus.
  - If the minimum valid bid is greater than or equal to valuation, output `[bid: pass]`.

### Multi-Lot Opportunity Cost & Budget Preservation
- Prioritize bids that secure large surplus margins ($\text{valuation} - \text{bid}$).
- When budget is constrained relative to remaining lots, pass on low-margin lots (where valuation is barely above estimate or bid) to preserve purchasing power for later high-margin opportunities.