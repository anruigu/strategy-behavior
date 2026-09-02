---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1269
---
# Execution Playbook

### 1. Delivery & Inventory Management
* When I have acquired all required delivery units (e.g., position reaches delivery target and shortfall is 0), immediately reply with `[order: none]` and sit out all remaining ticks.
* When I am short of my delivery target, prioritize securing the needed units early to avoid shortfall penalties and rising prices.

### 2. Early-Tick Aggressive Execution
* On Tick 1, cross the spread immediately by lifting the full available liquidity at the best ask (typically `[order: buy 2 @ best_ask]`) to secure the majority of required inventory before prices escalate.
* On Tick 2, immediately buy the remaining deficit (typically `[order: buy 1 @ best_ask]`) to complete the entire delivery requirement by Tick 2 or Tick 3.
* Do not attempt passive bidding inside the spread during early ticks; competitor buying rapidly moves the market upward, leaving resting bids behind and forcing more expensive fills later.
* Never carry a delivery deficit into ticks 4–6.

### 3. Sizing and Risk Control
* When crossing the ask, size the order to min(available depth at ask, remaining delivery deficit, available cash // ask price).
* Do not overbuy beyond the delivery requirement unless clear structural edge is present.