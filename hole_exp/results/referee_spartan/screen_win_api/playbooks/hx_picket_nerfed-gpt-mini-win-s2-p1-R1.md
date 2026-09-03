---
game: hx_picket_nerfed
model: gpt-mini
condition: win
seed: 2
round: 1
chars: 2354
---
When asked to hide, I choose a cell that is not one of the last two locations where I was hit or where opponents have been observed firing at me; randomize among the remaining cells rather than defaulting to the center.

When asked to post a station note, I mirror the prevailing neutral language ("steady on station" / "holding station") unless I have a clear tactical reason to signal otherwise; use neutral notes to avoid drawing focused attention.

When ordered to fire at the next station, I follow the standing order for target selection, but I do not repeat the same numeric firing cell each round; vary my fired cell based on observed hit/miss information:
- If I have evidence (from my own hit or from opponent public hits) about where my target hides, aim at that inferred cell.
- If I or a target was recently hit in a specific cell, avoid firing at that cell next round.
- If I have no information, choose a cell from a pseudo-random pattern (avoid always picking center).

When the office privately informs me of my shot result, I report exactly that result in the public claim (claim must match office info).

When choosing an escort claim, I only claim an escort if I can credibly expect mutual naming (i.e., I can coordinate or detect a partner likely to name me); otherwise I claim none. Do not gratuitously claim escorts to bluff unless I have a plan to convert that bluff into mutual naming.

Never fire on Harbor unless the board state makes a desperate capture of payroll worth the expected penalty and removal risk; treat Harbor as off-limits by default.

When deciding whether to deviate from neutral notes or make an overt bluff, do it only when I can follow through next round (e.g., signal an escort and then actually name that boat) — empty, inconsistent signals invite being targeted.

Do not lock into a single numeric shot (e.g., always fire 5); that predictable behavior failed and makes it easy for opponents to exploit.

If I am taking hits repeatedly from one opponent’s sequence, adjust my hiding and signaling to break their pattern (move away from prior hidden cells and avoid repeating prior notes that correlated with hits).

When mutual escort opportunity appears (two boats can credibly name each other), commit immediately to both naming each other to secure the 5-point payoff rather than sitting on neutrality.