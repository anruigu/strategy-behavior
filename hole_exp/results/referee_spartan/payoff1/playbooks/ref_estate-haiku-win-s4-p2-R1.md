---
game: ref_estate
model: haiku
condition: win
seed: 4
round: 1
chars: 1798
---
# Playbook for ref_estate

When I land on an unowned property, I need to evaluate whether to buy based on my current cash position and remaining laps. Buying properties generates rent income from other players, which is crucial to my final score. I should purchase properties when I have sufficient cash reserves to weather rent payments to other investors.

When I land on a property owned by another investor, I pay the rent due immediately and track my cash carefully.

When I pass or land on START, I collect my 25 salary and add it to my declared balance.

I keep rigorous track of my own cash at all times. After each turn, I declare my balance accurately by starting with my last declared balance, adding any salaries received, subtracting any rents paid, and subtracting any purchases made.

When evaluating a property purchase, I consider: (1) my current cash minus the purchase price should leave me with enough buffer for upcoming rent payments, (2) properties with higher rents are more valuable as the game progresses, (3) early in the game I should be more cautious about cash reserves, and (4) later in the game I should acquire remaining unowned properties if I have the cash, since owning more properties increases my final score.

I should not turn down property purchases too conservatively. In my previous game, I had cash available but was too hesitant to buy. The Exchange purchase at 120 was good, and the Quarry purchase at 60 was good. I should continue this pattern of acquiring properties when my cash position allows it.

My final score includes both my declared cash and the purchase prices of the deeds I hold. Therefore, owning properties matters as much as having cash reserves. I should balance these two components rather than hoarding cash or spending recklessly.