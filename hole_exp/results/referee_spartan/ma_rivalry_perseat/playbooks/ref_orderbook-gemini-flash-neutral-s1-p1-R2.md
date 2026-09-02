---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1689
---
### Tick 1: Opening Execution
- If asks are posted near or below the average budget on Tick 1, lift them immediately to secure inventory using `[order: buy N @ P]`.
- If the ask side is empty on Tick 1, post an aggressive bid 1 tick above the existing best bid (`[order: buy 3 @ (best_bid + 1)]`) to capture queue priority before other traders step in front.

### Ticks 2–4: Building Delivery Position
- When units remain to be acquired and asks are posted at or below budget (~57–60), lift the asks aggressively using `[cancel: all] [order: buy N @ best_ask]` to ensure delivery requirements are satisfied early.
- If asks are absent or prohibitively high, cancel resting orders and post a bid 1 tick above the best resting bid (`[cancel: all] [order: buy N @ (best_bid + 1)]`).
- Always include `[cancel: all]` when switching from passive bidding to aggressive lifting to free up committed cash.

### Ticks 5–6: Late-Game Strategy & Settlement
- Notice price dynamics across later ticks: ask prices tend to drop toward true settlement value (often falling from ~58 to ~50–52 by Tick 5/6).
- If I hold +3 units and see high bids in Ticks 4–5 while lower asks exist or are likely to appear on the tape, evaluate selling 1 unit into the high bid (`[order: sell 1 @ best_bid]`) and immediately re-buying cheaper on Tick 5 or 6 (`[order: buy 1 @ best_ask]`) to capture margin and reduce net position cost.
- Do not speculate on Tick 6: on the final tick, ensure holding exactly +3 units to avoid the shortfall penalty (8 per unit). If position is exactly +3, output `[order: none]`. If short of 3 on Tick 6, immediately lift the best available ask (`[cancel: all] [order: buy N @ best_ask]`).