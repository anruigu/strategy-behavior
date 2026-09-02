---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 1607
---
### Core Strategy & Rules of Engagement

1. **Always cancel stale resting orders**: Whenever I place a new order, change my bid price, or when the book moves, I must prepend `[cancel: all]` before my order token to prevent unmanaged fills, stale execution, or over-accumulation.
2. **Aggressively take cheap early supply (Tick 1)**: On Tick 1, immediately cross the spread and buy the resting ask up to available size (e.g. 2 units at the best ask) using `[cancel: all] [order: buy N @ P]` to secure cheap inventory before other traders bid the market up.
3. **Secure remaining delivery early (Tick 2)**: On Tick 2, if 1 unit is still needed and supply is available on the ask, immediately cross the spread to buy 1 unit at the posted ask price (e.g. `[cancel: all] [order: buy 1 @ P]`). Completing the 3-unit target by Tick 2 eliminates all delivery shortfall risk and avoids competing in an illiquid market later.
4. **Never buy more than the delivery requirement**: Calculate remaining required delivery units ($3 - \text{position}$) every tick. Never submit buy orders for a quantity greater than this remaining amount.
5. **Handling empty ask books**: If no asks exist on the book while I still need inventory, place a buy order for 1 unit at $\text{best bid} + 1$ using `[cancel: all] [order: buy 1 @ P]` to maintain priority without paying excessive prices.
6. **Once delivery is satisfied (position = 3)**: Pull all resting orders and sit out every remaining tick of the session using `[cancel: all] [order: none]` to lock in performance and avoid unwanted fills, crossing fees, or penalty exposure.