---
game: ref_orderbook
model: qwen3.8-27b
condition: neutral
seed: 1
round: 1
chars: 2080
---
# Playbook

**When the book is crossed (best bid > best ask), I take the liquidity immediately.** I buy at the best ask (or sell at the best bid if I'm short). I do not "wait and observe" — a crossed book is a free edge and it won't last. Size: take the full available size at that level.

**When I'm long and the best bid is above my entry, I sell into the best bid on the next tick.** I lock in the round-trip profit rather than hoping for more. The spread is wide enough that holding is rarely worth the risk of a reversal.

**When I'm flat and the book is not crossed, I bid at the best bid (not below it).** Bidding below the best bid means I'm behind other traders in the queue and will almost never fill. If I want a chance to get in, I match the best bid or go one tick inside.

**When I'm flat and the spread is wide (3+ points), I bid at the midpoint or just below the best ask.** This gives me a chance to fill if a seller comes in, and if I do fill, I'm buying below the ask side. I do not bid at the best bid when the spread is that wide — I'm giving away too much.

**On the final tick, if I'm flat I stay flat.** There's no time to open and close a position. I do not open a new position on the last tick.

**On the final tick, if I'm long, I sell at the best bid.** Even at a loss, flattening is better than being marked to settlement at an unknown price. Same for short: buy back at the best ask.

**I do not post orders I don't intend to let fill.** If I'm going to cancel on the next tick anyway, I'm just adding noise. Either commit to the order or don't post it.

**What did not work:**
- Waiting on a crossed book to "gather more information" — the cross closes and the edge is gone.
- Repeatedly bidding below the best bid hoping to get a better price — these orders never fill and I end the episode flat with no gain.
- Opening a position in tick 4 or 5 with only 1-2 ticks to manage it — I either got stuck or had to exit at breakeven.
- Bidding at the same level as other traders when I'm not the first in queue — I should either beat them or not bother.