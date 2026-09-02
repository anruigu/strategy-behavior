---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1178
---
- On tick 1, immediately take the resting ask or place a buy order matching the best ask price for at least 2 units if the ask price is cheap relative to initial cash, rather than pennying inside the spread and getting left behind.
- When resting bids exist that I previously posted, always include `[cancel: all]` whenever I cross the ask or change target prices, so stale bids do not unexpectedly fill later and cause over-buying.
- When behind on delivery schedule (ticks 1–3), aggressively cross the spread at the best ask instead of attempting to make a market with passive bids, because other traders will take liquidity and push prices up.
- When buying, size the order to only what is needed to reach exactly the required delivery target (e.g., if needing 3, buy 2 then 1, or 3 if available), never exceeding the target position.
- Once the delivery obligation is completely met (remaining units to acquire is 0), immediately pull all resting orders with `[cancel: all]` and output `[order: none]` for the remainder of the episode.
- Never place passive bids in the middle of a rising market that might sit on the book and double-fill alongside aggressive market orders.