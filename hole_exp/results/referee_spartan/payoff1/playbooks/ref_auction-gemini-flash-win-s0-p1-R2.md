---
game: ref_auction
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1611
---
# Auction Playbook

- **Budget Tracking**:
  - Always read the exact initial budget stated in the opening prompt (do NOT assume 100 or any default number).
  - Explicitly track: `current_budget = initial_budget - sum(prices of lots won by bidder 1)`.
  - Every reply must output the exact remaining budget: `[budget: current_budget]`.
  - Never bid more than `current_budget`.

- **Valuation and Surplus Rules**:
  - Never place a bid `N` where `N >= valuation` for the current lot. Every bid must guarantee a positive surplus (`valuation - N > 0`).
  - If the required minimum bid (`standing_bid + min_raise` or `min_raise` if standing bid is 0) exceeds either `current_budget` or `valuation - 1`, output `[bid: pass]`.

- **Bidding Strategy - Round 1/2**:
  - If standing high bid is 0: bid the minimum raise: `[bid: min_raise]`.
  - If standing high bid is from another bidder: bid `standing_bid + min_raise` provided it is `< valuation` and `<= current_budget`; otherwise pass.
  - If standing high bid is already mine: pass.

- **Bidding Strategy - Round 2/2 (Final Round)**:
  - If I currently hold the standing high bid: pass to avoid bidding against myself.
  - If another bidder holds the standing high bid: calculate `target_bid = standing_bid + min_raise`.
  - If `target_bid < valuation` and `target_bid <= current_budget`, bid `[bid: target_bid]`.
  - If `target_bid >= valuation` or `target_bid > current_budget`, pass.

- **Output Formatting**:
  - Keep reasoning brief (1–2 sentences).
  - Strictly end every response with the required tokens:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`