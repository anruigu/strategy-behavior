---
game: ref_orderbook
model: haiku
condition: neutral
seed: 1
round: 3
chars: 4291
---
# Playbook for ref_orderbook

## Core Objective
I must hold exactly 3 units at settlement. Each unit short costs me 8 points. My score is the movement in total value (cash + marked position - shortfall penalty) from my starting 190 cash.

## Opening Phase (Ticks 1-3)
When I see the initial book, I calculate the midpoint between best bid and ask as my reference fair value.

I place an aggressive buy order immediately to start accumulating units. I buy at or near the ask price to ensure I get filled, rather than placing passive bids that may never execute.

I commit to acquiring all 3 units within the first 3 ticks. Delaying acquisition creates unnecessary risk of missing the settlement deadline.

I do not use limit orders at mid-market prices expecting the market to come to me. The market does not reliably come to me.

I should buy 2 units on tick 1 at the ask if the ask is reasonable (within 5-10 points of my opening estimate), then buy my final unit on tick 2. This leaves tick 3 free to assess my position.

## Mid Phase (Ticks 3-4): Hold, Do Not Liquidate
By tick 3, I should already hold exactly 3 units with zero delivery obligation remaining. 

**Once I acquire exactly 3 units, I hold them. I do not liquidate and re-buy.**

My past four episodes all showed the same pattern: I sold my 3-unit position after tick 3, then was forced to re-acquire before tick 6, wasting spreads and capital. Even when re-entry prices were favorable, this cycle was inefficient. When re-entry prices were poor, my score collapsed.

Holding my 3-unit position from tick 3 through tick 6 settlement eliminates this waste. The delivery obligation is met once I hold 3 units. Settlement will mark my position at fair value.

On ticks 4-5, if I still hold my original 3 units, I post no orders and take no action.

## Critical Timing Issue — Holding vs. Liquidating
My first three ticks are consistent and strong across all episodes: I acquire 3 units by tick 3 with a blended cost of 49-57.

The variable part is what happens next:
- Episodes where I held my 3-unit position through to settlement scored +15 and +15.
- Episodes where I liquidated early, then re-acquired late, scored +15, +14, and lower.

The best score in my dataset was +15, achieved by:
- Buying 2 units on tick 1 at the ask.
- Buying 1 unit on tick 2 at the ask.
- Holding all 3 units through tick 6 without liquidating or re-acquiring.
- Posting no orders on ticks 3-6.

This pattern is consistent. I will adopt it as my standard approach.

## Exit and Final Tick (Tick 6)
If I still hold my original 3-unit position from tick 3, I post [order: none] on tick 6 and let my position settle at market price. The game ends; settlement marks my position.

If I was forced to buy additional units after tick 3 (due to miscalculation or shortfall), I hold them without liquidating and let settlement mark the full position.

I do not liquidate at the final tick unless I'm trying to capture a sudden price spike above my acquisition cost. In the absence of clear upside, holding is simpler and more reliable than trying to time a final-tick sale.

## What Worked
Buying aggressively at the ask on tick 1 (2 units) followed by tick 2 (1 unit) consistently filled me by tick 3 with 3 units acquired.

Holding my 3-unit position from tick 3 through settlement without liquidating or re-acquiring generated scores of +15, which matches my best results.

The consistency of my first three ticks (ticks 1-3) was strong across all four episodes. Simplifying my actions on ticks 3-6 (do nothing) removed the variability that came from trying to optimize liquidation timing and re-entry prices.

## What Did Not Work
Selling my 3-unit position immediately after acquiring it, then re-buying before settlement, created a trading cycle that wasted spreads and capital.

Placing orders at passive price levels early in the game left me unfilled while the market moved away from me.

Over-thinking mid-market placement in ticks 2-4 caused missed fills. Direct market orders at the ask were more reliable for acquisition.

Waiting for better prices at tick 4-6 after liquidating at tick 3 was inefficient. Once I acquired 3 units, there was no benefit to selling. The spread I captured at sale was always offset by having to re-acquire later.