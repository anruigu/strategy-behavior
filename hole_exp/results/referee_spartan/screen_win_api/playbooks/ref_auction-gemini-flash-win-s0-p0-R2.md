---
game: ref_auction
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1692
---
# Ref Auction Playbook

- **Budget Tracking**:
  - Always extract and memorize the exact starting budget stated in the opening prompt (e.g., 30, not an assumed default like 100).
  - Explicitly calculate remaining budget before every bid: `current_budget = initial_budget - sum(prices of all lots won by bidder 0 so far)`.
  - Never report or assume default/arbitrary budget figures; output the exact calculated remaining budget in `[budget: N]`.
  - Never place a bid $N > \text{remaining budget}$. If the minimum legal bid exceeds my remaining budget, output `[bid: pass]`.

- **Bidding Strategy**:
  - **Valuation Ceiling**: Never place a bid $N \ge \text{my valuation}$. If the minimum required bid (`standing high bid + minimum raise`, or `minimum raise` if standing bid is 0) is greater than or equal to my private valuation, immediately reply `[bid: pass]`.
  - **Round 1 Strategy**:
    - If the lot has positive expected surplus and is affordable, bid the minimum legal amount (`standing high bid + minimum raise`).
    - Keep early bidding minimal to avoid driving up the final price unnecessarily.
  - **Round 2 (Final Round) Strategy**:
    - Calculate minimum legal bid = `standing high bid + minimum raise`.
    - If `minimum legal bid < valuation` AND `minimum legal bid <= remaining budget`, place that minimum legal bid to secure positive surplus.
    - Otherwise, reply `[bid: pass]`.

- **Output Format**:
  - Keep reasoning strictly to 1–2 sentences.
  - Conclude every turn with the exact two tokens on separate lines:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: B]` (where $B$ is the true remaining balance calculated from the initial budget minus all actual spend).