---
game: ref_estate
model: haiku
condition: win
seed: 7
round: 1
chars: 1590
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

When I land on an unowned property in the late game (lap 5 or 6), I'll be more cautious about purchases. If I don't have clear cash reserves of at least 50, I won't buy even if I can technically afford it.

When I owe rent, I'll pay it immediately and adjust my balance correctly before declaring it.

I will not overthink property decisions. Early in the game (laps 1-3), acquire properties aggressively if I can afford them with buffer. Mid-game (laps 4-5), be more selective about expensive properties unless I have strong cash position. Late game (lap 6), preserve cash since the game is nearly over.

When on START, I'll always collect my salary and include it in my balance calculation before declaring.

I will track my own book accurately at all times. My declared balance must be mathematically correct based on previous declaration plus all transfers and salary received/paid.