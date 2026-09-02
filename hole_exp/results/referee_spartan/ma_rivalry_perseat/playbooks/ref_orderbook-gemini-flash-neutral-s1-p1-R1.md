---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1796
---
### Tick 1: Opening Execution
- When the market opens on Tick 1 with asks available near or below the average budget, immediately lift the available asks to secure the initial base (up to the required delivery size) using `[order: buy N @ P]`.
- Do not post a passive bid inside the spread on Tick 1 hoping for fills; other traders will lift the cheap asks immediately, leaving me chasing higher prices later.

### Ticks 2–4: Completing the Delivery Obligation
- When I still have units left to acquire and an ask is available at an acceptable price within my remaining cash, lift the ask immediately (`[order: buy N @ P]`).
- When the ask side is empty or spreads are wide, post a competitive bid 1 tick above the current best bid (`[order: buy N @ (best_bid + 1)]`) to gain queue priority and draw liquidity before prices rise.
- Always include `[cancel: all]` before posting a new aggressive buy order if I have resting bids that were stepped in front of.

### Ticks 4–6: Trading Inventory & Delivery Management
- When I have reached my required delivery position (+3) and there are ticks remaining before the final tick:
  - If bids exist above my average acquisition cost and there is sufficient ask liquidity/time to buy back later at a discount, sell 1 or 2 units into the bid (`[order: sell N @ best_bid]`) to monetize price spikes.
  - If the spread is flat or prices are trending higher, do not speculate; maintain the delivery requirement and hold.
- When I sell down below the delivery requirement on intermediate ticks, aggressively lift resting asks on Tick 5 or Tick 6 (`[order: buy N @ best_ask]`) to ensure the final holding is exactly 3 units at settlement. Never end with a delivery shortfall.
- When the delivery requirement of 3 units is met on Tick 6, reply `[order: none]`.