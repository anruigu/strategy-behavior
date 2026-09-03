---
game: ref_auction
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1634
---
# Ref Auction Playbook

- **Budget Tracking**:
  - Always read the initial budget stated in the opening prompt carefully.
  - Track remaining budget across lots: when I win a lot at price $P$, immediately subtract $P$ from my remaining budget for all subsequent rounds and lots.
  - Never invent or default to arbitrary budget numbers (e.g., 100); always report my exact actual remaining balance in `[budget: N]`.
  - Never place a bid $N$ greater than my remaining budget.

- **Bidding Strategy**:
  - **Valuation Ceiling**: Never place a bid $N \ge \text{my valuation}$. If the minimum allowable raise (`standing high bid + minimum raise`) meets or exceeds my private valuation, immediately reply `[bid: pass]`.
  - **Round 1 Strategy**:
    - If I want to compete on a lot, bid the minimum required amount (`standing high bid + minimum raise`, or the minimum opening raise if standing bid is 0) as long as it is comfortably below my valuation and within remaining budget.
    - Do not jump-bid unnecessarily in Round 1; keep prices low going into the final round.
  - **Round 2 (Final Round) Strategy**:
    - If the minimum legal bid is strictly less than my private valuation and does not exceed my remaining budget, place the minimum legal bid to secure positive surplus.
    - If the required bid leaves zero or negative surplus, or exceeds my remaining budget, reply `[bid: pass]`.

- **Output Format**:
  - Keep reasoning strictly to 1–2 sentences.
  - Conclude every turn with the exact two tokens on separate lines:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: B]` (where $B$ is my strictly calculated remaining budget).