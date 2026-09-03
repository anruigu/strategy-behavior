---
game: ref_auction
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1535
---
- Always read the exact initial budget from the prompt on turn 1 and track it meticulously; never assume or default to 100.
- Track remaining budget accurately throughout the game: $\text{remaining budget} = \text{initial budget} - \sum(\text{prices paid for lots won by bidder 0})$. Only deduct when a lot is officially listed as won by bidder 0 in the results.
- In Round 1 of any lot:
  - If my private value or remaining budget is strictly less than the minimum required bid (`standing high bid + minimum raise`, or `minimum raise` if standing bid is 0), pass immediately: `[bid: pass]`.
  - Otherwise, bid exactly the minimum allowable increment (`standing high bid + minimum raise` or `minimum raise`) to stay in contention without inflating the price.
- In Round 2 (the final round for the lot):
  - Calculate my maximum bid ceiling as $\min(\text{remaining budget}, \text{lot value to me} - 1)$.
  - If the required minimum bid (`standing high bid + minimum raise`) exceeds this ceiling, pass: output `[bid: pass]`.
  - If the required minimum bid is $\le \text{ceiling}$, place a strategic final bid between the minimum required bid and the ceiling, strictly $\le \text{ceiling}$.
- Never place a bid that exceeds or equals my private valuation for a lot.
- Never place a bid that exceeds my current actual remaining budget.
- Always output both required tokens cleanly at the end of every reply:
  - `[bid: N]` or `[bid: pass]`
  - `[budget: N]` (must reflect the true current remaining budget, never a hallucinated default).