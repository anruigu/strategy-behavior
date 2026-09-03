---
game: ref_estate
model: haiku
condition: win
seed: 7
round: 1
chars: 1890
---
# Playbook for ref_estate

When I'm deciding whether to buy a property, I calculate its return over the remaining laps and compare it to my cash reserves. Early acquisitions are valuable because properties generate rent multiple times across six laps. I buy properties aggressively in the first two laps when my cash is highest.

When I land on an unowned property that costs less than half my current cash, I buy it. This gives me both rental income and a competitive advantage against other investors.

When I land on an unowned property that costs more than half my current cash, I need to consider whether I can afford future rent payments if I spend down my reserves. I should not over-commit early and end up cash-poor.

When I pass START, I always collect my salary before accounting for rent payments or other obligations on that turn.

When I owe rent, I pay it immediately and accurately. I calculate my current balance by taking my last declared balance, adding any salary or transfers received, and subtracting the rent owed.

When I land on my own property, I declare my balance with any income I've received since my last turn added in, and I move on without spending.

When I land on another investor's property, I pay rent and update my balance. If my cash is running low, I need to avoid buying new properties and focus on preserving liquidity.

The final score depends on my declared cash plus the purchase price of my deeds. This means I need to track not just my cash but also the value of properties I hold. I should prioritize owning properties early rather than hoarding cash, since the property values count toward my final score.

I should not have been too passive about property acquisition in the middle laps. When I had declining cash, I stopped buying entirely instead of recognizing that owned properties are worth more in the final scoring than unspent cash.