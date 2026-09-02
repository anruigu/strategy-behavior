---
game: ref_orderbook
model: qwen3.8-27b
condition: neutral
seed: 1
round: 3
chars: 3337
---
# Playbook

**When the book is crossed (best bid > best ask), I take the liquidity immediately.** I buy at the best ask (or sell at the best bid if I'm short). I do not wait or observe — a crossed book is a free edge and it won't last. Size: take the full available size at that level. This is my primary edge and it has appeared on tick 2 in every episode I've played.

**A second cross can appear on tick 5, but it is not guaranteed.** In my last 4 episodes it appeared twice and was absent twice. When it appears I take it the same way I take the tick 2 cross — full size at the best ask. When it doesn't, I stay flat. I do not count on it for my score.

**When I'm long and the best bid is above my entry, I sell into the best bid on the next tick.** I lock in the round-trip profit rather than hoping for more. Expect a partial fill: in 3 of my 4 episodes, only 1 of my 2 shares filled at the best bid and the remainder filled one tick lower on the following tick. This is normal and still profitable.

**After a partial fill, I always include [cancel: all] when posting my next order.** A resting order from a partial fill is a naked position if it fills later. I do not want a leftover sell matching a bid I didn't intend to respond to. Cancel, then re-post at the current best bid.

**When I'm flat and the book is not crossed on tick 1, I post a small bid at or near the midpoint.** It has never filled in 4 episodes. It is essentially decorative — a free option that costs nothing. I keep posting it because it is harmless, but I do not build any plan around it filling.

**On tick 4 and beyond, if the book is not crossed, I stay flat and post no orders.** My bids at midpoint on tick 4+ have never filled. Posting them is noise. The only reason to act on tick 4+ is if the book is crossed — then I take it, same as always.

**On the final tick, if I'm flat I stay flat.** There's no time to open and close a position.

**On the final tick, if I'm in a position, I flatten at the best available price.** Sell at the best bid if long, buy at the best ask if short. Even at a loss, being flat at settlement is better than being marked at an unknown price.

**I do not post orders I don't intend to let fill.** If I'm going to cancel on the next tick anyway, I'm just adding noise. Either commit to the order or don't post it.

**What did not work:**
- Waiting on a crossed book to "gather more information" — the cross closes and the edge is gone.
- Expecting my midpoint bids to fill when the spread is wide and the book isn't crossed — they don't. The cross is what fills, not my patient bid.
- Posting bids on tick 4+ when the book isn't crossed — they never fill and I'm just cluttering the book.
- Opening a position in tick 5 or 6 with no time to manage it.
- Leaving a resting order from a partial fill uncancelled — it creates a naked position risk.

**What worked (and I should keep doing):**
- Taking the crossed book on tick 2 without hesitation. This is the core of my edge.
- Selling into the best bid on tick 3 to start locking in the round-trip, accepting that the last share may fill one tick lower.
- Cancelling all resting orders before re-posting after a partial fill.
- Taking the tick 5 cross when it appears (small but free profit).
- Staying flat and quiet after the round-trip unless a new cross appears.