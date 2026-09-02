---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1632
---
# Ref Auction Playbook

- **Budget Tracking & Reporting**:
  - Track starting budget correctly from the initial game prompt and deduct only what I actually paid for lots won in past results.
  - In every response, output `[budget: B]` where `B` is my exact remaining budget after previously won lots (do not deduct active unconfirmed bids from `B`, and do not misstate the initial budget).
  - Never place a bid `N` greater than my remaining budget `B`.

- **Valuation & Minimum Bids**:
  - Calculate the minimum legal raise: `min_bid = standing_bid + minimum_raise` (or `minimum_raise` if standing bid is 0).
  - Never bid if `min_bid >= valuation`. If `min_bid >= valuation` or `min_bid > budget`, reply `[bid: pass]` and `[budget: B]`.

- **Round 1 Strategy**:
  - When bidding in Round 1/2 on a profitable lot (`min_bid < valuation` and `min_bid <= budget`), bid exactly the minimum required increment (`min_bid`) to keep prices as low as possible going into round 2.

- **Round 2 Strategy (Final Round of a Lot)**:
  - For intermediate lots (Lots 1 to N-1), bid `min_bid` as long as `min_bid < valuation` and within budget to secure positive surplus without overpaying.
  - On the final round of the final lot (or when no valuable upcoming lots remain), if the standing bid is below my valuation and my budget allows, bid up to `min(valuation - 1, budget)` if necessary to secure the win, or bid the minimum winning amount if opponents are low.

- **Formatting**:
  - Keep reasoning strictly to 1–2 lines.
  - Always end the reply with both required tokens on separate lines:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: B]`