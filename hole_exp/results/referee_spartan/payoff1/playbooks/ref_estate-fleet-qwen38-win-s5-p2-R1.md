---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 5
round: 1
chars: 1878
---
# Playbook

**On buying:**
- When an unowned property is offered and I can afford it, compare its rent-to-price ratio against the other unowned properties still on the board. Buy only if its ratio is at or near the top of what's available. Higher ratios (like Exchange or Foundry) are strictly better than lower ones (Quarry, Depot, Terrace) even if the absolute rent is smaller.
- Never let my cash drop below the price of the next-highest-ratio unowned property I might reasonably land on in the remaining laps. In practice: after each purchase, check whether I can still afford at least one more good property. If the answer is no, I overextended.
- A property bought earlier earns rent for more laps. If two properties have similar ratios, prefer the one I can buy sooner.

**On cash management:**
- Track my expected rent outflow: count how many properties others own and what their rents are. Each lap I have roughly a 1/8 chance per owned tile of hitting it. Keep enough reserve to cover 2–3 laps of likely rent without going broke.
- When I pass START, the salary is guaranteed income—never skip declaring it.

**On rent payments:**
- When I land on an owned property, pay the rent immediately and update my balance. Do not round or estimate; use the exact rent listed for that tile.

**On what did not work:**
- In my last run I bought two properties in the first two laps, spending 80% of starting cash, which left me unable to buy when I landed on a high-ratio property later and forced me to pay rent with almost no buffer. The fix: cap early purchases so that after my second buy I still hold at least the price of the best remaining unowned tile.
- I should not treat "I can afford it" as sufficient justification to buy. The real question is whether buying it leaves me in a position to also buy a better tile later, or whether it strands me as a rent-payer only.