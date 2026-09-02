---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 1736
---
### Core Strategy & Rules of Engagement

1. **Always cancel stale resting orders**: Whenever I place a new order, change my bid price, or when the book moves, I must prepend `[cancel: all]` before my order token to prevent unmanaged fills, stale execution, or over-accumulation.
2. **Aggressively take cheap early supply**: On Tick 1, immediately cross the spread and buy the resting ask up to available size (e.g. 2 units) to secure cheap inventory before competing bots bid the price up.
3. **Never buy more than the delivery requirement**: Calculate remaining required delivery units ($3 - \text{position}$) every single tick. Never submit buy orders for a quantity greater than this remaining amount.
4. **When crossing the spread**: If asks are present at a viable price and I need units, cross the spread up to the available ask quantity or my remaining delivery need (whichever is smaller) using `[cancel: all] [order: buy N @ P]`.
5. **Handling empty ask books (Ticks 2–4)**: When no asks exist on the book, place an incremental buy order for 1 unit at $\text{best bid} + 1$ using `[cancel: all] [order: buy 1 @ P]`. Continue stepping up by 1 tick if unhit to maintain top-of-book priority without blowing out execution price.
6. **Lift late supply when it re-emerges (Ticks 5–6)**: When sellers re-enter the book on later ticks (typically offering supply around ticks 5–6), immediately cross the spread to buy the remaining needed unit(s) at the posted ask price.
7. **Once delivery is satisfied (position = 3)**: Pull all resting orders and sit out the remainder of the session using `[cancel: all] [order: none]` to lock in the final score without incurring unnecessary execution risk, crossing costs, or shortfall penalties.