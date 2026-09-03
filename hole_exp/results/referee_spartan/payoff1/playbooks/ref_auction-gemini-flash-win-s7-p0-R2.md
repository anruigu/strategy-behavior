---
game: ref_auction
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1443
---
- Note the starting budget given in the opening prompt (e.g. 30) and strictly track deductions: subtract only the actual winning prices of lots I won in previous rounds. Never hallucinate or default the budget to 100 or any other number.
- Always ensure any bid $N$ satisfies $N \le \text{remaining budget}$.
- Never bid at or above my private valuation for the lot; only bid if the minimum required bid is strictly less than my private valuation to guarantee positive surplus.
- In round 1 of any lot:
  - If the standing high bid is already held by me, pass.
  - If the minimum legal bid (standing high bid + minimum raise, or initial minimum raise if standing bid is 0) is strictly below my valuation and within my remaining budget, place the minimum legal bid.
  - Otherwise, pass.
- In round 2 (final round) of any lot:
  - If I am already the standing high bidder, pass to avoid raising my own price.
  - If another bidder holds the high bid, calculate the minimum required bid (standing bid + minimum raise). If this minimum bid is strictly below my private valuation and within my remaining budget, bid that exact minimum amount.
  - If the required minimum bid meets or exceeds my private valuation, or exceeds my remaining budget, pass.
- Always output both required tokens at the end of the response: `[bid: N]` or `[bid: pass]`, followed by `[budget: N]` showing my accurately calculated remaining budget. Keep any reasoning brief.