---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 1220
---
- On Tick 1, place a resting buy order inside the spread (`best_bid + 1`) for the full delivery requirement to capture cheap inventory early.
- When an ask is priced at or below competing bids on the book (crossed/mispriced book), immediately cross the spread with `[order: buy N @ ask_price]` to lock in cheap liquidity before competitors take it.
- In early and middle ticks (Ticks 2–3), if there is resting ask liquidity available at a reasonable price (e.g. at or below typical settlement estimates ~57–58) and the spread is narrow (<= 1), cross the spread to take the available units rather than continuously chasing bids upwards.
- When resting bids fail to fill and the spread is wide in Ticks 2–3, improve the best bid by posting `[order: buy N @ (best_bid + 1)]`, always matching `N` to the exact remaining delivery requirement.
- By Tick 4 at the latest, prioritize securing any remaining delivery shortfall by crossing the best available ask, provided it avoids taking severe price spikes above the true value. Do not enter the final two ticks needing multiple units.
- Once the delivery requirement is satisfied (`Delivery: 0 of 3`), never speculate or sell; post `[order: none]` and hold through settlement.