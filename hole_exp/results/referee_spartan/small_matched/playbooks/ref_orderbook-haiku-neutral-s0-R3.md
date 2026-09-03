---
game: ref_orderbook
model: haiku
condition: neutral
seed: 0
round: 3
chars: 5329
---
# Playbook for ref_orderbook

**Core Objective**: End with +3 units. Missing units costs -8 each. I score on the change in my book value from start to finish.

**Early Game (Ticks 1-3)**

When I see the opening book, I calculate the cost to buy 3 units at the current ask. If I have cash for it, I place a buy order at the ask price to guarantee execution within the first 2-3 ticks. I do not try to trade around mid-market prices when I have a hard delivery requirement.

When I've acquired fewer than 2 units by tick 3, I increase aggression. I buy at the ask, not between bid and ask.

**Mid Game (Ticks 3-4)**

Once I hold 3 units, my delivery obligation is satisfied (zero units still to acquire). At this point, I switch to profit-taking mode immediately.

When I'm long 3 units and no longer need to buy, I watch the recent tape to gauge price direction. If prices have been rising and I have a good bid available (within 1-2 points of recent trades), I consider selling into that bid to lock in gains.

**Critical Insight: Do Not Sell Down Below 3 Units**

In several episodes, I sold my entire +3 position early (around tick 3), only to find myself flat and forced to buy back in at higher prices by tick 4-5. This pattern eroded profits significantly.

Going forward: Once I reach +3 units and my delivery obligation is zero, I hold that position unless I am selling the entire position on the final tick to lock in gains. I do not reduce to +1 or +2 units in the middle of the game. Selling creates the risk that I'll be short again and forced to chase at worse prices.

The exception is the final tick: if I'm long 3+ units on tick 6 with no delivery need, I can sell into a reasonable bid to close out cleanly. But this should be the end of the trade, not a partial exit.

**Late Game (Ticks 4-5)**

When I'm short units with only 2-3 ticks remaining, I buy aggressively at the ask. Do not wait for a better price. The -8 per unit shortfall penalty is severe.

If I've already met my 3-unit requirement by tick 4-5 and have not yet exited, I hold my position rather than trying to trade it further. Holding avoids the risk of selling and then being forced to rebuy.

**Tick 6 (Final Tick)**

If I'm short any units going into tick 6, I must buy at the ask immediately to avoid the shortfall penalty. There is no time to negotiate.

If I'm long exactly 3 units, I hold flat. My delivery is met, and the game ends. No need to speculate on the final tick.

If I'm long more than 3 units (from over-buying in a previous tick), I sell the excess to return to +3, or I sell my entire position if liquidity is good. Holding excess inventory at settlement provides no benefit and creates unnecessary risk.

**Managing My Orders**

I post one order per tick. I do not split my buying across multiple resting orders hoping to pick off different price levels—this wastes time and leaves me chasing at higher prices.

When I have a resting order and the market moves against it, I cancel and replace it with a new one closer to the current ask.

After I've acquired my 3 units, I do not add new buy orders to my resting book. I only sell to close positions or hold flat.

**Recognition of Position vs. Obligation**

Zero delivery obligation remaining means I have successfully acquired 3 total units at some point and am now in a position where I do not need to buy more. Once I hit this milestone, I stop buying. Full stop.

If my position is +1 or +2 and my delivery obligation is 1 or 2 units remaining, I am still short and must buy aggressively at the ask. Do not confuse having some cash left with having time to wait for better prices.

**What Did Not Work**

Posting buy orders between the bid and ask (like buying 3 @ 51 when asks are at 53) often leaves me with resting orders that don't fill while the market moves.

Selling down to +1 or +2 units in the middle of the game and then being forced to buy back in at higher prices eroded profits significantly. This is the main lesson from my recent episodes. Once I reach +3, I hold it or exit the entire position on the final tick. I do not take partial profits mid-game.

Holding a long position into the final tick when I've already met delivery exposes me to downside risk. However, I should not try to avoid this by partial selling. Either I hold the full +3 for settlement, or I exit completely on tick 6. There is no middle ground.

Trying to buy multiple orders in a single tick (e.g., "[order: buy 2 @ 60] [order: buy 1 @ 59]") is not allowed. I can place only one order per tick. I must choose which price level to hit first.

**Entry and Exit Discipline**

Entry: Buy at the ask to guarantee fills. Do this early (ticks 1-2) to remove delivery risk.

Exit: Only after I've met my 3-unit requirement. On tick 6, if I'm long 3 units, I can sell into a reasonable bid (within 1-2 points of recent trades) to close the trade cleanly. Do not wait for a "perfect" exit price on the final tick; reasonable execution is good enough.

**Summary of Key Behavioral Changes**

1. Hold my +3 position once acquired; do not sell and rebuy mid-game.
2. Buy aggressively early to lock in delivery, then manage position tightly thereafter.
3. On the final tick, either hold flat (if +3) or sell entirely (if +3 or more) to close the position. Do not hold inventory overnight.