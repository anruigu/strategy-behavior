---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1788
---
# Playbook: Multi-Lot Ascending Auction

### Budget Tracking & Reporting
- Read the initial starting budget carefully in the opening rules (do not default to assumptions like 100).
- Keep an exact running ledger of remaining cash: subtract only the actual winning prices of lots I won, as reported in "Results so far". Money is not deducted for losing bids.
- In every reply, report my true remaining budget in `[budget: N]`. Never subtract the current active bid before winning the lot.

### Valuation & Bidding Thresholds
- Compute my profit margin for any bid as `my_value - bid_amount`.
- Never place a bid greater than or equal to my valuation (`bid < my_value` strictly).
- If the required minimum legal bid (`standing_bid + min_raise`, or `min_raise` if standing bid is 0) is greater than or equal to my valuation, or exceeds my remaining budget, output `[bid: pass]`.

### Round 1 Strategy (Opening / Early Round)
- If standing bid is 0 and `min_raise < my_value`, bid exactly `min_raise`.
- If another bidder has already bid and `standing_bid + min_raise < my_value`, bid the exact minimum legal raise (`standing_bid + min_raise`).
- Do not jump-bid or raise by more than the minimum increment in Round 1.

### Round 2 Strategy (Final Round of Lot)
- If competing in Round 2, bid only if `standing_bid + min_raise < my_value` and within remaining budget.
- Place a bid that balances win probability and surplus: bid the minimum allowable raise (`standing_bid + min_raise`) when surplus is tight, or a targeted bid below valuation to lock in positive margin.
- Never bid more than my remaining budget or my private valuation under any circumstance.

### Formatting
- Always end my response with both required tags on separate lines:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`