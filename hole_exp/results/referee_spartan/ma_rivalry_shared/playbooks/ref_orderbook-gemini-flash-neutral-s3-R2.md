---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 2167
---
# Order Book Playbook

## Core Strategy & Objective
- My objective is to acquire the required delivery target at the lowest possible total cost while strictly avoiding the shortfall penalty (8 per unit short).
- Always include `[cancel: all]` before issuing any new order whenever I have resting orders out to prevent accidental double-fills or over-accumulation.

## Tick 1: Opening
- When Tick 1 opens, place a passive buy order inside the spread at `best_bid + 1` for the full target quantity: `[order: buy target @ best_bid + 1]`.
- Do not cross the spread immediately on Tick 1 unless the ask is unusually cheap.

## Ticks 2–4: Accumulation & Liquidity Taking
- On Tick 2, if the best ask is at or near the opening ask level, lift liquidity aggressively:
  - If the ask depth covers all remaining needed units, cross at that price: `[cancel: all] [order: buy remaining @ best_ask]`.
  - If the ask depth at the lowest price is less than the remaining required units, either take the available depth at `best_ask` or cross up to the second ask tier if the price remains attractive to secure the full target immediately.
- On Ticks 3–4, if units are still needed:
  - If the spread is wide and tape has stabilized, post an improved bid inside the spread (`best_bid + 1` or `best_ask - 1`) to capture a passive fill.
  - If asks are thin or other participants are aggressively bidding up the market, cross the spread immediately (`[cancel: all] [order: buy remaining @ best_ask]`) to lock in inventory and avoid chasing prices higher.

## Ticks 5–6: Delivery Completion & Inventory Clean-up
- If any required delivery units remain unacquired by Tick 4 or 5, cross the spread without hesitation: `[cancel: all] [order: buy shortfall @ best_ask]` to ensure zero penalty shortfall.
- Once the target delivery quantity is reached (`remaining == 0`):
  - Immediately pull all resting orders: `[cancel: all] [order: none]`.
  - Maintain `[cancel: all] [order: none]` on all subsequent ticks through Tick 6.
  - If an accidental over-fill occurs (position > target), sell the excess inventory immediately into the best bid: `[cancel: all] [order: sell excess @ best_bid]`.