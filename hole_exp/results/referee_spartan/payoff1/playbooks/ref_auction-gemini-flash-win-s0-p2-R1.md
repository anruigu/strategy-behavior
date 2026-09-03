---
game: ref_auction
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1607
---
# Playbook: Ref Auction

- **Track the starting budget accurately**: Read the starting budget directly from the initial prompt instructions (e.g., if it says budget of 30, initialize at 30; do not default to 100 or any assumed standard). 
- **Update budget remaining across lots**:
  - Keep running track of the current remaining budget by taking the initial budget and subtracting only the winning bids of lots already won (as shown under "Results so far").
  - Do not deduct bids while an auction for a lot is currently active; only deduct after a lot is won.
  - Report the exact remaining cash in `[budget: N]` on every turn.

- **Check budget constraints before bidding**:
  - When the minimum required bid (`standing high bid + minimum raise`) exceeds my remaining budget, output `[bid: pass]`.
  - Never place a bid that exceeds my currently available budget.

- **Evaluate surplus before bidding**:
  - Calculate the minimum required bid as `standing high bid + minimum raise`.
  - If the minimum required bid is greater than or equal to my private valuation for the lot, output `[bid: pass]`.
  - If the minimum required bid is strictly less than my private valuation and within my remaining budget, bid the exact minimum required amount: `[bid: standing_bid + min_raise]`.

- **Preserve surplus across rounds**:
  - In Round 1, always raise by the minimum possible increment to stay in contention without inflating the price unnecessarily.
  - In Round 2, bid the minimum increment if and only if it still yields positive surplus (`valuation - bid > 0`) and remains within budget; otherwise, pass.