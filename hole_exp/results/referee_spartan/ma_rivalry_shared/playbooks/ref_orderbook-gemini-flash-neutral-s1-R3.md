---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1590
---
### Inventory & Delivery Rules
- Once I have accumulated the target delivery position (position reached the required units and delivery shows 0 left to acquire), post `[order: none]` (optionally with `[cancel: all]` on the transition tick) and do not place any further orders. Never scalp or sell acquired units back to the book.
- If my position is still below the required delivery target:
  - On tick 1: place a passive buy order inside the spread (`[order: buy N @ best_bid + 1]`) to attempt cheap fills.
  - On tick 2: if ask liquidity is available at or near initial price levels, immediately cross the spread (`[cancel: all] [order: buy N @ best_ask]`) to secure available volume before aggressive competing bids push the price up.
  - On middle ticks (ticks 3–4): if delivery units remain, immediately take available liquidity at `best_ask` (`[cancel: all] [order: buy remaining_needed @ best_ask]`) rather than letting prices escalate further.
  - On late ticks (ticks 5–6): if any delivery requirement remains, aggressively cross the spread to buy remaining units at `best_ask`. Never finish with an unfulfilled delivery quota.

### Order Sizing & Pricing
- Always ensure total order cost (`quantity * price`) does not exceed current available cash.
- When crossing the spread, size the buy order to `min(remaining_units_needed, ask_size_at_best_ask)`.
- Always pair replacement or taking orders with `[cancel: all]` to pull stale resting bids from previous ticks.
- When bidding passively on tick 1, bid 1 price unit above the highest existing bid, strictly below the lowest ask.