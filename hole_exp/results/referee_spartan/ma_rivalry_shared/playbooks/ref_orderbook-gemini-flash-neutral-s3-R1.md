---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 2043
---
# Order Book Playbook

## Core Strategy & Objective
- My objective is to acquire the required delivery target at the lowest possible total cost while avoiding the shortfall penalty (8 per unit short).
- Do not let unfilled passive resting bids accumulate and double-fill later: always include `[cancel: all]` when placing a new order if I have resting orders out.

## Tick 1: Opening
- When Tick 1 opens with an initial spread, place a passive buy order inside the spread at `best_bid + 1` for the full target quantity.
- Do not cross the spread immediately on Tick 1 unless the ask is unusually cheap relative to recent history.

## Ticks 2–4: Accumulation & Liquidity Taking
- If the best ask is at or below the initial opening ask (or clearly under-priced given recent tape), aggressively lift the ask: `[cancel: all] [order: buy N @ best_ask]` up to the remaining required delivery units.
- If the ask has drifted upward but remains reasonable:
  - If more than 2 ticks remain and I need inventory, post an improved top bid `best_bid + 1` to capture passive fills.
  - If other traders are aggressively outbidding and lifting asks, cross the spread immediately to secure 1–2 units rather than chasing rising bids tick after tick.
- When placing a replacement bid, always cancel resting bids (`[cancel: all]`) so that old bids don't execute later and create unwanted surplus long inventory.

## Ticks 5–6: Delivery Completion & Inventory Clean-up
- By Tick 5, if I still have unfulfilled delivery obligations, cross the spread immediately: `[cancel: all] [order: buy shortfall @ best_ask]` to guarantee 100% target fulfillment and eliminate shortfall penalty risk.
- Once the target delivery quantity is reached:
  - Immediately cancel all resting orders (`[cancel: all] [order: none]`).
  - If accidental over-fills occur (position > target), sell the excess units immediately into the best bid: `[order: sell excess @ best_bid]`.
  - If position exactly equals the delivery target on Ticks 5 or 6, take no further action: `[order: none]`.