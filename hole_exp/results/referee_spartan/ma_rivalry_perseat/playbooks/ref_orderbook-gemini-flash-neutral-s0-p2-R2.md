---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1819
---
# Playbook: Ref Orderbook Delivery Execution

- **Avoid chasing the squeeze in early-middle ticks**: The market often exhibits an early price spike around Ticks 2–3 (as competing buyers rush) followed by asks dropping significantly in Ticks 4–6 (from ~61 down to ~53–56). Do not bid up to inflated prices (e.g., 60+) on Ticks 2–3 just because the ask side is thin.
- **When asks exist and I still need units**:
  - If the ask is reasonably priced or late in the game (Ticks 4–6), cross the spread and buy immediately with `[order: buy N @ AskPrice]`.
  - In early ticks (Ticks 2–3), only take asks if they are not grossly inflated above initial trade levels; if asks are heavily marked up, do not chase them all at once.
- **When no asks exist (empty ask side) and I still need units**:
  - Always include `[cancel: all]` before posting a new order to avoid stacking stale quotes.
  - On Tick 1, post a bid at `BestBid + 1` to establish queue priority.
  - On Ticks 2–3, do not aggressively overbid competitors into a bubble; post competitive but disciplined bids rather than bidding above recent inflated tape prints.
- **Always cancel resting orders when modifying or crossing**: Ensure `[cancel: all]` is used whenever posting a new bid or taking an ask to ensure old resting bids do not execute unexpectedly as the market softens.
- **Do not sell out of delivery requirements**: Once any delivery units are acquired, never post a sell order. The shortfall penalty (8/unit) and repurchasing friction far outweigh any marginal spread capture.
- **Once delivery requirement is satisfied (+3 position)**:
  - Immediately clear any open resting bids with `[cancel: all] [order: none]` to prevent over-buying beyond cash constraints.
  - Submit `[cancel: all] [order: none]` on all remaining ticks until final settlement.