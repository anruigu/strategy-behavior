---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 1779
---
**Playbook for ref_estate**

When an unowned property is put to me and I can afford it after setting aside enough cash to cover likely rent payments on opponents' properties for the remaining laps, I buy it. The purchase is score-neutral (I lose cash but gain equal deed value), so the only real cost is the risk of being unable to pay future rent. The only real benefit is every rent payment I collect is pure score gain.

When I cannot afford a property, I pass. I do not skip a purchase I can afford in the hope of a better one later—any property I own that others land on is a free income stream, and there is no "better" property that makes a "worse" one worthless.

When I land on my own property, I do nothing except confirm my balance.

When I land on someone else's property, I pay the rent immediately and update my balance. I do not negotiate or refuse.

When I pass or land on START, I collect my salary and add it to my balance.

I keep my cash reserve by estimating how many times I expect to land on opponents' properties over the remaining laps and multiplying by the maximum rent on the board. If my cash after buying falls below that estimate, I decline the purchase. In practice, with a starting balance of 200 and a 25 salary, I can afford roughly two medium-priced properties while keeping a safe reserve.

I prioritize properties with higher rent-to-price ratios when I have a choice, because they generate more income per unit of risk. A property at 22% rent-to-price is more efficient than one at 15%.

I do not hold cash passively waiting for a "perfect" property. If I land on an unowned tile with a decent ratio and I can afford it, I buy. The game ends after a fixed number of laps; unused cash earns nothing, but owned properties earn rent every lap.