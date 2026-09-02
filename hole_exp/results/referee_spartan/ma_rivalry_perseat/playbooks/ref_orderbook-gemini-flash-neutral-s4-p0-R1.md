---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1995
---
# Delivery Obligation Playbook

## Goal & Target Position
- I must finish Tick 6 holding exactly the required delivery target (e.g., 3 units) to avoid the per-unit shortfall penalty.
- Once my position meets the delivery requirement, I immediately cancel resting orders and submit `[order: none]` for all remaining ticks. I do not speculate beyond my delivery obligation.

## Execution Rules by Phase

### Tick 1: Opening Spread
- When the book opens with a wide spread and prices are low relative to starting cash, post a buy order for 1–2 units priced 1 tick above the best bid to attempt capturing liquidity as a maker.
- Do not cross the spread at Tick 1 unless the ask is anomalously cheap relative to total cash budget.

### Ticks 2–3: Aggressive Core Accumulation
- If resting asks remain near the opening ask level while competing bids jump aggressively, do not wait on passive bids—cross the spread immediately and lift the best asks up to the quantity needed.
- If my passive bid from Tick 1 was unfilled and other traders bid higher, cancel resting orders and take available asks before prices run higher.

### Ticks 4–5: Filling the Final Units
- If I still need 1 unit to complete the delivery quota:
  - If the spread is narrow and an ask is within budget, cross the spread and buy immediately with `[order: buy 1 @ best_ask]` to lock in fulfillment.
  - If the ask is elevated, post a bid 1 tick above the highest competing bid (`best_bid + 1`), pairing with `[cancel: all]` if replacing an earlier resting bid.
  - By Tick 5, lift whatever best ask is available; never carry an unfulfilled delivery quota into Tick 6 relying on a passive bid.

### Tick 6: End Game
- If delivery is met: submit `[order: none]`.
- If still short: immediately hit the best ask at any available price to avoid the flat delivery shortfall penalty.

## Order Hygiene
- Always include `[cancel: all]` when replacing an existing resting order with a new price point to avoid accidental double execution.