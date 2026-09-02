---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 2268
---
### Tick 1: Opening Execution
- If asks are posted near or below the average budget (~55–60) on Tick 1, lift them immediately to secure inventory using `[order: buy N @ best_ask]`.
- If the ask side is empty on Tick 1, post an aggressive bid 1 tick above the existing best bid (`[order: buy 3 @ (best_bid + 1)]`) to capture queue priority before other traders step in front.

### Ticks 2–3: Building Core Delivery Position
- When units remain to be acquired and asks are posted at reasonable prices (~57–60), lift the asks aggressively using `[cancel: all] [order: buy N @ best_ask]` to ensure delivery requirements are satisfied early and reliably.
- If asks are absent or prohibitively high, cancel resting orders and step 1 tick above the best resting bid (`[cancel: all] [order: buy N @ (best_bid + 1)]`).
- Always prepend `[cancel: all]` when issuing new buy orders to release any cash tied up in resting passive bids.

### Ticks 4–5: Scalping & Re-balancing
- Once at +3 units, look for predictable late-game price declines (prices drop from peak levels of ~58–60 down toward settlement around ~50–53).
- On Tick 4: If holding +3 units and bids remain elevated (e.g. >= 58), sell 1 unit into the best bid (`[order: sell 1 @ best_bid]`). This frees cash and positions for a cheap repurchase on Tick 5.
- On Tick 5:
  - If holding +2 units (after a Tick 4 sale), immediately lift the best ask at the newly depressed prices (~50–53) using `[cancel: all] [order: buy 1 @ best_ask]` to lock in the scalp profit and return to the required +3 units before the final tick.
  - If already holding +3 units on Tick 5 and an crossed/wide spread appears (e.g., bids >= 55, asks <= 51), sell 1 unit into the bid (`[order: sell 1 @ best_bid]`) only if confident in lifting on Tick 6, but prefer executing the roundtrip on Ticks 4->5 to avoid leaving fulfillment to the final tick.

### Tick 6: Final Settlement Protection
- Never speculate or sell inventory on Tick 6.
- If position is exactly +3 units, maintain the delivery requirement and take no action: output `[order: none]`.
- If position is short of +3 units for any reason, immediately lift the best available ask to complete delivery and avoid the severe shortfall penalty: `[cancel: all] [order: buy N @ best_ask]`.