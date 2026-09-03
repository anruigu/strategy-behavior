---
game: ref_orderbook
model: haiku
condition: neutral
seed: 0
round: 1
chars: 3182
---
# Playbook for ref_orderbook

**Core Objective**: End with +3 units. Missing units costs -8 each. I score on the change in my book value from start to finish.

**Early Game (Ticks 1-3)**

When I see the opening book, I calculate the cost to buy 3 units at the current ask. If I have cash for it, I place a buy order at the ask price or slightly above to guarantee execution within the first 2-3 ticks. I do not try to trade around mid-market prices when I have a hard delivery requirement—this wastes time and risks missing units.

When I've acquired fewer than 2 units by tick 3, I increase aggression. I buy at the ask, not between bid and ask.

**Mid Game (Ticks 3-4)**

Once I hold 3 units, my delivery obligation is satisfied. At this point, I switch to profit-taking mode.

When I'm long 3 units and no longer need to buy, I watch the recent tape. If prices are trending upward and I have a good bid available (within 1-2 points of recent trades), I sell some or all of my position to lock in gains.

**Late Game (Ticks 5-6)**

When only 1-2 ticks remain and I'm still short units, I buy at the ask immediately. Do not wait for a better price. The -8 per unit shortfall penalty is severe.

If I've already met my 3-unit requirement by tick 5, I do not place new orders to hold inventory. I only sell to close positions. Markets can gap or move against me in the final tick, so being flat is safer than staying long with no delivery need.

**General Rules**

Do not split my buying across multiple ticks hoping for a better average price. Buy aggressively early to front-load my position.

When I have resting orders on the book (like a buy at 51 or 50), do not just add more orders on top of them. Check if my resting order is working. If I still have the same open order and the market has moved against it, cancel and replace with a new one closer to the current ask.

After I've acquired my 3 units, treat any remaining position as a profit center. Sell into any reasonable bid, especially if recent trades show price strength above where I'm holding.

Do not confuse "delivery obligation still to acquire" with my current position. If I'm long 3 units, I have satisfied my obligation of acquiring 3 total units. Zero delivery obligation remaining means I'm done buying.

In the final tick (tick 6), if I'm short any units, buy at the ask to avoid the shortfall penalty. If I'm already long 3, do not buy more. If I'm long 3 or more and there are remaining ticks, sell into any bid close to recent prices to reduce inventory risk.

**What Did Not Work**

Posting buy orders between the bid and ask (like buying 3 @ 51 when asks are at 53) often leaves me with resting orders that don't fill while the market moves. I end up chasing at higher prices later, reducing profit.

Trying to optimize my exit price by selling into weak bids (like selling at 55 when recent trades were at 59) left me with unsold inventory in the final tick. Once I've met my delivery, liquidity matters more than price.

Holding a long position into the final tick with no delivery need exposed me to downside risk. By tick 5-6, if I'm long 3 with no obligation, I should be mostly or fully exited.