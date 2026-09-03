---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 1842
---
Every reply ends with two bracketed tokens: the bid line and the budget line, in exactly that format, with no stray text after them.

The budget token is the budget the game reported to me as remaining, not a number I invent. I copy the figure shown alongside "You start with" or the latest standing state. I never guess a "standard 100 starting budget" when the actual stated budget is 30 — I track the true starting budget and subtract only what I actually won and paid.

Before bidding I compute: my value minus the required bid. If positive, I bid; if zero or negative, I pass. I never bid at or above my value.

In round 1 of a lot, I open with the minimum raise unless the lot is my last chance to score and I face aggressive rivals — minimum keeps the price low and wins cheap when others pass.

In round 2 (final round) of a lot I want, I judge how high rivals have pushed: if the standing bid is far below my value and rivals have shown they'll chase, I bid toward my value minus a small margin rather than the minimum, since there is no later round to recover. If I only bid the minimum each time, determined opponents outbid me and I win nothing.

I do not bid up a lot I don't want just because it's cheap — if my value is below the standing bid, I pass immediately, as I correctly did when the price passed my value.

I remember the budget rule: the budget token shows funds left, and a bid I make doesn't reduce it until I win. But I never let outstanding bids exceed what I can pay if I win.

I read rival behavior from results so far: if past lots closed well above minimum raises, rivals value the lots highly, so on remaining lots I bid aggressively on my high-value lots in round 2 rather than inching up.

I never end a final round holding most of my budget unspent while rivals take every lot — unused budget scores zero.