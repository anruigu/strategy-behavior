---
game: ref_orderbook
model: qwen3.8-27b
condition: neutral
seed: 1
round: 2
chars: 2549
---
# Playbook

**When the book is crossed (best bid > best ask), I take the liquidity immediately.** I buy at the best ask (or sell at the best bid if I'm short). I do not wait or observe — a crossed book is a free edge and it won't last. Size: take the full available size at that level. This is my primary edge and it has appeared reliably on tick 2 in every episode I've played.

**When I'm long and the best bid is above my entry, I sell into the best bid on the next tick.** I lock in the round-trip profit rather than hoping for more. This has worked every time: the bid side is consistently above my entry after a crossed-book fill.

**When I'm flat and the book is not crossed, I post a small bid at or near the midpoint as a free option.** I do not expect it to fill. It costs me nothing if it doesn't, and if the book moves my way I get in at a good price. I do not agonize over the exact level — midpoint or one tick inside the ask is fine. The point is to have a resting order in case of a favorable move, not to actively trade.

**On tick 4 and beyond, if the book is not crossed, I stay flat and post no orders.** My bids at midpoint on tick 4 have never filled in any episode. Posting them is noise. The only reason to act on tick 4+ is if the book is crossed — then I take it, same as always.

**On the final tick, if I'm flat I stay flat.** There's no time to open and close a position.

**On the final tick, if I'm in a position, I flatten at the best available price.** Sell at the best bid if long, buy at the best ask if short. Even at a loss, being flat at settlement is better than being marked at an unknown price.

**I do not post orders I don't intend to let fill.** If I'm going to cancel on the next tick anyway, I'm just adding noise. Either commit to the order or don't post it.

**What did not work:**
- Waiting on a crossed book to "gather more information" — the cross closes and the edge is gone.
- Expecting my midpoint bids to fill when the spread is wide and the book isn't crossed — they don't. The cross is what fills, not my patient bid.
- Posting bids on tick 4+ when the book isn't crossed — they never fill and I'm just cluttering the book.
- Opening a position in tick 5 or 6 with no time to manage it.

**What worked (and I should keep doing):**
- The tick 1 bid as a free option (harmless, occasionally useful).
- Taking the crossed book on tick 2 without hesitation.
- Selling into the best bid on tick 3 to lock in the round-trip.
- Staying flat and quiet after the round-trip unless a new cross appears.