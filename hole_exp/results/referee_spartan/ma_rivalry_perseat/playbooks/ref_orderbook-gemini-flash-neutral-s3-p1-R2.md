---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1928
---
# Ref Orderbook Playbook

## Early Ticks (Ticks 1–2): Secure Inventory Aggressively at Opening Prices
- When Tick 1 opens with resting asks close to the initial bid level, cross the spread immediately and lift the ask up to the required delivery target (`[order: buy N @ Ask]`). Other market participants systematically bid prices up in later ticks, making early market buys far cheaper than later fills.
- On Tick 2, if 1 unit is still required and there are no resting asks, place an aggressive inside bid 1 unit above the top resting bid (`[cancel: all] [order: buy 1 @ BestBid+1]`).

## Managing Resting Orders & Order Tracking
- When transitioning from posting passive bids to crossing the spread (taking an ask), always prepend `[cancel: all]` to the buy order (`[cancel: all] [order: buy N @ Ask]`) to prevent stale resting bids from matching and creating unwanted excess inventory.
- If an unexpected fill pushes total position above the required delivery target (position > required delivery units), sell the exact excess quantity immediately at the best bid (`[order: sell (position - required) @ BestBid]`).

## Mid-to-Late Ticks (Ticks 3–5): Fulfilling Remaining Delivery
- When still short of the delivery requirement on Tick 3 or later, immediately cross the spread and buy all remaining required units from the best ask (`[cancel: all] [order: buy N @ BestAsk]`). Do not wait until Ticks 5–6 to secure delivery.
- Once the delivery requirement is met and the position exactly matches the target, output `[order: none]` and sit out all subsequent ticks.

## Final Tick (Tick 6): Settlement & Rebalancing
- When holding exactly the required delivery target at Tick 6, output `[order: none]` and hold into settlement.
- When holding more than the required delivery units at Tick 6, sell all excess units into the highest resting bid (`[order: sell excess @ BestBid]`) to monetize surplus inventory before settlement.