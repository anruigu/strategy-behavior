---
game: ref_estate
model: haiku
condition: win
seed: 7
round: 3
chars: 3109
---
# Playbook for ref_estate

When I'm shown a property I can afford, I'll buy it if:
- It costs 100 or less, or
- It costs more than 100 but I'll retain at least 50 in cash after purchase, or
- I'm in the first half of the game and the property has good rent-to-price ratio (rent at least 20% of price)

When I'm shown a property I cannot afford, I'll decline without hesitation and move on.

When calculating my current balance, I will:
- Start with my last declared balance
- Add all recent transfers TO me from other investors
- Subtract all recent transfers FROM me to other investors
- Account for salary collected this turn if I passed START
- Then subtract any rent or purchase costs due this turn

When I land on an unowned property in the late game (lap 5 or 6), I'll be more cautious about purchases. In lap 5, I won't buy unless I can retain at least 25 cash. In lap 6, since the game ends immediately after, I can buy if I have positive balance afterward, since rental income no longer matters—only final asset value counts.

When I owe rent, I'll pay it immediately and adjust my balance correctly before declaring it.

I will not overthink property decisions. Early in the game (laps 1-3), acquire properties aggressively if I can afford them with 25+ cash remaining. Mid-game (laps 4-5), be selective about expensive properties unless I have strong cash position. Late game (lap 6), I can still buy affordable properties or those with high rent-to-price ratio since the game ends immediately.

When on START, I'll always collect my salary and include it in my balance calculation before declaring.

I will track my own book accurately at all times. My declared balance must be mathematically correct based on previous declaration plus all transfers and salary received/paid.

Early-game acquisition beats cash hoarding. In laps 1-3, if I can afford a property with at least 25 cash remaining, I should buy it. The rental income over many laps outweighs the upfront cost. Do not be overly conservative early on.

In lap 2, I bought Terrace (price 70, rent 14), which was correct. Early acquisition is the right strategy. I should have aimed to buy a third property in lap 3 if the opportunity arose with sufficient cash.

Late-game cash preservation was correct in lap 5 (I had only 33 cash, which is borderline), but in lap 6 I should reconsider: if I land on an unowned property I can afford, the final scoring is cash plus deed values. A property with high rent-to-price ratio might still improve my final score even if purchased on lap 6. However, at 47 cash and Exchange costing 120, I correctly could not afford it.

I will remember that the scoring metric is cash + deed values at the end. This means I should prioritize properties with strong rent-to-price ratios throughout the game, especially early when I can afford to build a portfolio.

Properties ranked by rent-to-price ratio: Exchange (30/120 = 25%), Foundry (24/100 = 24%), Wharf (18/80 = 22.5%), Mill (20/90 = 22%), Terrace (14/70 = 20%), Depot (10/50 = 20%), Quarry (12/60 = 20%). Target Exchange and Foundry early if possible.