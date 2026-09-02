---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1845
---
# Ref Orderbook Playbook

## Early Ticks (Ticks 1–2): Secure Inventory Aggressively at Opening Prices
- When Tick 1 opens with resting asks close to the initial bid level, cross the spread immediately and lift the ask up to the quantity needed (`[order: buy N @ Ask]`). Do not post passive inside bids on Tick 1; other market participants systematically lift prices in later ticks, making early market buys far cheaper than later fills.
- When resting asks are available below the mid-50s on early ticks, take them immediately rather than trying to penny the book.

## Managing Resting Orders & Order Tracking
- When transitioning from posting passive bids to crossing the spread (taking an ask), always include `[cancel: all]` with the market order to avoid accidental double-buys from forgotten resting bids getting filled later.
- If a resting bid gets filled unexpectedly and pushes the position above the target delivery requirement (e.g., position > required delivery units), sell the exact excess quantity immediately at the best bid (`[order: sell (position - required) @ BestBid]`).

## Mid-to-Late Ticks (Ticks 3–5): Fulfilling Remaining Delivery
- When still short of the delivery requirement with 3 or fewer ticks remaining, cross the spread and buy all remaining required units directly from the best ask. Do not wait for Tick 6 to finish buying.
- When the delivery requirement is met and holding exactly the required position, output `[order: none]` and do not post any additional orders.

## Final Tick (Tick 6): Position Rebalancing
- When holding exactly the required delivery target at Tick 6, post `[order: none]` and let the contract settle.
- When holding more than the required delivery units at Tick 6, hit the highest resting bid for all excess units (`[order: sell excess @ BestBid]`) to lock in cash before settlement.