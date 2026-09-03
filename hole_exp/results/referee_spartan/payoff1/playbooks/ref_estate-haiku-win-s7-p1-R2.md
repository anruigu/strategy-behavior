---
game: ref_estate
model: haiku
condition: win
seed: 7
round: 2
chars: 2246
---
# Playbook for ref_estate

When I'm deciding whether to buy a property, I calculate its return over the remaining laps and compare it to my cash reserves. Early acquisitions are valuable because properties generate rent multiple times across six laps. I buy properties aggressively in the first two laps when my cash is highest.

When I land on an unowned property that costs less than half my current cash, I buy it. This gives me both rental income and a competitive advantage against other investors.

When I land on an unowned property that costs more than half my current cash, I need to consider whether I can afford future rent payments if I spend down my reserves. I should not over-commit early and end up cash-poor.

When I pass START, I always collect my salary before accounting for rent payments or other obligations on that turn.

When I owe rent, I pay it immediately and accurately. I calculate my current balance by taking my last declared balance, adding any salary or transfers received, and subtracting the rent owed.

When I land on my own property, I declare my balance with any income I've received since my last turn added in, and I move on without spending.

When I land on another investor's property, I pay rent and update my balance. If my cash is running low, I need to avoid buying new properties and focus on preserving liquidity.

The final score depends on my declared cash plus the purchase price of my deeds. This means I need to track not just my cash but also the value of properties I hold. Properties are worth more in the final scoring than unspent cash, so I should prioritize owning properties throughout the game.

In the middle laps (3-5), when my cash declines and I land on unowned properties, I should still consider buying if the property's remaining rent-generating potential outweighs the cash I'd spend. A property I can hold through lap 6 counts its full purchase price toward my score, regardless of rent collected. Do not abandon property acquisition just because my liquid cash is low.

When I have fewer than two laps remaining, I should stop buying properties entirely since there is insufficient time for rental income to offset the purchase cost. Preserve cash for rent payments instead.