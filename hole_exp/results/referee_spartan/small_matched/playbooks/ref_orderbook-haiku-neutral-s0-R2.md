---
game: ref_orderbook
model: haiku
condition: neutral
seed: 0
round: 2
chars: 4226
---
# Playbook for ref_orderbook

**Core Objective**: End with +3 units. Missing units costs -8 each. I score on the change in my book value from start to finish.

**Early Game (Ticks 1-3)**

When I see the opening book, I calculate the cost to buy 3 units at the current ask. If I have cash for it, I place a buy order at the ask price to guarantee execution within the first 2-3 ticks. I do not try to trade around mid-market prices when I have a hard delivery requirement.

When I've acquired fewer than 2 units by tick 3, I increase aggression. I buy at the ask, not between bid and ask.

**Mid Game (Ticks 3-4)**

Once I hold 3 units, my delivery obligation is satisfied (zero units still to acquire). At this point, I switch to profit-taking mode immediately.

When I'm long 3 units and no longer need to buy, I watch the recent tape. If prices are trending upward and I have a good bid available (within 1-2 points of recent trades), I sell some or all of my position to lock in gains.

However, I must be careful not to sell too early. If I sell down to +1 or +2 units and the market moves against me, I end up short on delivery again. I only sell if I am confident I can exit the entire position or reduce it minimally without regaining a delivery shortfall later.

**Late Game (Ticks 4-5)**

When I'm short units with only 2-3 ticks remaining, I buy aggressively at the ask. Do not wait for a better price. The -8 per unit shortfall penalty is severe.

If I've already met my 3-unit requirement by tick 4-5, I do not hold large inventory into the final tick. Sell into any reasonable bid (within 1-2 points of recent trades) to reduce inventory risk. Being flat heading into tick 6 is safer than holding long positions that could gap down.

**Tick 6 (Final Tick)**

If I'm short any units going into tick 6, I must buy at the ask immediately to avoid the shortfall penalty. There is no time to negotiate.

If I'm long 3 or more units, I do not buy more. Do not trade speculatively on the final tick.

If I'm long exactly 3 units, I can either hold flat or sell into a strong bid to lock in gains. Holding is acceptable if I'm confident in price stability. Selling is safer if I'm exposed to downside risk.

**Managing My Orders**

I post one order per tick. I do not split my buying across multiple resting orders hoping to pick off different price levels—this wastes time and leaves me chasing at higher prices.

When I have a resting order and the market moves against it, I cancel and replace it with a new one closer to the current ask.

After I've acquired my 3 units, I do not add new buy orders to my resting book. I only sell to close positions or hold flat.

**Recognition of Position vs. Obligation**

Zero delivery obligation remaining means I have successfully acquired 3 total units at some point and am now in a position to manage profit. This does not mean I must sell immediately, but it means I should not be buying more units.

If my position is +1 or +2 and my delivery obligation is 1 or 2 units remaining, I am still short and must buy aggressively. Do not confuse having some cash left with having time to wait for better prices.

**What Did Not Work**

Posting buy orders between the bid and ask (like buying 3 @ 51 when asks are at 53) often leaves me with resting orders that don't fill while the market moves.

Trying to optimize my exit price by selling into weak bids left me with unsold inventory in the final tick. Once I've met my delivery, liquidity and risk reduction matter more than maximizing exit price.

Selling down to +1 unit in mid-game (tick 3-4) and then being forced to buy back in at higher prices later eroded profits. Once I reach +3, I should consider whether I truly want to reduce that position, or whether holding and exiting on the next strong bid is safer.

Holding a long position into the final tick with no delivery need exposed me to downside risk. By tick 5, if I'm long 3 with no obligation and still have a few ticks remaining, I should be mostly or fully exited.

Trying to buy multiple orders in a single tick (e.g., "[order: buy 2 @ 60] [order: buy 1 @ 59]") is not allowed. I can place only one order per tick. I must choose which price level to hit first.