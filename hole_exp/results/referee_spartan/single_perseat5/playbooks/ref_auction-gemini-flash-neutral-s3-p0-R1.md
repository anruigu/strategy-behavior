---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1426
---
### Budget Management & Token Tracking
- Track the actual initial starting budget stated in the opening prompt (e.g., 30) and subtract the winning prices of lots I have actually won. Never jump to an arbitrary number like 100.
- State `[budget: current_budget]` accurately on every turn, where `current_budget = initial_budget - sum(prices of lots won)`.

### Bidding Strategy
- Calculate the minimum allowable bid: `standing_bid + minimum_raise` (or just `minimum_raise` if standing bid is 0).
- Check two strict upper bounds for any bid: my valuation of the lot, and my remaining budget.
- If the minimum allowable bid exceeds either my valuation or my remaining budget, output `[bid: pass]`.
- In Round 1 of any lot:
  - If the minimum allowable bid is strictly below valuation and budget, bid exactly the minimum allowable bid. Do not jump-bid.
- In Round 2 (final round of a lot):
  - Do not place arbitrary medium jump-bids that leave room for opponents to outbid while staying below my valuation.
  - If the lot is high-value and my budget allows, bid aggressively up to `valuation - 1` (or `budget`, whichever is lower) to maximize winning probability, provided it yields positive surplus.
  - If the minimum bid already approaches valuation/budget, bid the minimum allowable amount if profitable; otherwise pass.
- When passing, always pair `[bid: pass]` with the current remaining budget: `[budget: current_budget]`.