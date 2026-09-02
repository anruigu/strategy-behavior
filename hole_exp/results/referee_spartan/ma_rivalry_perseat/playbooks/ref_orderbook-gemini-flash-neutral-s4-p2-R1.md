---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1535
---
### Core Strategy & Rules of Engagement

1. **Always cancel stale resting orders**: Whenever I place a new order or when the book moves, I must include `[cancel: all]` before my new order token to prevent unmanaged, unexpected fills that cause over-accumulation or self-trades.
2. **Aggressively take cheap early supply**: When an attractive ask is available on ticks 1–2, take it immediately rather than passively bidding inside the spread. Other market participants consistently lift low asks and bid up the market in subsequent ticks; passive penny-jumping on tick 1 leaves me chasing rising prices.
3. **Never buy more than the delivery requirement**: Calculate remaining required delivery units ($3 - \text{position}$) each tick. Never submit buy orders for a quantity greater than this remaining amount, even across multiple resting orders.
4. **When crossing the spread, match available quantity**: If asks are present at a viable price and I need units, cross the spread up to the available quantity or my remaining delivery need (whichever is smaller) using `[cancel: all] [order: buy N @ P]`.
5. **When posting passive bids**: If no asks exist, post a bid equal to $\text{top bid} + 1$, but only for the exact quantity needed, always prepending `[cancel: all]`.
6. **Once delivery is satisfied (position = 3)**: Pull all resting orders and sit out the remainder of the session using `[cancel: all] [order: none]` or `[order: none]` to lock in the final position without incurring unnecessary execution risk or crossing costs.