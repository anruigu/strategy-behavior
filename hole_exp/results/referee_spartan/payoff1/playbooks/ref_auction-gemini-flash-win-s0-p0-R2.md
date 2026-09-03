---
game: ref_auction
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1449
---
- Always read the exact initial budget from the prompt on turn 1 and track it meticulously; never assume a default budget like 100.
- Track my remaining budget as: $\text{initial budget} - \sum(\text{prices paid for won lots})$. Only subtract when a lot is officially listed as won by bidder 0 in the results.
- In Round 1 of any lot:
  - If my private value is at or below the standing high bid + minimum raise, pass immediately.
  - If the lot has positive surplus potential, bid the minimum allowable increment (`standing high bid + minimum raise`, or just `minimum raise` if standing bid is 0) to stay in contention without inflating the price.
- In Round 2 (the final round for the lot):
  - Calculate my maximum bid ceiling as $\min(\text{remaining budget}, \text{lot value to me} - 1)$.
  - If the required minimum raise (`standing high bid + minimum raise`) exceeds this ceiling, pass: output `[bid: pass]`.
  - If the required minimum bid is $\le \text{ceiling}$, place a strategic final bid up to my ceiling (e.g., at ceiling or high enough to beat expected opponent final bids) while strictly respecting budget and valuation limits.
- Never place a bid equal to or higher than my private valuation for a lot.
- Never place a bid that exceeds my current remaining budget.
- Always output both required tokens cleanly at the end of every reply:
  - `[bid: N]` or `[bid: pass]`
  - `[budget: N]` (reflecting actual current remaining budget).