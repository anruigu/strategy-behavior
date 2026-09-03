---
game: ref_auction
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 1937
---
# Auction Playbook

- **Track Actual Budget Accurately**:
  - Read the exact starting budget stated in the opening prompt (e.g., 30) and do not default to 100 or any other arbitrary figure.
  - Review the "Results so far" block on every turn: whenever I win a lot (`bidder 0 won at X`), subtract `X` from my running budget balance.
  - Report the exact current arithmetic balance in `[budget: N]` on every single turn, including passes. Never increase or hallucinate budget mid-game.

- **Valuation and Budget Bounds**:
  - Hard constraint: never bid above my valuation for a lot (`bid < valuation` or `bid <= valuation`).
  - Hard constraint: never bid more than my remaining available budget (`bid <= remaining budget`).
  - If the minimum legal bid (`standing high bid + minimum raise`, or `minimum raise` if standing bid is 0) exceeds either my valuation or my remaining budget, output `[bid: pass]`.

- **Bidding Strategy by Round**:
  - **Round 1/2**:
    - Always bid the exact minimum legal bid (`standing high bid + minimum raise`, or `minimum raise` if unbid) to stay in contention while conserving capital and avoiding unnecessary price inflation.
    - If the minimum legal bid already exceeds valuation or budget, pass immediately.
  - **Round 2/2 (Final Round for Lot)**:
    - If the minimum legal bid is strictly below valuation and within budget, bid to win.
    - Bid high enough to beat likely opponent bids, but strictly bounded by `min(valuation - 1, remaining budget)`.
    - If competitors are aggressive, choose a bid near `min(valuation - 1, remaining budget)` to secure the surplus.
    - If no positive surplus can be extracted (`min_bid >= valuation`), pass.

- **Output Formatting**:
  - Keep reasoning concise (1–2 sentences).
  - Always end the response with the exact two required tokens on separate lines:
    `[bid: N]` or `[bid: pass]`
    `[budget: N]` (reflecting the exact tracked budget remaining).