---
game: ref_orderbook
model: haiku
condition: neutral
seed: 2
round: 3
chars: 3901
---
# Playbook for ref_orderbook

## Core Obligation
When I sit down, my primary goal is to hold exactly 3 units at settlement. Every unit I fall short costs me 8 points. This dominates everything else—aggressive acquisition is justified.

## Early Game (Ticks 1-2)
At tick 1, I need all 3 units. I place a buy order between the current bid-ask spread rather than at the ask. I target 2 units at a split price: typically the midpoint between bid and ask, or 1-2 points above the current best bid.

This approach has worked consistently across episodes. I build position without committing all cash immediately, leaving flexibility to escalate if the market moves against me.

At tick 2, if my order from tick 1 did not fill and I still have 0 units, the market has likely moved against me. I reassess: if the best ask has risen significantly (3+ points), I escalate to buying at or near the ask to lock in position before prices move further. Do not remain passive if the market is moving away from me.

If I have acquired 2 units by tick 2, I hold and assess remaining need.

## Mid Game (Ticks 3-4)
At tick 3, if I have 0-1 units acquired and need 2-3 units, the situation is urgent. I buy 2 units at best ask immediately to secure the bulk of my obligation and prevent late-game panic buying. Do not place passive bids when significantly under-positioned mid-game.

At tick 3, if I have 2 units acquired and need 1 unit remaining, I place a buy order at a split price (1-2 points above best bid, or midpoint between bid and ask). This leaves room to escalate to the ask on tick 4 if needed.

At tick 4, if I need 1 unit and have 2 ticks remaining, I place a buy order at a split price (between bid and ask, closer to the ask). I remain prepared to escalate to the ask on tick 5.

At tick 4, if I need more than 1 unit, I buy aggressively at best ask. By tick 4, I should already have 2+ units. If I don't, I have wasted too much time being passive and must catch up now.

## Late Game (Ticks 5-6)
At tick 5, if I still need any units, I buy at the best ask immediately without hesitation. The penalty for missing delivery far outweighs overpaying by a few points. Do not place passive bids at tick 5.

At tick 6 (final tick), I check my position immediately.

If I'm short, I buy at market at the best ask without delay. There is no negotiation—I execute.

If I'm exactly at 3 units or long, I place no order. Do not attempt to sell for profit at the final tick. Once I have 3 units, I am done.

## What Did Not Work
Placing bids that are too passive early (e.g., buying 2 units at 50 when the market is trading at 53-56) results in zero fills and wastes ticks. I end up forced to buy at much higher prices at the end. If a bid doesn't fill by tick 2, I escalate.

Over-acquiring beyond 3 units creates exit risk and wastes cash. I should target exactly 3 units, not more. If I reach 3 units before tick 6, I hold and do nothing for the remainder.

Spreading my buying across too many price levels over too many ticks leaves me under-positioned late. I should consolidate my buying earlier (ticks 1-4) rather than trying to time perfect fills across all 6 ticks.

Waiting at tick 4 with a full 3-unit need remaining is fatal. By tick 4, I should already have 2+ units.

## Decision Rules in Order
When an order is put to me, I apply these in sequence:

1. How many units do I need to reach 3? (Current need)
2. How many ticks remain including this one? (Urgency)
3. If need = 0: place no order. (Goal met, hold.)
4. If need ≥ 1 and ticks ≤ 2: buy full remaining need at best ask.
5. If need = 1 and ticks = 3-4: buy 1 unit at bid-ask split (midpoint or 1-2 points above best bid), prepared to escalate to ask on next tick if no fill.
6. If need ≥ 2 and ticks = 3-4: buy 2 units at best ask. Secure the bulk of the need now.
7. If need ≥ 1 and ticks = 5: buy full remaining need at best ask immediately.