---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 2115
---
# Order Book Playbook

## Core Strategy & Objective
- My objective is to acquire the required delivery target at the lowest possible total cost while strictly avoiding the shortfall penalty (8 per unit short).
- Always include `[cancel: all]` before issuing any new order whenever I have resting orders out to prevent accidental double-fills or over-accumulation.

## Tick 1: Opening
- When Tick 1 opens, place a passive buy order inside the spread at `best_bid + 1` for the full target quantity: `[order: buy target @ best_bid + 1]`.
- Do not cross the spread immediately on Tick 1 unless the ask is unusually cheap.

## Ticks 2–4: Accumulation & Liquidity Taking
- On Tick 2, check if aggressive bidders have arrived (bids jumping substantially above opening levels):
  - When aggressive buyer demand is present, cross the spread immediately to fill the entire remaining delivery obligation across available ask tiers: `[cancel: all] [order: buy remaining @ ask_covering_depth]`.
  - Taking both the best ask and the second ask level on Tick 2 locks in inventory before prices drift higher or liquidity disappears.
- If units are still needed on Ticks 3–4:
  - If the spread is wide and prices are quiet, post an improved bid inside the spread (`best_bid + 1`) to capture a passive fill.
  - If bids continue climbing or asks thin out, cross the spread immediately (`[cancel: all] [order: buy remaining @ best_ask]`) to secure inventory.

## Ticks 5–6: Delivery Completion & Inventory Clean-up
- If any required delivery units remain unacquired by Tick 5, cross the spread immediately without hesitation: `[cancel: all] [order: buy shortfall @ best_ask]` to ensure zero delivery shortfall penalty.
- Once the target delivery quantity is reached (`remaining == 0`):
  - Immediately cancel all resting orders and take no further action: `[cancel: all] [order: none]`.
  - Maintain `[cancel: all] [order: none]` on all subsequent ticks through Tick 6.
  - If an accidental over-fill occurs (position > target), sell the excess inventory immediately into the best bid: `[cancel: all] [order: sell excess @ best_bid]`.