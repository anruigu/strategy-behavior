---
game: ref_orderbook
model: haiku
condition: neutral
seed: 1
round: 1
chars: 2388
---
# Playbook for ref_orderbook

## Core Objective
I must hold exactly 3 units at settlement. Each unit short costs me 8 points. My score is the movement in total value (cash + marked position - shortfall penalty) from my starting 190 cash.

## Opening Phase (Ticks 1-3)
When I see the initial book, I calculate the midpoint between best bid and ask as my reference fair value.

I place an aggressive buy order immediately to start accumulating units. I buy at or near the ask price to ensure I get filled, rather than placing passive bids that may never execute.

I commit to acquiring all 3 units within the first 3 ticks. Delaying acquisition creates unnecessary risk of missing the settlement deadline.

I do not use limit orders at mid-market prices expecting the market to come to me. The market does not reliably come to me.

## Mid Phase (Ticks 4-5)
By tick 4, I should already hold 2-3 units. If I still need units, I become more aggressive with pricing.

If I'm short on units at tick 4, I hit the ask prices directly rather than hoping for better fills. Time decay matters more than price improvement at this stage.

Once I hold 3 units and have zero delivery obligations remaining, I stop trying to acquire more inventory. My job is done.

## Exit and Final Tick (Tick 6)
Once I've secured my 3-unit delivery requirement, I do not hold the position into settlement. I liquidate my full position for cash.

I sell my 3 units at the best available bid price, not at mid-market or ask prices. I capture whatever bid liquidity exists.

On the final tick, I execute my exit trade immediately without waiting to see if the market moves. The game ends immediately after tick 6 and marks my position at settlement price.

## What Did Not Work
Placing orders at passive price levels (below current market) early in the game left me unfilled while the market moved away from me. I wasted ticks waiting for fills that never came.

Holding inventory after fulfilling my delivery obligation and waiting for better exit prices sometimes backfired. I got trapped short of cash at settlement or forced to sell into weakness.

Over-thinking mid-market placement in ticks 2-4 caused missed fills. Direct market orders at the ask were more reliable for acquisition.

Trying to time exits or optimize selling prices in the final ticks created risk. Simple immediate execution would have been better.