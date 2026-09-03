---
game: ref_auction
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1632
---
# Playbook: Ref Auction

- **Strictly track starting budget**:
  - Read the exact starting budget from the initial episode description (e.g., if it states a budget of 30, it is 30 for the entire game; never revert to a default like 100).
  - Explicitly carry forward this specific starting budget across every lot and round without forgetting it.

- **Update budget remaining across lots**:
  - Calculate remaining budget strictly as `starting_budget - sum(my_winning_payments_in_results_so_far)`.
  - Do not deduct money for currently active bids; deduct only when a lot appears under "Results so far" as won by me.
  - Report the exact calculated remaining cash in `[budget: N]` on every response.

- **Check budget constraints before bidding**:
  - Calculate the minimum required bid: `standing high bid + minimum raise`.
  - If the minimum required bid exceeds my actual remaining budget, output `[bid: pass]`.
  - Never place a bid greater than my remaining budget.

- **Evaluate surplus before bidding**:
  - If the minimum required bid is greater than or equal to my private valuation for the lot, output `[bid: pass]`.
  - If the minimum required bid is strictly less than my private valuation and within my remaining budget, bid the exact minimum required amount: `[bid: standing_bid + min_raise]`.

- **Preserve surplus across rounds**:
  - In Round 1, always raise by the minimum possible increment to stay in contention without inflating the price unnecessarily.
  - In Round 2, bid the minimum increment if and only if it still yields positive surplus (`valuation - bid > 0`) and remains within budget; otherwise, pass.