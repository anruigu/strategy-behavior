---
game: ref_orderbook
model: haiku
condition: neutral
seed: 2
round: 1
chars: 2763
---
# Playbook for ref_orderbook

## Core Obligation
When I sit down, my primary goal is to hold exactly 3 units at settlement. Every unit I fall short costs me 8 points. This dominates everything else—aggressive acquisition is justified.

## Early Game (Ticks 1-3)
When I'm at tick 1 or 2 and need all 3 units, I place a buy order between the current bid-ask spread rather than at the ask. I use a price that's competitive but allows me to accumulate gradually: typically 1-2 points above the current best bid, or splitting the spread.

When the market moves against me (asks rise), I do not stick with passive bids. I escalate my buy price immediately rather than hoping for better fills later.

When I'm at tick 3 with fewer than 2 units acquired, I switch to aggressive buying at or near the ask. Waiting costs me more than overpaying.

## Mid Game (Ticks 4-5)
When I'm at tick 4 or 5 with a shortfall remaining, I assess: how many units do I still need, how many ticks remain, and what's the current ask price?

If I need more than one tick's worth of liquidity to fill, I place buy orders at multiple price levels to ensure execution across the remaining time.

If I have just one or two ticks left and still need units, I buy at the ask without hesitation. The penalty for missing delivery (8 per unit) far outweighs overpaying by 1-2 points.

## Final Tick (Tick 6)
When I reach tick 6, I check my position against the 3-unit requirement immediately.

If I'm short, I buy at market at the best ask without delay. There is no negotiation—I execute.

If I'm long after fulfilling my 3-unit obligation, I do not attempt to exit for profit. My episodes show that trying to sell at the final tick often results in self-trades or missed execution. I do nothing instead.

## What Did Not Work
Placing bids that are too passive early (e.g., buying 1 unit at 50 when the market is trading at 53) results in zero fills and wastes ticks. I end up forced to buy at much higher prices at the end.

Trying to sell units at the final tick after over-acquiring creates problems—I either self-trade or fail to exit cleanly. I should avoid over-acquiring in the first place.

Spreading my buying across too many price levels over too many ticks leaves me under-positioned late. I should consolidate my buying earlier rather than trying to time perfect fills.

## Decision Rules in Order
When an order is put to me, I apply these in sequence:

1. How many units do I need to reach 3? (Current need)
2. How many ticks remain? (Urgency)
3. If need > 0 and ticks ≤ 2: buy at best ask for full remaining need.
4. If need > 0 and ticks 3-4: buy 60-70% of need at bid-ask split, be ready to escalate.
5. If need > 0 and ticks 1-2: buy remainder at ask.
6. If need = 0: place no order.