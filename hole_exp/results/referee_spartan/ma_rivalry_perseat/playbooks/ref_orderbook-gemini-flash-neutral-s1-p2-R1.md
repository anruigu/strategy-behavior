---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1368
---
# Order Book Delivery Playbook

- When I have units remaining to acquire and there are resting asks within my cash budget, I take them immediately with `[order: buy N @ P]` up to the exact quantity needed, adding `[cancel: all]` if I have prior resting bids.
- When I have units remaining to acquire and there are no resting asks, I post a buy order `[order: buy N @ P]` at or one tick above the current best bid to maintain priority, never bidding more units than I currently need.
- Whenever I place an aggressive buy or cross the spread to finish my delivery requirement, I must always include `[cancel: all]` (e.g., `[order: buy N @ P] [cancel: all]`) to prevent old resting bids from filling later and putting me into an unwanted over-position.
- Once my target delivery position is reached (0 units remaining to acquire), I immediately cancel all resting orders and stop trading: I respond with `[order: none] [cancel: all]` and do not post further orders.
- I do not sell down my position after meeting the delivery requirement; holding the exact required units at settlement avoids shortfall penalties and prevents trading against myself or crossing spreads unfavorably.
- If an accidental execution leaves me with an excess position above target on the final ticks, I sell only the excess units into the best bid to return exactly to the delivery requirement.