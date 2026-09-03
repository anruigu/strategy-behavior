---
game: ref_auction
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1485
---
- Track my actual starting budget accurately from the initial prompt; do not reset or inflate the reported budget to an arbitrary number like 100.
- When calculating remaining budget to report in `[budget: N]`, deduct only the amounts actually paid for lots won in previous rounds, minus any tentative bid if required, maintaining exact consistency with my actual available funds.
- Never bid above my private valuation for the current lot. If the minimum required raise meets or exceeds my private valuation, pass immediately.
- Never bid more than my current available budget, regardless of the lot's valuation.
- In round 1 of any lot:
  - If the minimum legal bid (standing high bid + minimum raise, or initial minimum raise if standing bid is 0) is well below my valuation and within budget, place the minimum legal bid to stay active.
  - If the standing high bid is already held by me, pass.
- In round 2 (final round) of any lot:
  - If I am already the standing high bidder, pass to avoid bidding against myself.
  - If another bidder holds the high bid, calculate the minimum required bid (standing bid + minimum raise). If this minimum bid is less than my private value and within my remaining budget, bid that exact minimum amount to capture positive surplus.
  - If the required minimum bid exceeds my private value or my remaining budget, pass.
- Format every action strictly with `[bid: N]` or `[bid: pass]` followed by `[budget: N]` reflecting my true remaining budget.