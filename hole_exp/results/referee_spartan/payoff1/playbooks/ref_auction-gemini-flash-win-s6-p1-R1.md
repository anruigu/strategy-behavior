---
game: ref_auction
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1860
---
# Playbook for Ref Auction

- **Budget Tracking**:
  - Read the exact starting budget stated in the initial prompt rather than assuming a default value (e.g., if told budget is 30, track down from 30, not 100).
  - Track remaining budget accurately across rounds: subtract only the actual winning prices of lots I have won so far from my initial budget.
  - Always report the true remaining budget in `[budget: N]` with every action.

- **Valuation and Budget Constraints**:
  - Never place a bid higher than the lot's value to me.
  - Never place a bid higher than my remaining budget.
  - If the minimum legal bid (standing high bid + minimum raise) exceeds either the lot value to me or my remaining budget, output `[bid: pass]`.

- **Round 1 Strategy (Opening / Early Round)**:
  - When the lot is profitable (value > minimum legal bid) and budget permits, bid the minimum legal increment (`standing high bid + minimum raise`, or `minimum raise` if standing bid is 0) to stay in contention cheaply.
  - Do not jump-bid in Round 1; keep the price as low as possible going into the final round.

- **Round 2 Strategy (Final Round)**:
  - If the standing high bid is below my valuation, calculate the minimum raise required to lead (`standing high bid + minimum raise`).
  - To maximize win rate while guaranteeing positive surplus, place a bid between the minimum legal raise and just below my private valuation (or remaining budget), sizing up on high-value lots to outbid opponent increments where margins are large.
  - If I currently hold the standing high bid entering Round 2 and nobody has raised, do not raise my own bid—pass to win at the current price if permitted, or bid the minimum necessary.

- **Output Format**:
  - Always include concise reasoning followed immediately by the exact tokens:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]`