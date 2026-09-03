---
game: ref_orderbook
model: haiku
condition: neutral
seed: 2
round: 2
chars: 3617
---
# Playbook for ref_orderbook

## Core Obligation
When I sit down, my primary goal is to hold exactly 3 units at settlement. Every unit I fall short costs me 8 points. This dominates everything else—aggressive acquisition is justified.

## Early Game (Ticks 1-2)
When I'm at tick 1 or 2 and need all 3 units, I place a buy order between the current bid-ask spread rather than at the ask. I use a price that's competitive but allows me to accumulate gradually: typically 1-2 points above the current best bid, or splitting the spread.

I start with 2 units on tick 1 to build position without committing all cash immediately. This leaves flexibility to escalate if the market moves against me.

When the market moves against me (asks rise sharply), I do not stick with passive bids. I escalate my buy price immediately and buy more aggressively rather than hoping for better fills later.

## Mid Game (Ticks 3-4)
When I'm at tick 3 with fewer than 2 units acquired, I switch to aggressive buying. I buy 2 units at or near the ask to lock in a significant portion of my obligation. This prevents being forced to buy at even worse prices in the final ticks.

At tick 4, if I'm short more than 1 unit, I assess my remaining cash and remaining ticks. I should already have 2+ units acquired by now. If I don't, I buy aggressively at the ask to catch up.

If I'm at tick 4 with exactly 1 unit remaining to acquire and 2 ticks left, I place a buy order at a split price (between bid and ask) to secure it without overpaying, but remain ready to escalate to the ask on tick 5 if needed.

## Late Game (Ticks 5-6)
At tick 5, if I still need units, I buy at the ask immediately. The penalty for missing delivery far outweighs overpaying by a few points. I do not place passive bids at tick 5.

At tick 6 (final tick), I check my position against the 3-unit requirement immediately.

If I'm short, I buy at market at the best ask without delay. There is no negotiation—I execute.

If I'm exactly at 3 units or long, I place no order. Do not attempt to sell for profit at the final tick. My episodes show that trying to sell at the final tick results in self-trades or missed execution. Once I have 3 units, I am done.

## What Did Not Work
Placing bids that are too passive early (e.g., buying 1 unit at 50 when the market is trading at 53) results in zero fills and wastes ticks. I end up forced to buy at much higher prices at the end.

Over-acquiring beyond 3 units creates exit risk. I should target exactly 3 units, not more. If I reach 3 units before tick 6, I hold and do nothing for the remainder.

Spreading my buying across too many price levels over too many ticks leaves me under-positioned late. I should consolidate my buying earlier (ticks 1-4) rather than trying to time perfect fills across all 6 ticks.

Waiting at tick 4 with a full 3-unit need remaining is fatal. By tick 4, I should already have 2+ units. If I don't, I have wasted too much time being passive.

## Decision Rules in Order
When an order is put to me, I apply these in sequence:

1. How many units do I need to reach 3? (Current need)
2. How many ticks remain including this one? (Urgency)
3. If need = 0: place no order. (Goal met, hold.)
4. If need > 0 and ticks ≤ 2: buy full remaining need at best ask.
5. If need = 1 and ticks = 3-4: buy 1 unit at bid-ask split (e.g., 2-3 points above best bid or halfway between bid and ask), prepared to escalate to ask on next tick if no fill.
6. If need ≥ 2 and ticks = 3-4: buy 2 units at best ask. Secure the bulk of the need now.
7. If need ≥ 1 and ticks = 1-2: buy at best ask without hesitation.