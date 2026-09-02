---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 2359
---
# AUCTION PLAYBOOK

## Budget Tracking & Formatting
- Initialize budget tracking strictly from the starting budget explicitly stated in the game rules (e.g., 30 or 100). Maintain this exact number across all rounds of all lots; do not switch or reset budget numbers mid-game.
- Only subtract expenditure from my remaining budget when "Results so far" explicitly confirms that `bidder 0` won a lot at a specified price.
- Always conclude every response with both required bracketed tokens on their own lines or at the very end: `[bid: N]` (or `[bid: pass]`) and `[budget: N]` reflecting my true remaining budget.

## Bidding Strategy

### Absolute Ceilings & Pass Conditions
- Compute the maximum allowable bid for any lot as $\min(\text{valuation}, \text{remaining budget})$.
- Never submit a bid exceeding valuation or remaining budget.
- The minimum valid bid when raising is $\text{standing high bid} + \text{minimum raise}$ (or just $\text{minimum raise}$ if the standing bid is 0).
- If the minimum valid bid exceeds my valuation or my remaining budget, output `[bid: pass]`.

### Round 1 / 2 (Opening)
- If the standing high bid is 0 and the minimum raise is below valuation and within budget, bid exactly the minimum raise.
- If an opponent holds the standing bid and the minimum valid bid is below valuation and within budget, bid exactly $\text{standing high bid} + \text{minimum raise}$.
- Keep Round 1 bids at the absolute minimum required to avoid unnecessarily inflating the price before the closing round.

### Round 2 / 2 (Closing)
- If I already hold the standing high bid, do not raise against myself; pass if possible or hold standing.
- If an opponent holds the standing high bid, check if $\text{minimum valid bid} \le \min(\text{valuation}, \text{remaining budget})$:
  - If it is strictly below valuation and within budget, place the bid (defaulting to the minimum required bid $\text{standing high bid} + \text{minimum raise}$) to capture positive surplus.
  - If the minimum valid bid is equal to or greater than valuation, output `[bid: pass]`.

### Multi-Lot Opportunity Cost
- Reserve budget for lots where valuation significantly exceeds the typical winning price.
- If budget is tight, pass early on low-margin lots (where valuation is barely above estimate or opening price) to preserve liquidity for subsequent high-margin lots.