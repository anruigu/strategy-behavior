---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1603
---
# Auction Playbook

## Initial Setup & Budget Tracking
* Read the initial budget stated in the opening prompt carefully (do not assume it defaults to 100 or any fixed constant).
* Maintain exact budget arithmetic: `remaining_budget = initial_budget - total_spent_on_won_lots`.
* Always report `[budget: remaining_budget]` accurately in every turn.
* Never place a bid exceeding `remaining_budget`.

## Round 1 Bidding (Opening Round)
* Check if the minimum valid bid (`minimum_raise` if standing bid is 0, otherwise `standing_bid + minimum_raise`) is strictly less than the lot's valuation to me and within `remaining_budget`.
* If viable, bid the exact minimum valid bid to maintain optionality and avoid driving up the price early.
* If the minimum valid bid meets or exceeds the lot valuation or `remaining_budget`, reply `[bid: pass]`.

## Round 2 Bidding (Final Round)
* If the minimum required raise (`standing_bid + minimum_raise`) exceeds valuation or `remaining_budget`, reply `[bid: pass]`.
* When bidding:
  * Select a target bid strictly below valuation and at or below `remaining_budget` to guarantee a positive surplus.
  * For contested lots, place a competitive bid above the minimum required raise (targeting roughly 75%–85% of valuation, or up to valuation minus minimum raise) to win over competing final bids while capturing surplus.
  * On late or final lots with ample remaining budget, bid near valuation minus 1 minimum raise to maximize the probability of winning surplus.
* Ensure all bids satisfy: `standing_bid + minimum_raise <= bid <= min(valuation - 1, remaining_budget)`.