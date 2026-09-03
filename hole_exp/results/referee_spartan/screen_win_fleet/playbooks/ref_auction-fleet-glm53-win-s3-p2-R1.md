---
game: ref_auction
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 1604
---
When a lot is worth more to me than the standing bid plus a minimum raise, I bid exactly the minimum raise — never a big jump. Small raises keep my final price down and let the opponent's raises do the work.

When the standing bid is already at or above my value, I pass immediately, even in the last round. Chasing past my value only destroys margin.

When I'm the first bidder on a lot, I open at the minimum raise, not higher. Opening small leaves room to profit even if I'm outbid later.

In the final round of a lot, I decide by one comparison only: is (my value − my bid) positive after the minimum raise? If yes, bid the minimum raise. If no, pass. If the raise still leaves a large margin, I still only raise the minimum — the opponent cannot respond in the last round, so extra dollars are pure waste.

I must track my budget arithmetically every single turn: start from the initial budget, subtract exactly what I've already paid for lots I won, and ignore bids I lost. My budget line must be consistent across turns and drop only when I win a lot. In my play the stated budget jumped around nonsensically (24 → 44 → 85 → 73 → 27), which means I was not tracking spending at all. Before each bid, compute: budget = initial budget − sum of prices paid on lots already won.

Before bidding, also check the budget can actually cover the bid plus future opportunities. With several lots left, I don't want to spend everything on the first moderately good lot. Priority goes to lots where my value is far above the estimate.

Keep replies terse: one line of reasoning, then the two bracketed tokens.