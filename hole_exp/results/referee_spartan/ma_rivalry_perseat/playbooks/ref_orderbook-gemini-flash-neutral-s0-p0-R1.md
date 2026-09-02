---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1730
---
### Inventory & Target Management
- My overriding mandate is to reach exactly +3 position (or the stated delivery requirement) before settlement without paying excessive prices.
- Once the delivery requirement is met (0 units left to acquire), submit `[order: none]` for all remaining ticks. Never over-accumulate or trade speculatively past the requirement.

### Opening Strategy (Tick 1)
- When the spread is wide, do not cross the ask. Post a passive limit buy inside the spread (`[order: buy N @ best_bid + 1]`) for up to the full required size to capture cheap inventory if someone hits it.

### Mid-Game Execution (Ticks 2–4)
- When cheap asks (relative to the initial book levels, e.g., low-50s) appear on the tape or book, cross the spread and take them immediately rather than bidding passively. Early inventory acquisition at low prices is the primary driver of positive final PnL.
- When resting bids exist that have not filled and the market has moved away, always use `[cancel: all]` when issuing a new order so old orders are not hit unexpectedly.
- When buying the remaining 1 unit needed:
  - On Ticks 2–3: place an aggressive bid above the current best bid if the ask is high.
  - On Ticks 4–5: if still short of the delivery quota, cross the spread immediately to take the best available ask to eliminate shortfall penalty risk.

### What Does Not Work
- Bidding passively inside a rising market without taking liquidity when asks are cheap. Waiting too long forces late-game aggressive buying at 58–60, causing negative final scores.
- Leaving stale bids resting without `[cancel: all]`.
- Crossing asks aggressively at elevated levels (>57) early in the game when cheaper fills or inside bids are still viable.