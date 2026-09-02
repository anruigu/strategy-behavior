---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1688
---
# Order Book Delivery Playbook

- When I have units remaining to acquire and there are resting asks within my cash budget, I take them immediately up to the exact quantity needed using `[order: buy N @ P] [cancel: all]` at the best ask price.
- When crossing the spread where the resting ask size is smaller than my remaining delivery need, I only buy the quantity currently available on the ask (e.g., if 2 are offered at 58 and I need 3, send `[order: buy 2 @ 58] [cancel: all]`), avoiding over-bidding beyond the ask depth to prevent leaving an expensive resting bid that gets adversely selected when prices drop in later ticks.
- When I have units remaining to acquire and there are no resting asks, I post a buy order `[order: buy N @ P]` at or one tick above the current best bid to maintain priority, never bidding more units than I currently need and never exceeding my available cash budget.
- Whenever I place an aggressive buy or cross the spread to acquire inventory, I always include `[cancel: all]` (e.g., `[order: buy N @ P] [cancel: all]`) to pull any previous resting bids and prevent unwanted fills.
- Once my target delivery position is reached (0 units remaining to acquire), I immediately cancel all resting orders and stop trading: I reply with `[order: none] [cancel: all]` on all remaining ticks.
- I do not sell down my position after meeting the delivery requirement; holding the exact required units at settlement avoids shortfall penalties and unnecessary transaction costs.
- If an accidental execution leaves me with an excess position above target on later ticks, I sell only the excess units into the best bid to return exactly to the delivery requirement.