---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 980
---
- On Tick 1, place a resting buy order inside the spread (`best_bid + 1`) for the full delivery requirement to capture cheap inventory early.
- When an ask is priced at or below the competing bids on the book, cross the spread immediately with `[order: buy N @ ask_price]` to lock in mispriced liquidity before competitors take it.
- When still needing units in the middle ticks (ticks 2–4) and the spread is wide, improve the top of the bid queue by posting `[order: buy N @ (best_bid + 1)]`.
- If a resting bid remains unfilled and there are 2 or fewer ticks remaining (or if an ask matches our bid price), immediately cross the spread to buy the remaining units needed for delivery. Never risk going into the final tick short of the required delivery amount.
- Once the delivery requirement is satisfied (`Delivery: 0 of 3`), do not sell or speculate; post `[order: none]` and hold through settlement. Never sell out of a fulfilled delivery position to take short-term profits.