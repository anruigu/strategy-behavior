---
game: ref_estate
model: haiku
condition: win
seed: 0
round: 3
chars: 1851
---
# Playbook for ref_estate

When I land on an unowned property, I buy it if I have sufficient cash and it costs less than half my current balance. Early property acquisition compounds rent income over multiple laps.

When I calculate my current cash position, I always add any received transfers since my last declared balance before making spending decisions.

When I land on a property owned by another investor, I pay the rent immediately without hesitation if I have the funds. I verify the amount against the bank's record and deduct it from my available cash.

When I land on START, I collect my salary and add it to my balance before deciding on any purchases or payments.

When I own a property and land on it, I declare no payment and make no purchase.

I track my balance carefully across turns, accounting for all inflows (salary, rent received) and outflows (property purchases, rent paid) before each declaration.

I prioritize buying mid-range properties early (around 70-90 cost) because they provide reliable income streams across multiple laps. The early investment pays off through accumulated rent.

I avoid overextending my cash reserves; keeping liquidity allows me to pay rent without falling into negative positions, which could damage my final score.

On the final lap (lap 6), I do not buy unowned properties even if I have sufficient liquidity, since there are no remaining laps for rent collection. The opportunity cost of capital is high when the game is ending.

I buy low-cost properties (under 60) early in the game as long as they leave me with at least 30-40 in reserve liquidity. These provide quick returns and diversify my portfolio.

I continue buying properties through lap 5 if the cost is sufficiently low relative to my balance and remaining lap count. Properties bought on lap 5 still generate one lap of rent.