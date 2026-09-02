---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2127
---
# Playbook: Ref Orderbook Delivery Execution

- **Avoid chasing the squeeze in early ticks (Ticks 2–3)**: The market often exhibits an early price spike around Ticks 2–3 (as competing buyers rush) followed by asks dropping significantly in Ticks 4–6 (often dropping below 52). Do not chase asks or post high aggressive bids at 58+ in early rounds; buying too high in Ticks 2–3 severely hurts settlement PnL.
- **Pacing unit acquisition across ticks**:
  - Do not rush to buy all 3 units immediately in Ticks 2–3 if prices are elevated. Acquiring 1 unit early is fine to hedge shortfall risk, but leave remaining capacity for Ticks 4–6 where cheaper liquidity reliably appears.
  - In Ticks 4–6, aggressively cross the spread (`[order: buy N @ AskPrice]`) to fill any remaining shortfall on declining ask prices (e.g. <= 56).
- **When asks exist and I still need units**:
  - In early ticks (Ticks 2–3), only take at most 1 unit if the ask is somewhat elevated (57–58); do not take multiple units at peak prices (58–60).
  - In later ticks (Ticks 4–6), lift all remaining required units across available asks whenever prices soften.
- **When no asks exist (empty ask side) and I still need units**:
  - Always include `[cancel: all]` before posting a new order to avoid stacking stale quotes.
  - On Tick 1, post a bid at `BestBid + 1` for the full required quantity to establish priority.
  - On Ticks 2–3, do not aggressively leapfrog high competitor bids; post disciplined bids rather than bidding into a bubble.
- **Always cancel resting orders on every turn**: Always use `[cancel: all]` before every order submission to prevent stale resting bids from matching unexpectedly as market prices collapse late in the game.
- **Never sell delivery units**: Once delivery units are acquired, never post sell orders. Shortfall penalties (8/unit) and rebuying risk outweigh marginal gains.
- **Once delivery requirement is satisfied (+3 position)**:
  - Immediately post `[cancel: all] [order: none]`.
  - Submit `[cancel: all] [order: none]` on every remaining tick until settlement to prevent unintended execution and cash drain.