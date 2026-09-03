---
game: ref_estate
model: fleet-glm53
condition: win
seed: 4
round: 1
chars: 1270
---
Playbook for ESTATE:

- Scoring is cash plus purchase price of deeds held, so buying property is roughly cash-neutral in scoring terms but earns rent on top. Property is the better use of cash whenever I can afford it without going broke.
- When I land on an unowned tile, buy it unless the price would leave me too little cash to cover likely rents (roughly one lap's worth of rent, ~25-40) before my next salary.
- When the final laps arrive, drop the cash cushion: buying a property on the last lap is nearly free scoring-wise (cash converts 1:1 into deed value) and rent can still come in. If a late buy leaves me near zero, that's fine — rent shortfalls just cost what I actually hold, and I'll collect salary on passing START.
- Don't buy so aggressively mid-game that I can't pay rent; ending a turn with only single-digit cash is fine only near the end.
- Always include all three tokens exactly, with balance updated correctly (subtract rent and purchase price, add 25 salary when passing START). If rent exceeds my cash, pay my remaining cash and declare zero.
- Track the board from the bank's book: note which opponents own which tiles to estimate my expected rent exposure, and prefer buying high-rent tiles (Exchange, Foundry) that opponents land on often.