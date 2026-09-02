---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1313
---
# Execution Playbook

### 1. Delivery & Inventory Management
* When I have acquired all required delivery units (shortfall is 0 / 0 units still to acquire), immediately reply with `[order: none]` and sit out all remaining ticks.
* When short of the delivery target, prioritize acquiring the necessary units as early as possible (Ticks 1 and 2) to avoid shortfall penalties and trend escalation.

### 2. Early-Tick Aggressive Execution
* **Tick 1**: Immediately cross the spread and lift the best ask for the maximum available volume up to the delivery requirement (typically `[order: buy 2 @ best_ask]`).
* **Tick 2**: If delivery units remain to be acquired, immediately lift the best ask for the remaining deficit (typically `[order: buy 1 @ best_ask]`) to fully close the delivery obligation.
* Avoid resting passive bids on early ticks; market dynamics push prices upward across ticks, causing passive bids to miss execution and resulting in worse fills later.
* Never carry an unfulfilled delivery deficit past Tick 2 or 3.

### 3. Order Sizing and Safety
* Always size buy orders to `min(remaining_delivery_units, ask_volume, available_cash // best_ask_price)`.
* Do not trade, speculate, or buy excess inventory once the delivery target is met; preserve cash and maintain exact required delivery inventory.