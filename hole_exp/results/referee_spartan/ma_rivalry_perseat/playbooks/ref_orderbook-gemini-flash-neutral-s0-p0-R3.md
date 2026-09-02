---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2149
---
### Inventory & Target Management
- My overriding mandate is to reach exactly +3 position (or the stated delivery requirement) before settlement at the lowest possible volume-weighted average price.
- Once the delivery requirement is met (0 units left to acquire), submit `[cancel: all] [order: none]` for all remaining ticks. Never over-accumulate or trade speculatively past the requirement.
- Only order the exact quantity needed to complete delivery (`remaining_units = target - current_position`).

### Price Dynamics & Valuation
- Initial midpoint (e.g. ~47–51) indicates approximate fair value. Other traders regularly create a buying frenzy in ticks 2–3 (pushing bids/asks to 57–60) before supply mean-reverts back down in ticks 5–6 (often dropping to 49–53).
- Chasing prices at 58–60 during ticks 2–5 wipes out PnL (yielding +0.0 score). Buying near 55–56 in mid-ticks or catching 49–51 in late ticks yields consistent profits (+2.0 to +3.0).

### Execution Strategy by Tick
- **Tick 1**:
  - Post an inside bid (`[order: buy 3 @ best_bid + 1]`) to capture early liquidity inside the spread before the squeeze.
- **Ticks 2–3**:
  - Do NOT chase market asks into 57–60.
  - Reposition bids competitively near 54–55 (`[cancel: all] [order: buy N @ 55]`) to capture matching asks from aggressive traders without crossing at the top.
  - Always prepend `[cancel: all]` when updating orders.
- **Ticks 4–5**:
  - If still holding 0 or partial position: take available asks at 55–57 if supply is matching your bid, but avoid paying 59–60.
  - Watch for late-game selloffs where asks drop back to 49–51; cross immediately when these cheap asks appear to fill the rest of the quota.
- **Tick 6**:
  - If any delivery requirement remains, take the best available ask immediately to avoid the -8 per unit shortfall penalty.
  - If requirement is fully satisfied, strictly `[cancel: all] [order: none]`.

### What Does Not Work
- Panic-buying at 58–60 on ticks 4–5 when waiting one tick allows buying at 49–53 or filling passively at 55–56.
- Leaving stale orders resting across ticks without `[cancel: all]`.
- Over-buying beyond the +3 requirement.