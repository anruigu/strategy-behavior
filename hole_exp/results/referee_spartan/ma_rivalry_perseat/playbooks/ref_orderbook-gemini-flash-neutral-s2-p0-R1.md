---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1538
---
# Playbook: Ref Orderbook Delivery

### 1. Delivery & Aggressiveness Rules
- When the episode starts (Tick 1) and a tight spread exists, lift the best ask immediately if the price is low (sub-50s) rather than posting passive bids inside the spread. Resting passive bids in early ticks repeatedly fails to fill and allows other traders to push prices higher.
- When resting on 0 position at Tick 2 or Tick 3, take available ask liquidity immediately up to the delivery requirement or available book depth. Do not post limit bids between the spread; crossing the spread early secures low prices before book drift.
- When 1 unit remains to satisfy delivery, lift the lowest ask immediately unless there are at least 3 ticks remaining and a resting bid is already active at the top of the book. Never wait past Tick 4 to secure the final delivery unit.

### 2. Position Management & Halting
- When `Delivery: 0 of 3 units still to acquire` (position is fully met), reply with `[order: none]` and pull any leftover resting orders if present. Do not speculate or trade beyond the required delivery target.
- Never sell units once accumulated toward the delivery target, as the shortfall penalty per missing unit outweighs marginal trading gains.

### 3. Order Sizing & Pricing
- Match order quantities directly to the remaining units needed or the exact size of the target level on the ask side (e.g., `[order: buy 2 @ P]` when 2 are offered and needed).
- If crossing the spread, set price exactly equal to the best ask price (`P = best_ask`).