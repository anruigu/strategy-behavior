---
game: ref_auction
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1789
---
# Auction Playbook

- **Budget Tracking**:
  - Always track the exact initial budget and deduct the cost of won lots after each lot concludes.
  - Never invent or default to an arbitrary budget (e.g., 100). Calculate `current_budget = initial_budget - sum(costs of lots won)`.
  - Report the exact remaining budget in every `[budget: N]` tag.

- **Bid Feasibility & Constraints**:
  - Never place a bid `N` that exceeds my `current_budget`.
  - Never place a bid `N` that exceeds or equals my valuation of the lot (`N < valuation`); a bid must offer a positive expected surplus (`valuation - N > 0`).
  - If `standing_bid + min_raise > current_budget` or `standing_bid + min_raise >= valuation`, output `[bid: pass]` along with `[budget: current_budget]`.

- **Bidding Strategy - Round 1/2**:
  - If the standing high bid is 0, bid the minimum raise: `[bid: min_raise]`.
  - If there is a standing high bid, bid exactly the minimum required raise: `[bid: standing_bid + min_raise]`, provided it is within budget and below valuation; otherwise pass.
  - Avoid opening with arbitrary large bids that drive up the price unnecessarily.

- **Bidding Strategy - Round 2/2 (Final Round)**:
  - If I am already holding the standing high bid, pass to avoid bidding against myself.
  - If another bidder holds the standing high bid, calculate `target_bid = standing_bid + min_raise`.
  - If `target_bid <= current_budget` and `target_bid < valuation`, place `[bid: target_bid]`.
  - If the surplus on a lot is marginal and future lots with higher valuation-to-cost potential remain, conserve budget by passing on low-margin lots.

- **Formatting**:
  - Always end responses strictly with the required tokens on separate lines or cleanly formatted:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`