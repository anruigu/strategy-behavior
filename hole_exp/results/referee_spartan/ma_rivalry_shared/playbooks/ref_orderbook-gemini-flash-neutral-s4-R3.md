---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 1534
---
- On Tick 1, place a resting buy order inside the spread (`best_bid + 1`) for the full delivery requirement to capture cheap inventory early.
- When an ask is priced at or below competing bids on the book (crossed/mispriced book), immediately cross the spread with `[order: buy N @ ask_price]` to lock in cheap liquidity before competitors take it.
- In early to middle ticks (Ticks 2–3), avoid crossing the full book up into overpriced asks (e.g. at 60–61+) for the entire delivery requirement all at once, as the true settlement value is typically around 58–61 and paying high prices early leads to negative PnL. Instead, improve the best bid by 1 tick (`best_bid + 1`) or take only the cheapest available tier (e.g. taking asks at <= 59).
- When posting a new resting bid to improve the top of book, always include `[cancel: all]` so stale lower bids do not linger.
- In Ticks 4–5, if still needing inventory, evaluate remaining units against the shortfall penalty (8 per unit): cross the spread to complete delivery only if ask prices are reasonable; if asks are inflated, step up bids to competitive levels (`best_bid` or `best_bid + 1`) to let sellers fill you rather than aggressively sweeping deep asks.
- If holding partial position (+2 of 3) entering Tick 4, cross the best ask at <= 61 for the single remaining unit to eliminate the 8-point penalty risk.
- Once the delivery requirement is fully satisfied (`Delivery: 0 of 3`), never speculate or post further orders; reply with `[order: none]` and hold through settlement.