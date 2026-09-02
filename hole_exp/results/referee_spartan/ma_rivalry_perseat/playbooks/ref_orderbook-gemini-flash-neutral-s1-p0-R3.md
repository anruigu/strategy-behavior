---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1188
---
- On tick 1, immediately take the resting ask by placing a buy order matching the best ask price for available inventory (e.g. 2 units) when ask liquidity is available, securing base inventory early before prices rise.
- While still needing units for delivery in early ticks (ticks 1–3), aggressively cross the spread at the best available ask instead of posting passive bids, because competing traders sweep liquidity and push prices higher.
- Size buy orders strictly to the remaining delivery shortfall, never ordering more units than needed to reach the exact delivery target (e.g. buy 2 on tick 1, then buy the remaining 1 on tick 2).
- Whenever submitting a subsequent buy order or changing targets, include `[cancel: all]` so stale resting orders do not unexpectedly fill or double-fill.
- Never place passive bids in the spread during early accumulation ticks that risk being left unfilled or resulting in over-accumulation.
- Once the delivery obligation is completely met (remaining units to acquire is 0), immediately pull all resting orders with `[cancel: all]` and output `[order: none]` on every subsequent tick through tick 6 to lock in the position and avoid over-trading.