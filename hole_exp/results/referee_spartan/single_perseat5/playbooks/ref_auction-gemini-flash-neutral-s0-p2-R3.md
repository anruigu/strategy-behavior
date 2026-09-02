---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1581
---
# Ref Auction Playbook

- **Budget Tracking & Reporting**:
  - Read the starting budget strictly from the introductory text of the episode (e.g., if it states a budget of 30, my initial budget is 30; if it states 100, my initial budget is 100).
  - Never hallucinate or switch the starting budget mid-episode (e.g., do not switch from 30 to 100).
  - Track remaining budget: `B = initial_budget - sum(winning_prices_of_my_won_lots)`.
  - In every response, output `[budget: B]` reflecting confirmed won lots from the "Results so far" block. Do not deduct active bids or unconfirmed pending bids until a lot is officially won.
  - Never place a bid `N` greater than my remaining budget `B`.

- **Valuation & Minimum Bids**:
  - Calculate the minimum legal raise: `min_bid = standing_bid + minimum_raise` (or `minimum_raise` if standing bid is 0).
  - Never bid if `min_bid >= valuation`. If `min_bid >= valuation` or `min_bid > B`, reply `[bid: pass]` and `[budget: B]`.

- **Round 1 Strategy**:
  - When bidding in Round 1/2 on a profitable lot (`min_bid < valuation` and `min_bid <= B`), bid exactly the minimum required increment (`min_bid`) to keep the price low.

- **Round 2 Strategy (Final Round of a Lot)**:
  - If `min_bid < valuation` and `min_bid <= B`, bid `min_bid` to capture positive surplus.
  - If `min_bid >= valuation` or `min_bid > B`, immediately output `[bid: pass]`.

- **Formatting**:
  - Keep reasoning strictly to 1–2 brief sentences.
  - Always end the reply with both required tokens on separate lines:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: B]`