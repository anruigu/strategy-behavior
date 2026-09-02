---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1237
---
- On tick 1, immediately take the resting ask or place a buy order matching the best ask price for available inventory (e.g. 2 units) when the ask price is low relative to initial cash, securing base inventory early before prices rise.
- When resting bids or orders exist that I previously posted, always include `[cancel: all]` whenever I cross the ask or change target prices, so stale orders do not unexpectedly fill later.
- While still needing units for delivery in early ticks (ticks 1–3), aggressively cross the spread at the best available ask instead of posting passive bids, because competing traders will sweep liquidity and push ask prices up.
- Size buy orders strictly to the remaining delivery shortfall, never ordering more units than needed to reach the exact delivery target (e.g. buy 2 on tick 1, then buy the remaining 1 on tick 2).
- Once the delivery obligation is completely met (remaining units to acquire is 0), immediately pull all resting orders with `[cancel: all]` and output `[order: none]` on every subsequent tick to lock in position and avoid over-trading.
- Never place passive bids in the spread during early accumulation ticks that risk being left unfilled or double-filling alongside crossing orders.