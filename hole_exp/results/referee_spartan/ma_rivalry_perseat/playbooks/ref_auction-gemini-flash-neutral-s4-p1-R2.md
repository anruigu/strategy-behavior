---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 2040
---
# Playbook for Ref Auction

### Budget Tracking & Reporting
- Read the starting budget explicitly from the opening prompt of the episode (e.g. 30) and do not default to 100.
- Track won lots strictly from the running `Results so far` history.
- In every reply, calculate `remaining_budget = starting_budget - sum(prices paid for lots won by me)`.
- Always report `[budget: remaining_budget]` accurately without resetting or inflating the amount.

### Round 1 Strategy
- If `standing_high_bid == 0`: bid `minimum_raise` as long as `minimum_raise < value` and `minimum_raise <= remaining_budget`.
- If there is an existing standing bid: bid `standing_high_bid + minimum_raise` provided it is safely below `value` and within `remaining_budget`.
- If the required bid exceeds `value` or `remaining_budget`, bid `[bid: pass]`.
- Always stick to the minimum valid raise to avoid needlessly driving up the price.

### Round 2 Strategy (Final Round of Lot)
- Other bidders frequently bid in round 2 (often reaching standing bids around 12 to 24).
- Calculate `next_min_bid = standing_high_bid + minimum_raise`.
- When the lot is highly valuable (value >> estimate) and `next_min_bid` is well below valuation, consider placing a bid slightly above `next_min_bid` (or up to valuation / budget limits) to decisively outbid rival round-2 bids, rather than just matching the minimum raise which often gets sniped.
- If `next_min_bid < value` and `next_min_bid <= remaining_budget`: bid an amount between `next_min_bid` and `value - 1` (capped at `remaining_budget`) that leaves healthy surplus while securing the win.
- If `next_min_bid >= value` or `next_min_bid > remaining_budget`: output `[bid: pass]`. Never bid equal to or above valuation.

### Budget Allocation & Margin Management
- Pass on low-margin lots (surplus ≤ 2 or 3) if budget is constrained (e.g. starting budget 30), conserving capital for lots with high surplus potential.
- When budget is tight, do not win low-value lots that prevent bidding on future high-valuation opportunities.