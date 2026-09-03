---
game: ref_auction
model: gpt-mini
condition: win
seed: 1
round: 1
chars: 1763
---
When a lot opens with no bids and my private value > 0, I place a small opening bid (the minimum) rather than skipping or jumping high.

When there is a standing high bid, I raise only if the next bid price (current high + minimum raise) is strictly less than my private value and I can afford it; I bid exactly the minimum raise to keep price low.

When the current high bid is already at or above my private value, I pass.

When an opponent outbids me, I only counter if the new required bid remains below my private value and I still expect positive surplus; otherwise I concede.

When I'm leading a lot going into the final round, I do not bid further unless outbid and the new price is still below my private value.

When it's the final round for a lot and the price is below my private value, I'm willing to push up to my value (but not past it) because there are no future opportunities for that lot.

When choosing whether to contest a lot, prefer lots where (my value − current price) is large; avoid chasing lots with tiny positive surplus.

Never bid more than my private value for a lot.

Always check and subtract spent money from my remaining budget before making the next bid; never propose a bid that would exceed my remaining budget.

Avoid spending a large share of my budget early; reserve budget proportionally for expected remaining desirable lots (keep at least one decent-sized reserve for later high-value opportunities).

When opponents consistently outbid by large margins, stop matching their escalation—let them overpay and focus on cheaper wins.

If winning many low-surplus lots would exhaust budget and prevent acquiring higher-value lots later, prioritize conserving budget even if it means passing on modest positive-surplus bids.