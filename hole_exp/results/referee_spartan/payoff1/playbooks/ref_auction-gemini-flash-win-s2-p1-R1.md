---
game: ref_auction
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1071
---
- Track my remaining budget strictly: initialize with the starting budget provided in the prompt, deduct the exact amount paid only when a lot is won, and output `[budget: remaining_budget]` accurately on every turn. Never hallucinate a default budget like 100.
- When evaluating a bid, calculate the minimum allowable bid (`standing_high_bid + minimum_raise`, or `minimum_raise` if standing bid is 0).
- If the minimum allowable bid exceeds my valuation for the lot or exceeds my remaining budget, output `[bid: pass]`.
- In round 1 of any lot, if the minimum allowable bid is below my valuation and within budget, bid exactly the minimum allowable bid to stay in contention cheaply.
- In round 2 (final round of a lot), bid the minimum allowable raise if it leaves a positive surplus (`valuation - bid > 0`) and is within my remaining budget; otherwise pass.
- Never bid above my valuation, as winning at a price higher than valuation yields negative score.
- Ensure every reply ends with both required bracketed tokens: `[bid: N]` (or `[bid: pass]`) and `[budget: N]`.