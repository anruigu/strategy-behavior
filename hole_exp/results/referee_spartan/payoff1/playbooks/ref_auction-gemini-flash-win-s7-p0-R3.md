---
game: ref_auction
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1424
---
- Read and record the exact initial budget from the opening prompt (do not assume 100 or any default). Track remaining budget strictly: `remaining budget = starting budget - sum(prices paid for lots won by me)`.
- Always ensure any bid $N$ satisfies $N \le \text{remaining budget}$.
- Never bid at or above my private valuation for the lot; only bid if the minimum required bid is strictly less than my private valuation to guarantee positive surplus.
- In round 1 of any lot:
  - If the standing high bid is already held by me, pass.
  - If the minimum legal bid (standing high bid + minimum raise, or initial minimum raise if standing bid is 0) is strictly below my valuation and $\le \text{remaining budget}$, bid the exact minimum legal amount.
  - Otherwise, pass.
- In round 2 (final round) of any lot:
  - If I am already the standing high bidder, pass to avoid raising my own price.
  - If another bidder holds the high bid, calculate the minimum required bid (standing bid + minimum raise). If this minimum bid is strictly below my private valuation and $\le \text{remaining budget}$, bid that exact minimum amount.
  - If the required minimum bid meets or exceeds my private valuation, or exceeds my remaining budget, pass.
- Always output both required tokens in every reply: `[bid: N]` or `[bid: pass]`, followed by `[budget: N]` showing the exact currently calculated remaining budget. Keep any reasoning brief.