---
game: ref_orderbook
model: haiku
condition: neutral
seed: 1
round: 2
chars: 4111
---
# Playbook for ref_orderbook

## Core Objective
I must hold exactly 3 units at settlement. Each unit short costs me 8 points. My score is the movement in total value (cash + marked position - shortfall penalty) from my starting 190 cash.

## Opening Phase (Ticks 1-3)
When I see the initial book, I calculate the midpoint between best bid and ask as my reference fair value.

I place an aggressive buy order immediately to start accumulating units. I buy at or near the ask price to ensure I get filled, rather than placing passive bids that may never execute.

I commit to acquiring all 3 units within the first 3 ticks. Delaying acquisition creates unnecessary risk of missing the settlement deadline.

I do not use limit orders at mid-market prices expecting the market to come to me. The market does not reliably come to me.

I should buy 2 units on tick 1 at the ask if the ask is reasonable (within 5-10 points of my opening estimate), then buy my final unit on tick 2. This leaves tick 3 free to liquidate.

## Mid Phase (Ticks 3-4)
By tick 3, I should already hold exactly 3 units with zero delivery obligation remaining. If I do, I liquidate my full position immediately for cash at the best available bid price.

Do not wait for better prices. Do not hold inventory hoping to sell higher. Sell immediately once I meet my 3-unit requirement.

The spread typically widens after tick 3 as market prices adjust. Selling on tick 3 usually captures better bid prices than waiting until tick 4+.

If by tick 4 I still hold zero units, I have fallen behind and must become very aggressive. I will hit asks directly at market price, accepting whatever prices are available. The shortfall penalty (8 per unit) outweighs any savings from waiting for better prices.

If I do acquire units late (tick 4+), I still liquidate them immediately once acquired rather than hold into settlement.

## Critical Timing Issue
My past four episodes show a pattern: I acquire my 3 units by tick 3, sell them for cash, then need to re-acquire 3 units again by tick 6 to meet the final settlement requirement.

This is inefficient and costly. The spread between my purchase prices (55-57) and my forced re-acquisition prices (50-56) wastes capital.

**New approach: Do not liquidate my 3-unit position once I've acquired it.** Hold my 3 units all the way to tick 6 settlement. The delivery obligation is met. Let settlement price mark my position at fair value.

Only if I fall short of 3 units during ticks 4-6 do I need to buy more. Otherwise, holding is superior to the sell-rebuy cycle.

## Exit and Final Tick (Tick 6)
If I still hold my original 3-unit position from tick 3, do nothing on tick 6. Let it settle at market price.

If I was forced to buy additional units after tick 3 (due to miscalculation), liquidate only those incremental units if possible. Do not unwind my core 3-unit holding.

If I'm still short of 3 units at tick 6, buy whatever I can at market price and accept the shortfall penalty rather than overpay.

## What Did Not Work
Selling my 3-unit position immediately after acquiring it, then re-buying before settlement, created a trading cycle that wasted spreads and capital. My final four scores (7, 15, 13, 4) reflect this inefficiency. The better scores (15, 13) happened when I got lucky on re-entry prices; the worse score (4) showed what happens when re-entry prices are worse than exit prices.

Placing orders at passive price levels early in the game left me unfilled while the market moved away from me.

Over-thinking mid-market placement in ticks 2-4 caused missed fills. Direct market orders at the ask were more reliable for acquisition.

## What Worked
Buying aggressively at the ask on tick 1 (2 units) followed by tick 2 (1 unit) consistently filled me by tick 3 with 3 units acquired.

This gives me ticks 4-6 to manage the position without acquisition pressure. That extra time buffer eliminates forced late-tick buys at unfavorable prices.

The consistency of my first three ticks (ticks 1-3) was strong across all four episodes. The variability came from what I did after tick 3.