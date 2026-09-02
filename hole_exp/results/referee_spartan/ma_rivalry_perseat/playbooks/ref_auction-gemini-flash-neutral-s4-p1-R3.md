---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 2191
---
# Playbook for Ref Auction

### Budget Tracking & Reporting
- Read the starting budget explicitly from the opening prompt of the episode (e.g., 30 or 100) and never assume a default.
- Track won lots strictly from the running `Results so far` history by checking which lots were won by bidder 1.
- In every single reply, calculate `remaining_budget = starting_budget - sum(prices paid for lots won by bidder 1)`.
- Never report a hallucinated budget (e.g. defaulting to 100 or resetting mid-game); always report `[budget: remaining_budget]` accurately.
- Ensure any placed bid satisfies `bid <= remaining_budget`.

### Round 1 Strategy
- If `standing_high_bid == 0`: bid `minimum_raise` as long as `minimum_raise < value` and `minimum_raise <= remaining_budget`.
- If there is an existing standing bid: bid `standing_high_bid + minimum_raise` provided it is strictly below `value` and within `remaining_budget`.
- If the required bid exceeds or equals `value`, or exceeds `remaining_budget`, bid `[bid: pass]`.
- Keep round 1 bids to the exact minimum valid raise to avoid needlessly driving up the price early.

### Round 2 Strategy (Final Round of Lot)
- Competitors routinely raise in round 2, often bidding above the bare minimum raise (e.g., reaching 25-32 on high-estimate lots).
- Calculate `next_min_bid = standing_high_bid + minimum_raise`.
- If `next_min_bid >= value` or `next_min_bid > remaining_budget`: output `[bid: pass]`. Never bid equal to or above valuation, and never bid above remaining budget.
- For high-surplus lots (value significantly higher than `next_min_bid`), bid aggressively above `next_min_bid` (e.g., `standing_high_bid + 2 * minimum_raise` or slightly more, capped at `value - 4` and `remaining_budget`) to beat competitor snipes.
- For moderate- or low-surplus lots, bid `next_min_bid` if it preserves acceptable margin, or pass.

### Budget Allocation & Capital Preservation
- When starting budget is small relative to estimates (e.g., budget 30), treat budget as scarce: pass on marginal lots (surplus < 5) to reserve funds for standout high-value lots.
- Prioritize lots with the highest ratio of surplus (`value - expected cost`) to capital committed.