---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 2201
---
# Playbook for Order Book Delivery Game

- When Tick 1 opens with resting asks near or slightly above the initial bid levels, buy immediately to lock in low prices instead of pennying the bids. In an accumulation requirement with competing buyers, prices ratchet upward aggressively; delaying inventory acquisition forces costly fills at higher prices in late ticks.
- When no asks are present on the book during early ticks (Ticks 1–3), place a competitive resting bid at or just above the current best bid (e.g. best bid + 1) for the exact quantity needed, but avoid bidding excessively high (above 60) in Tick 3 if sellers consistently arrive at lower prices in Ticks 4–5.
- When placing or modifying a resting bid, always include `[cancel: all]` on subsequent ticks so older resting bids do not remain on the book and cause unintended over-fills when sellers cross the spread.
- When resting a bid, never bid for more units than the exact quantity still required to satisfy the delivery target (`Delivery: N of 3 units still to acquire`).
- As soon as asks appear on the book (typically Ticks 4–5), cross the spread immediately by bidding at or above the best ask price for up to the needed quantity rather than continuing to post resting passive bids.
- When crossing an ask for fewer units than needed, place the buy order at the ask price for the full remaining delivery quantity (e.g. `[order: buy 3 @ P_ask]`) so that available asks fill immediately while the balance remains as a high-priority resting bid at that lower ask price.
- In Tick 5, if still needing 1 unit and asks are resting below prior prices, cross the best ask immediately with `[order: buy 1 @ P_ask]` to guarantee the delivery requirement is met before the final tick.
- When surplus units are acquired beyond the delivery target, immediately cross the highest available bid with `[order: sell N @ P]` to liquidate the excess before market prices decay toward settlement.
- Once the delivery requirement is fully met (0 units left to acquire) and the position equals the target, submit `[cancel: all] [order: none]` on all remaining ticks (especially Tick 6) to avoid any accidental executions and lock in the final score.