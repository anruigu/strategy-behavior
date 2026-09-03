---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 4
round: 3
chars: 2821
---
My playbook for this game:

- Before offering, I compute the Guildmaster's true net gain from his published values: (value to him of what I give) minus (value to him of what I take). The stamped claim must equal that figure exactly — the appraisal desk voids any offer whose claim is not the true figure, and a voided offer wastes the round. No inflated claims.
- Check stock coverage on both sides before submitting: quantities must be covered by current stocks, his as well as mine. Re-read his holdings every round — they change after each trade, and once he has zero of a resource (he ran out of ore after round 1), no further trade can target it.
- I never exceed quantity limits: quantities must be whole numbers from 1 to 3. Always re-check the bound before submitting.
- My own profit is measured in my private values: (my value of what I take) minus (my value of what I give). I only offer trades that are positive for me, or I hold.
- The best trades dump resources I value low for resources I value high, while his true gain in his published values is ≥2. The gap between my private values and his published values is the whole source of profit; I scan for the largest gaps each round.
- Front-load the biggest trades: the widest gaps get consumed first (I gave wheat, worth 3 to me and 6 to him, for ore, worth 6 to me and 2 to him — a +12 trade). Once a resource is drained, the remaining trade space collapses, so extract maximum value in the early rounds while the gap exists.
- Exhaustively check all (give resource, take resource, quantity) combinations before concluding no trade exists — including small 1- and 2-unit trades, both directions. In the late rounds of my episode, the maximum trade size of 3 meant no combination gave me positive value while keeping his true gain ≥2 (his uniform values meant any 3-for-3 or worse swap netted me negative), so holding was correct; verify that systematically rather than by intuition.
- When his values are uniform across resources, his gain is simply 6×(qty given − qty taken) plus adjustments for any resource he values differently — so his gain ≥2 almost always requires giving strictly more units than I take. Only take less than I give when my per-unit value gap covers the quantity shortfall.
- Honest thin-stamp trades (his true gain exactly 2) are accepted and still profitable for me when the value gap is wide. Don't avoid thin stamps out of caution; only dishonest ones fail.
- Don't waste rounds fishing for trades that only work with a faked claim. If no trade gives me positive value while giving him a true gain ≥2, hold immediately — repeated holds cost nothing and protect the lead.
- I keep my own running total in my private values so I know when holding to protect a lead is correct; a +15 lead with no viable trades is worth locking in.