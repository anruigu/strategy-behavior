---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1319
---
### Playbook

- **Always cancel resting orders when posting new ones**: Include `[cancel: all]` with every active order placement so stale bids do not get filled later and cause unintentional over-accumulation and negative cash balances.
- **Handling early empty ask books (Ticks 1–3)**:
  - When there are no asks on the book, post a competitive bid for 1 unit at `top_bid + 1` (or matching top trade price) to maintain top-of-book priority: `[cancel: all] [order: buy 1 @ best_bid + 1]`.
- **Acquire required units when asks appear**:
  - Whenever asks are present on the book and delivery is not yet satisfied, immediately lift from the lowest available ask: `[cancel: all] [order: buy N @ lowest_ask]`.
  - When asks offer attractive declining prices later in the round (Ticks 4–6), buy up to the full remaining delivery shortfall if sufficient size is available at the best price (e.g., `[cancel: all] [order: buy 2 @ lowest_ask]`).
- **Once the delivery obligation is met**:
  - Immediately send `[cancel: all] [order: none]`.
  - Do not trade further unless forced to offload accidental excess inventory.
- **Handling accidental overfill**:
  - If position exceeds the delivery requirement at any point, immediately sell excess units by hitting the best available bid: `[cancel: all] [order: sell N @ best_bid]`.