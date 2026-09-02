---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1715
---
# Playbook: Ref Orderbook Delivery

### 1. Delivery & Aggressiveness Rules
- When the episode starts (Tick 1), immediately lift the best available ask up to the available size or delivery requirement (`[order: buy N @ best_ask]`). Never post passive bids at Tick 1; other participants consistently bid prices up on subsequent ticks.
- When 1 unit remains to satisfy delivery (Tick 2 onwards), immediately cross the spread and buy 1 unit at the current best ask (`[order: buy 1 @ best_ask]`). Completing the entire 3-unit position by Tick 2 eliminates all book drift and execution risk.
- Do not attempt passive fills or wait for better prices; the shortfall penalty and price escalation across ticks make immediate liquidity taking optimal.

### 2. Position Management & Halting
- Once `Delivery: 0 of 3 units still to acquire` is reached (position +3), immediately halt all trading activity for the remainder of the episode.
- On the first tick after acquiring full delivery, include `[cancel: all]` alongside `[order: none]` (i.e. `[cancel: all] [order: none]`) to clear any unintended resting orders.
- On all subsequent ticks once delivery is satisfied, maintain zero activity with `[cancel: all] [order: none]` or `[order: none]`.
- Never sell units once accumulated toward the delivery target, as shortfall penalties far exceed any short-term resale profit.

### 3. Order Sizing & Pricing
- Match order quantities strictly to the remaining units needed or the available depth at the top ask (e.g., `[order: buy 2 @ best_ask]` on Tick 1 when 2 units are offered).
- When crossing the spread to buy, set the limit price equal to the best ask price (`P = best_ask`). Always verify remaining cash exceeds `N * P`.