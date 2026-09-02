---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1479
---
### Inventory & Delivery Rules
- Once I have accumulated the target delivery position (e.g., position reached the required units and delivery shows 0 left to acquire), I will post `[order: none]` and do not place any sell orders. Never scalp or sell acquired units back to the bid to "realize gains" — it incurs unnecessary spread crossing and transaction friction when buying them back.
- If my position is still below the required delivery target:
  - On early ticks (ticks 1–2): place a buy order inside the spread or at top-of-book (`[order: buy N @ best_bid + 1]`) to attempt passive fills. Always pair new bid adjustments with `[cancel: all]` if replacing an unfilled resting order.
  - On middle ticks (ticks 3–4): if passive bids are being stepped over and not filling, take liquidity directly by crossing the spread (`[order: buy N @ best_ask]`) to acquire available units before asks step up.
  - On late ticks (ticks 5–6): if any delivery requirement remains, immediately cross the spread and sweep the asks up to available cash (`[order: buy remaining_units @ best_ask]`). Never end with an unfilled shortfall.

### Order Sizing & Pricing
- Do not place buy orders that exceed remaining cash.
- When crossing the spread to fulfill inventory, buy the exact quantity needed to reach the target delivery quota at the lowest available ask price level.
- When bidding passively, bid 1 tick above the existing highest bid, provided it remains strictly below the lowest ask.