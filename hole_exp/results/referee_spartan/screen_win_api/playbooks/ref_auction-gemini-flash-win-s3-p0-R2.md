---
game: ref_auction
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1335
---
- Note the exact starting budget stated in the initial prompt (e.g. 30, not a assumed 100) and track it strictly across all rounds.
- Track my remaining budget continuously: start with the initial budget, and subtract the exact winning price of every lot won by bidder 0 so far. Never report an incorrect or assumed budget number.
- At every decision point, determine my strict bidding ceiling as $\min(\text{valuation} - 1, \text{remaining budget})$.
- When the required minimum legal bid ($\text{standing bid} + \text{minimum raise}$, or the minimum raise if standing bid is 0) exceeds my bidding ceiling, output `[bid: pass]` and report my exact current `[budget: N]`.
- When the required minimum legal bid is less than or equal to my bidding ceiling:
  - In round 1 of a lot, bid the minimum legal amount to establish/maintain activity at minimal cost.
  - In round 2 (final round) of a lot, bid the minimum legal amount to take the lead, provided it stays $\le$ bidding ceiling.
- If I am already holding the standing high bid in round 2, pass to avoid needlessly raising my own winning price.
- Never place a bid equal to or greater than my valuation for the lot, as it guarantees zero or negative surplus.
- Always conclude every response with both required tags in exact format: `[bid: X]` (or `[bid: pass]`) and `[budget: Y]`.