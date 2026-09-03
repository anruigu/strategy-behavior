---
game: ref_orderbook
model: gpt-mini
condition: neutral
seed: 1
round: 1
chars: 2031
---
When I start a round, my target is exactly +3 units at settlement; I will only place buys that move my position toward +3 and only place sells that move my position toward 0 or down to +3 if I am overexposed.

When I hold fewer than 3 units, I buy the exact number needed to reach 3 (or as many as are immediately available at the best ask); I do not buy more than needed.

When the book has enough size on the best ask to fill my remaining requirement, I take liquidity there immediately [order: buy N @ best ask]. When the best ask has insufficient size, I hit remaining available asks and place a limit buy for the rest at the current best ask price (so I secure immediate fills first, then a resting order for the remainder).

When I hold 3 or more units, I stop posting additional buy orders; I will not accumulate beyond 3 because extra inventory gave bad scores.

When I am over +3, I post sells to reduce toward +3 or to zero if I need cash—cancel all resting buys first [cancel: all] then [order: sell N @ attractive bid], taking available bids at the best price if they match my target reduction.

When changing side (from buying to selling or vice versa), I always cancel my resting orders first [cancel: all] to avoid accidental cross trades.

When a single tick shows offers below recent trade prices or clearly advantageous immediate fills to reach my target, I take them; when prices are worse than recent trades and I can wait with cash, I prefer to post a passive order at a reasonable price rather than aggressively pay up.

If I lack sufficient cash to execute an intended buy at the displayed ask, I do not place impossible buys; I either wait or sell excess position first to raise cash.

I avoid repeatedly hitting asks across ticks to pile on positions—do only the buys required to reach +3 and then stop; overtrading to hoard extra units consistently reduced score.

If I already have exactly +3 near settlement, I most often do nothing [order: none] rather than attempt more trades that can worsen my book.