---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1581
---
# Playbook: Ref Orderbook Delivery

### 1. Delivery & Aggressiveness Rules
- When the episode starts (Tick 1), immediately lift the best available ask up to the available size or delivery requirement (`[order: buy N @ best_ask]`). Never post passive bids at Tick 1; other participants consistently bid prices up on subsequent ticks.
- When 1 unit remains to satisfy delivery (Tick 2 onwards), immediately cross the spread and buy the required remaining unit(s) at the current best ask (`[order: buy N @ best_ask]`). Completing the entire required delivery position by Tick 2 eliminates all book drift, shortfall penalty risk, and execution risk.
- Do not attempt passive fills or wait for late-tick price pullbacks; securing early fills prevents being locked out by aggressive competing bids.

### 2. Position Management & Halting
- Once `Delivery: 0 of N units still to acquire` is reached (target position met), immediately halt all trading activity for the remainder of the episode.
- On every tick once delivery is fully satisfied, send `[cancel: all] [order: none]` to guarantee no resting orders execute and alter the position.
- Never sell units once accumulated toward the delivery target, as shortfall penalties (-8 per missing unit) far exceed any potential spread-capturing gains.

### 3. Order Sizing & Pricing
- Match buy order quantities strictly to `min(remaining_units_needed, available_depth_at_best_ask)`.
- When crossing the spread to take liquidity, set the limit price equal to the best ask price (`P = best_ask`). Always verify remaining cash exceeds `N * P`.