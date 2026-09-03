---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 1606
---
# Playbook: Ref Estate

When I land on an unowned property and can afford it, I weigh the rent-per-price ratio and my remaining laps against the price. I buy cheap properties only if I can still afford a high-rent property later in the game. Since buying is score-neutral (cash converts 1:1 into deed value), the only upside to buying is rent income from others landing on my tiles.

When multiple unowned properties are available across the game, I prioritize the ones with the highest rent-to-price ratio and the ones I expect others to hit most often. A 120-property paying 30 rent beats a 50-property paying 10 rent, even if I have to wait an extra lap to afford it.

When I land on someone else's property, I pay the rent immediately and don't second-guess it. I keep my arithmetic clean: last declared balance minus rent equals new balance.

When I pass START, I add 25 to my balance and record it.

When I cannot afford a property, I simply decline and keep my balance unchanged. I do not buy what I cannot pay for.

I track my own running total of cash after every transaction and make sure my declared balance always reflects: starting 200, minus all rents paid, minus all purchases, plus all salaries collected. I double-check the arithmetic before declaring.

**What went wrong last time:** I spent 50 on a low-rent tile (10 rent) early, which left me unable to afford a high-rent tile (30 rent) on the final lap. The net score was the same either way, but I missed the rent-income opportunity. Next time, I hold cash for the big purchase unless the cheap tile has a genuinely strong rent ratio.