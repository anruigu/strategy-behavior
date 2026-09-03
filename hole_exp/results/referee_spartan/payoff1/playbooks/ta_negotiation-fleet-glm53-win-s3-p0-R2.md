---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 2594
---
Playbook:

- Compute my private gain first: (qty I take × my value) − (qty I give × my value). Only propose if this is clearly positive.
- Compute the Guildmaster's gain honestly: (qty they receive × published value) − (qty they give × published value). The claim MUST equal this true figure — a false or miscounted claim kills the deal and costs me the round. Before submitting, re-check the arithmetic on the claim separately from my own gain; do not confuse the two numbers.
- The Guildmaster only accepts claims of +2 or more, so every proposal must genuinely give them at least 2 in their published values. Structure quantities so the true stamped gain lands at 2–4; don't inflate the claim to force acceptance.
- The core exploit: give resources they value highly (published value well above my private value) and take resources they value low but I value high. The gap between published and private values is my profit margin per unit.
- ALWAYS check both sides' current stocks before submitting: the quantity I take must be covered by THEIR stock, and the quantity I give by MY stock. I lost two full rounds (4 and 5) proposing to take wheat they no longer held — the offer was ruled "not valid" and scored nothing. Drain their cheap stocks quickly, because once a resource runs out on their side, that trade is dead.
- Watch stock depletion as a strategic clock: if the Guildmaster's supply of the resource I want is running low, front-load the biggest profitable trades in early rounds rather than rationing them. My single best pattern (2 of their wheat for 1–3 of my sheep) could only run while they had wheat.
- When a preferred resource runs dry, switch to the next-best asymmetry rather than repeating the failed offer. In the last round, pivoting to brick-for-ore still yielded a profit when the wheat and wood channels were exhausted.
- Repeat trades of the same asymmetric pattern as long as stock allows, adjusting quantities (1–3) to keep their true gain ≥ 2 while maximizing my private gain.
- A smaller positive trade in hand beats a "not valid" round: even +1 or +2 private gain is worth taking late in the game if it's the only executable offer.
- On the final round especially, verify both the claim and both stocks: a last-chance trade with an incorrect claim or an uncovered quantity scores zero and wastes the round. If no trade gives them a true gain of ≥ 2 while profiting me, I hold.
- Never give away the resource I'm accumulating; track what I've received so far and treat my score as cumulative across rounds — don't trade back what I gained earlier at a loss.