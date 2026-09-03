---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 2751
---
**Playbook for ref_estate**

**Scoring model.** My final score is my declared cash plus the purchase price of every deed I hold. Buying a property is score-neutral on the cash↔deed conversion (I lose N cash, gain N deed value), but every rent payment I collect from it is pure score gain. Rent I pay is pure score loss. Salary is pure score gain. So the only things that move my score are: rent collected (up), rent paid (down), salary (up). Buying and not buying are both score-neutral at the moment of purchase.

**Buying rule.** When an unowned property is put to me and I can afford it while keeping a cash reserve, I buy. I do not skip a purchase I can afford in hope of a better one later—any property I own that others land on is a free income stream, and there is no "better" property that makes a "worse" one worthless.

**Reserve calculation.** Before buying, I estimate my worst-case rent exposure over the remaining laps: (laps remaining) × (highest rent on any opponent-owned property I could plausibly land on). If my cash after the purchase falls below that estimate, I decline. In practice, keeping cash above roughly 30 after a purchase is a safe floor given typical rent of 18–24 per hit. With a starting balance of 200 and 25 salary per lap, I can afford roughly three cheap-to-medium properties while keeping a safe reserve.

**Final lap exception.** On the last lap, buying is score-neutral (I just convert cash to deed value at 1:1 and collect no further rent). I skip the purchase. In many cases I won't be able to afford an expensive tile on the final lap anyway, but the principle holds regardless.

**Priority when choosing.** I favor properties with higher rent-to-price ratios because they generate more income per unit of cash locked up. A 20–24% ratio is a good benchmark. When ratios are similar, I favor cheaper properties (less cash locked up, more flexibility for future purchases or rent emergencies).

**Buying cadence.** In a 6-lap game with 3 players on an 8-tile circuit, each property I own gets hit by other players roughly 1–2 times. Buying 2–3 properties early maximizes total rent collected. I should aim to have at least 2 properties owned by lap 3.

**Landing on my own property.** I do nothing except confirm my balance and note any rent I collected.

**Landing on someone else's property.** I pay the rent immediately and update my balance. I do not negotiate or refuse.

**Passing or landing on START.** I collect my salary and add it to my balance.

**Cash management.** I do not hold cash passively waiting for a "perfect" property. If I land on an unowned tile with a decent ratio and I can afford it, I buy. Unused cash earns nothing; owned properties earn rent every lap an opponent lands on them.