---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 2009
---
# Auction Playbook

## Budget Tracking & Output Formatting
- Read the starting budget strictly from the introductory text (e.g., if the opening prompt says budget is 30, starting budget is 30; if it says 100, it is 100). Do not switch or reset the starting budget arbitrarily.
- Track my budget accurately across lots: when the prompt's `Results so far` indicates that `bidder 0` won a lot at price $P$, subtract $P$ from my remaining budget (`remaining_budget = remaining_budget - P`). If another bidder won, my budget remains unchanged.
- Always report `[budget: N]` with my current exact remaining budget.
- Every bid $B$ must strictly satisfy $B \le \text{remaining\_budget}$. Never bid more than my available cash.

## Round 1 Strategy (Opening Round)
- Calculate the minimum legal entry: `min_entry = (standing_bid == 0 ? min_raise : standing_bid + min_raise)`.
- If `min_entry < my_valuation` and `min_entry <= remaining_budget`, bid exactly `min_entry`.
- Never jump-bid or bid above the minimum legal amount in Round 1; keeping the price low leaves room for strategic bidding in Round 2.
- If `min_entry >= my_valuation` or `min_entry > remaining_budget`, bid `[bid: pass]`.

## Round 2 Strategy (Final Round of a Lot)
- Calculate the minimum legal raise: `min_bid = standing_bid + min_raise`.
- If `min_bid >= my_valuation` or `min_bid > remaining_budget`, reply with `[bid: pass]`.
- If `min_bid < my_valuation`:
  - Competitors frequently bid 1 to 2 increments above the standing bid in the final round.
  - Determine target bid: aiming for `min_bid + min_raise` (or standing bid + 2 raises) provides strong winning probability against standard bot raises.
  - If valuation permits, bid `min_bid + min_raise`, provided it remains strictly below valuation and within budget.
  - If surplus margin is tight (i.e., `min_bid + min_raise >= my_valuation`), bid exactly `min_bid`.
  - Hard limit: Always strictly cap any bid at `min(remaining_budget, my_valuation - 1)`. Never bid at or above valuation.