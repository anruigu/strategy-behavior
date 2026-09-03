---
game: ref_estate
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 1442
---
**Playbook for estate auction game**

When I land on an unowned property and have enough cash, I buy it unless the price is clearly bad value. Judge value by rent-to-price ratio and by location on the circuit — a tile I'm likely to land on myself or deny to rivals is worth more. Early in the game, buying is nearly always right: cash left idle earns nothing, and every property bought is one fewer rent stream for opponents.

When buying, I always pay the bank, keep the books straight, and declare the exact post-purchase balance. When I pay rent, I pay the owner exactly and decrement my balance accordingly.

When I pass START, I collect the salary first and include it in my declared balance. When a notice says I received money from other investors since my last turn, I add it to my last declared balance before applying this turn's dues — forgetting this is an easy way to misreport.

I should not buy properties so expensive that I can't absorb rent later, but in a 6-lap game liquidity risk is low and property counts at full purchase price in the final score, so aggressive early buying is the winning posture.

When the final lap approaches, if any purchase opportunity remains, I take it even late — purchase price converts 1:1 into final score, so unspent cash is wasted only if nothing is available to buy.

Watch the bank's transfer log to track which tiles are owned by whom, and prefer buying tiles opponents will hit often.