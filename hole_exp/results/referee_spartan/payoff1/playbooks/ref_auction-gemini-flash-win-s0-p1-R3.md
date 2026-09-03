---
game: ref_auction
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1752
---
# Auction Playbook

- **Budget Tracking**:
  - Always read and record the exact initial budget from the initial game prompt (never assume 100 or any standard default).
  - Explicitly compute remaining budget at every step: `current_budget = initial_budget - sum(prices paid for all lots won by me so far)`.
  - Ensure every response outputs the exact current remaining budget: `[budget: current_budget]`.
  - Never submit a bid amount greater than `current_budget`.

- **Valuation and Surplus Rules**:
  - Never place a bid `N` where `N >= valuation` for the current lot. Every bid must yield a strictly positive surplus (`valuation - N > 0`).
  - Calculate required minimum bid: `min_required = standing_bid + min_raise` (or simply `min_raise` if standing bid is 0).
  - If `min_required >= valuation` or `min_required > current_budget`, output `[bid: pass]`.

- **Bidding Strategy - Round 1/2**:
  - If I hold the standing high bid: output `[bid: pass]`.
  - If standing high bid is 0: bid `[bid: min_raise]`, provided `min_raise < valuation` and `min_raise <= current_budget`.
  - If standing high bid is from another bidder: bid `[bid: standing_bid + min_raise]`, provided `standing_bid + min_raise < valuation` and `<= current_budget`; otherwise pass.

- **Bidding Strategy - Round 2/2 (Final Round)**:
  - If I hold the standing high bid: pass to avoid bidding against myself.
  - If another bidder holds the standing high bid: bid `[bid: standing_bid + min_raise]` if and only if `standing_bid + min_raise < valuation` and `<= current_budget`; otherwise pass.

- **Output Formatting**:
  - Keep reasoning concise (1–2 sentences).
  - Conclude every turn strictly with the exact bracketed tokens:
    `[bid: N]` or `[bid: pass]`
    `[budget: N]`