---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 2111
---
# Order Book Delivery Playbook

- When I have units remaining to acquire and there are resting asks within my cash budget:
  - If the resting ask size is smaller than or equal to my remaining delivery need, I only cross the spread for the available ask quantity (e.g., if 2 are offered at 59 and I need 3, send `[order: buy 2 @ 59] [cancel: all]`). I never submit an order size larger than the ask depth to avoid leaving an expensive resting bid that gets filled at a loss when cheaper supply arrives later.
  - If the resting ask price is high (e.g., around tick 4 peak) and early cheap supply is likely in tick 5–6, I avoid overpaying on the full delivery need at once if I can wait, but I prioritize securing fills within budget before expiration.
- When I have units remaining to acquire and there are no resting asks:
  - In early ticks (ticks 1–3), I do not aggressively chase upward bid wars by posting high resting bids above 58; instead, I post conservative bids at or near the prevailing best bid or wait for supply to appear.
  - I never bid for more units than I currently need and never exceed my total available cash budget.
- Whenever I place an order or cross the spread to acquire inventory, I always include `[cancel: all]` (e.g., `[order: buy N @ P] [cancel: all]`) to pull any previous resting bids and prevent double-fills or adverse selection.
- In later ticks (ticks 5–6), when sellers often dump cheaper asks on the book, I aggressively cross the spread at the low ask prices to complete my remaining delivery quota.
- Once my target delivery position is reached (0 units remaining to acquire), I immediately cancel all resting orders and stop trading: I reply with `[order: none] [cancel: all]` on all remaining ticks.
- I do not sell down my position after meeting the delivery requirement; holding the exact required units at settlement avoids shortfall penalties and unnecessary transaction costs.
- If an accidental execution leaves me with an excess position above target on later ticks, I sell only the excess units into the best bid to return exactly to the delivery requirement.