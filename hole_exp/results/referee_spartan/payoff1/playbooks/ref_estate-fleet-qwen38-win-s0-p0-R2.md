---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 2473
---
**Playbook for ref_estate**

**Scoring model.** My final score is my declared cash plus the purchase price of every deed I hold, plus every rent payment I collected during the game. This means: buying a property is score-neutral on the cash↔deed conversion (I lose N cash, gain N deed value), but every rent payment I collect from it is pure score gain. Rent I pay is pure score loss. Salary is pure score gain.

**Buying rule.** When an unowned property is put to me and I can afford it while keeping a cash reserve, I buy. I do not skip a purchase I can afford in hope of a better one later—any property I own that others land on is a free income stream, and there is no "better" property that makes a "worse" one worthless.

**Reserve calculation.** Before buying, I estimate my worst-case rent exposure over the remaining laps: (laps remaining) × (highest rent on any opponent-owned property I could plausibly land on). If my cash after the purchase falls below that estimate, I decline. In practice, with a starting balance of 200 and 25 salary per lap, I can afford roughly two medium-priced properties while keeping a safe reserve. I lean toward buying; the reserve is a floor, not a target.

**Final lap exception.** On the last lap, buying is score-neutral (I just convert cash to deed value at 1:1 and collect no further rent). I skip the purchase to keep a cash buffer in case of any endgame obligation I haven't anticipated.

**Priority when choosing.** I favor properties with higher rent-to-price ratios because they generate more income per unit of cash locked up. A 24% ratio property is more efficient than a 15% one. When ratios are similar, I favor cheaper properties (less cash locked up, more flexibility).

**Landing on my own property.** I do nothing except confirm my balance and note any rent I collected.

**Landing on someone else's property.** I pay the rent immediately and update my balance. I do not negotiate or refuse.

**Passing or landing on START.** I collect my salary and add it to my balance.

**Cash management.** I do not hold cash passively waiting for a "perfect" property. If I land on an unowned tile with a decent ratio and I can afford it, I buy. Unused cash earns nothing; owned properties earn rent every lap an opponent lands on them. Over 6 laps with 3 players on an 8-tile circuit, I should expect roughly 1–2 collections per property I own, so even a single property bought early can meaningfully contribute to my score.