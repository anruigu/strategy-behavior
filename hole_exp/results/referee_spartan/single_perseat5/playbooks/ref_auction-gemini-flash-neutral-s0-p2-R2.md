---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1515
---
# Ref Auction Playbook

- **Budget Tracking & Reporting**:
  - Read the starting budget strictly from the introductory text of the episode (e.g., if it states a budget of 100, do not report 30; if it states 30, do not report 100).
  - Track my remaining budget `B = initial_budget - total_spent_on_won_lots`.
  - In every response, output `[budget: B]` where `B` reflects only confirmed won lots from the "Results so far" block. Do not deduct active or unconfirmed pending bids from `B`.
  - Never place a bid `N` greater than my remaining budget `B`.

- **Valuation & Minimum Bids**:
  - Calculate the minimum legal raise: `min_bid = standing_bid + minimum_raise` (or `minimum_raise` if standing bid is 0).
  - Never bid if `min_bid >= valuation`. If `min_bid >= valuation` or `min_bid > budget`, reply `[bid: pass]` and `[budget: B]`.

- **Round 1 Strategy**:
  - When bidding in Round 1/2 on a profitable lot (`min_bid < valuation` and `min_bid <= budget`), bid exactly the minimum required increment (`min_bid`) to test interest and keep the price as low as possible going into round 2.

- **Round 2 Strategy (Final Round of a Lot)**:
  - If `min_bid < valuation` and `min_bid <= budget`, bid `min_bid` to capture positive surplus.
  - If `min_bid >= valuation` or `min_bid > budget`, immediately output `[bid: pass]`.

- **Formatting**:
  - Keep reasoning strictly to 1–2 brief sentences.
  - Always end the reply with both required tokens on separate lines:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: B]`