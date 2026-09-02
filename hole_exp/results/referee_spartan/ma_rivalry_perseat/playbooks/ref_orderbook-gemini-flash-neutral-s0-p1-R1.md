---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1416
---
# Playbook: Mandatory Delivery Order Book

### Delivery & Execution Priority
- Never sell below the required delivery threshold (+3) once acquired. Once delivery is fulfilled, do not scalp or sell inventory if it leaves a shortfall to repurchase in later ticks.
- Early ticks (1–2) often have the lowest ask prices. Lift attractive early asks immediately (e.g., tick 1 ask crossing) rather than passively bidding inside wide spreads, because prices consistently drift upward across the 6 ticks.
- When passive bids do not get filled after one tick, cancel resting bids and aggressively take the lowest available asks before the tape runs away.

### Position Management
- When holding `< required units` and asks are available within cash budget:
  - If tick $\ge 3$ or prices are rising, cross the spread immediately by posting `[order: buy N @ ask_price]` for remaining needed units.
  - If tick 1 has a narrow spread and cheap ask, buy as much required inventory as available immediately.
- When holding `= required units`:
  - Output `[order: none]` or maintain resting passive sell orders strictly above current ask levels. Never execute market sell orders that drop position below the delivery target.
- On tick 6:
  - If any delivery units remain unacquired, execute a market buy against the best available ask immediately to avoid the shortfall penalty.
  - If delivery is already met, output `[order: none]`.