---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1379
---
# Playbook for Order Book Delivery Game

- When Tick 1 opens with resting asks near or slightly above the initial bid levels, buy immediately to lock in the lowest prices of the game instead of trying to penny the bids. In an accumulation requirement with competing buyers, prices ratchet upward aggressively; delaying inventory acquisition forces panicky fills at much higher prices in late ticks.
- When placing a resting bid because no reasonable asks exist, always include `[cancel: all]` when updating the bid on the next tick so old orders do not linger and cause accidental double-fills when sellers cross the spread later.
- When resting a bid, only bid for the exact quantity still required to meet the target position, never for more units than needed.
- When holding unfilled delivery requirements by Tick 3 or 4 and asks are present on the book, cross the spread and take the available asks rather than continually trying to post incremental bids inside the spread.
- When surplus units are acquired beyond the delivery target, immediately cross the highest available bid with `[order: sell N @ P]` to liquidate the excess before market prices decay toward settlement.
- When the delivery requirement is fully met (0 units left to acquire) and the position equals the target, submit `[cancel: all] [order: none]` to avoid accidental fills and preserve the final book.