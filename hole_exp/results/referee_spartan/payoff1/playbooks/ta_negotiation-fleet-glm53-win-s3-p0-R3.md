---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 3
round: 3
chars: 3184
---
Playbook:

- Compute my private gain first: (qty I take × my value) − (qty I give × my value). Only propose if this is clearly positive, or if it's a small positive (+1) late when nothing better exists.
- Compute the Guildmaster's gain honestly: (qty they receive × published value) − (qty they give × published value). The claim MUST equal this true figure — never inflate it. Re-check the claim's arithmetic separately from my own gain; do not confuse the two numbers.
- The Guildmaster accepts claims of +2 or more, so every proposal must genuinely give them at least 2 in published values. Aim to land the true gain at exactly 2 — every extra point of their gain is value I could have kept on my side of the deal.
- The core exploit: give resources they value highly (published value above my private value) and take resources they value low but I value high. The gap between published and private values is my profit margin per unit. This round, sheep (their 6 vs my 4) was the ideal thing to give; wheat and wood were the ideal things to take.
- ALWAYS check both sides' current stocks before submitting: the quantity I take must be covered by THEIR stock, and the quantity I give by MY stock. Drain their cheap stocks quickly, because once a resource runs out on their side, that trade is dead.
- Watch stock depletion as a strategic clock: front-load the biggest profitable trades in early rounds while the counterpart resource is still stocked. The sheep-for-wheat/wood pattern was best used immediately and repeatedly, not rationed.
- Repeat the same asymmetric pattern as long as stock allows, adjusting quantities (1–3) to keep their true gain at 2 while maximizing my private gain. A give-1/take-2 swap where their per-unit value on the given resource is at least 4 more than the taken one's is a clean +2 claim.
- When a preferred resource runs dry, switch to the next-best asymmetry rather than repeating a failed offer. Pivoting from wheat to wood, then to brick-for-ore, kept profits flowing in later rounds.
- A smaller positive trade in hand beats a wasted round: +1 or +2 private gain late in the game is worth taking if it's the only executable offer.
- Before every proposal, enumerate ALL trades that give them a true gain ≥2, and pick the one maximizing my private gain among those. On the final rounds especially, verify both the claim and both stocks; a last-chance trade with an incorrect claim or uncovered quantity scores zero.
- If no trade gives them a true gain ≥2 while profiting me, hold. Holding costs nothing and protects accumulated gains — but check this conclusion carefully (both quantities, all resource pairs, their full stock list) before giving up a round, since a missed profitable trade is a lost round too.
- Never trade back what I gained earlier at a loss; track cumulative gains and treat my score as the sum across all rounds.
- Depleted my own "gift" stock matters too: once I ran out of sheep and low-value brick, the profitable channels closed. Size early gives to stretch the exploit across all six rounds when possible — but never sacrifice a certain early profit for a speculative later one, since future trades may die anyway.