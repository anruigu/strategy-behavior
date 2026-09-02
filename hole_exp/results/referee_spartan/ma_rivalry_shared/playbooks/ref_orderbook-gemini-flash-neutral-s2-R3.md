---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 940
---
- On Tick 1, lift the available resting ask immediately (e.g., `[order: buy 2 @ ask]` or `[order: buy 3 @ ask]`) to secure inventory at the lowest prices before competing buyers drive the market up.
- On Tick 2, immediately buy the remaining required unit(s) by crossing the lowest available ask to lock in the full delivery target before further price inflation occurs.
- When buying to meet delivery requirements, take liquidity aggressively at the best available ask rather than posting passive bids inside the spread that risk non-execution and higher future prices.
- Once the delivery requirement is satisfied (units to acquire reaches 0 and position is at +3), reply `[order: none]` for all remaining ticks; do not take on excess inventory or trade speculatively.
- Always verify remaining delivery units and available cash before submitting orders, sizing buy orders to match exact delivery needs without exceeding cash constraints.