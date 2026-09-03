---
game: ref_auction
model: gemini-flash
condition: win
seed: 6
round: 2
chars: 1714
---
# Playbook: Open Ascending Multi-Lot Auction

- **Budget Tracking**: 
  - Read the exact starting budget stated in the opening prompt (e.g., 30) and strictly track it throughout the game. Never assume or hallucinate a default budget (e.g., 100).
  - In every reply, report the actual remaining budget: `[budget: current_balance]`.
  - When I win a lot, subtract the price I paid from my budget balance before making any subsequent bids.
  - If I have not won any lots, my remaining budget stays exactly equal to the initial starting budget.

- **Bid Limits & Constraints**:
  - Absolute cap for any bid: `cap = min(valuation - 1, current_budget)`.
  - Never place a bid that exceeds this cap under any circumstances.
  - If the required minimum bid (`standing high bid + minimum raise`) is strictly greater than `cap`, output `[bid: pass]`.

- **Round 1 Strategy (Opening/Contention)**:
  - If the standing high bid is 0, bid the minimum opening amount (`minimum raise`), provided it is $\le cap$.
  - If another bidder holds the standing high bid, bid the minimum valid increment (`standing high bid + minimum raise`), provided it is $\le cap$.
  - Otherwise, pass.

- **Round 2 Strategy (Final Round of a Lot)**:
  - Check the minimum required bid: `min_bid = standing high bid + minimum raise`.
  - If `min_bid > cap`, output `[bid: pass]`.
  - If `min_bid <= cap`, place a strong competitive bid near or at `cap` (e.g., `cap` or close to it) to maximize the probability of winning the lot while strictly locking in positive surplus and respecting the budget.

- **Formatting**:
  - Always end every prompt response with exactly two tokens on their own lines:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`