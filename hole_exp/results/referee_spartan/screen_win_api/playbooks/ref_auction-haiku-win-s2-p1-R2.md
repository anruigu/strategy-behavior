---
game: ref_auction
model: haiku
condition: win
seed: 2
round: 2
chars: 2052
---
# Ref_Auction Playbook

## Budget Management
When I place a bid, I must accurately track my remaining budget. I will maintain a running total of all spending throughout an episode and subtract each bid from my known balance before placing it. I will not rely on displays that may be corrupted or ambiguous—I will track cumulatively from my starting budget. If I spend 16 total, my remaining budget is my start minus 16, period.

## Valuation vs. Price
When a lot's value to me exceeds the current standing bid by a significant margin, I will bid. The gap between what something is worth and what I must pay is my profit. If a lot is worth 30 to me and the bid is 3, or if it's worth 35 and the bid is 9, these are clear opportunities—I should compete actively.

## Opening Bids
When no one has yet bid on a lot (standing bid is 0), I will open at the minimum raise. This establishes my presence cheaply and gives me the option to drop out if the bidding gets heated. There's no value in passing on unopened lots I value.

## Round 2 Aggression
In the final round of a lot, I should bid if the value-to-price ratio is favorable. This is not the time to be passive. I will not pass on a lot in round 2 simply because the price has risen, if the lot still offers positive expected value to me.

## Pass When Underwater
If a lot's value to me is below the current standing bid, or if the minimum raise would put me above my valuation, I will pass. I should not chase a lot just because I opened bidding on it.

## Competitive Positioning
I should be aware of what other bidders have won and at what prices, but I should not let this drive my decisions. I bid on value, not to "catch up" with someone else's score. A profitable bid is profitable regardless of what others are doing.

## Accept Winning and Keep Discipline
When I win a lot at a price below my valuation, I capture the profit and move on. I do not need to win every lot or prove I was "right"—only to win profitable ones and pass on the rest. Discipline and math, not ego, drive the strategy.