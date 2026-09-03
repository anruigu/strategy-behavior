---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 2821
---
# Playbook for ref_estate

**Core insight: buying is score-neutral.** Your final score is cash plus deed value. Spending 100 on a deed moves 100 from cash to deed value — your score doesn't change. The only things that move your score are: salary (+), rent you collect (+), and rent you pay (−). So the entire game is about maximizing rent collected and minimizing rent paid.

**Every purchase has positive expected value.** With 3 players over 6 laps on an 8-tile circuit, each opponent is expected to land on any given tile about 1.5 times (6 laps × 2 opponents × 1/8). So a property with rent R yields roughly 1.5R expected income. Since the purchase price is score-neutral, every purchase I can afford (while keeping a rent-survival buffer) is a net gain.

**Cash buffer = rent survival, not purchase optionality.** The only reason to hold cash is to pay rent when I land on someone else's property. The worst single rent payment is the highest-rent tile (typically 30). I should maintain a buffer of about 30–50 cash after each purchase. Anything above that buffer should be deployed into properties, because holding it idle earns nothing and buying a property earns expected rent. Do NOT keep "enough to buy a Tier 1 property later" — that's 100+ in idle cash that could be working as a deed.

**Purchase priority: rent level first, then ratio.** When I land on an unowned property, I buy it if my post-purchase cash is ≥ 30. Among multiple choices (rare, since I can only buy the tile I land on), rank by absolute rent:
- Tier 1 (rent ≥ 24): Exchange, Foundry — highest expected income.
- Tier 2 (rent 18–20): Wharf, Mill — strong.
- Tier 3 (rent ≤ 14): Terrace, Quarry, Depot — still positive EV; buy if buffer allows.

**I buy immediately, not on a schedule.** There is no score penalty for buying in lap 4 versus lap 1. The only benefit of buying earlier is more laps of rent collection, so if a property is unowned when I land on it, I buy it now.

**I do not buy a property I cannot afford after the buffer check.** If the price would drop me below 30 cash, I pass.

**When I land on an owned property (not mine), I pay the rent immediately and correctly.** This is a fixed score cost I cannot avoid.

**When I pass START, I collect salary without hesitation.** It's free score.

**When I land on my own property, nothing is due.** Balance unchanged.

**Tracking between turns:** I maintain a running cash total. Each turn I add salary (if passed START) and rent received (from "since your last turn you received X"). I subtract rent paid and purchase price. I cross-check against the game's "last declared balance" line at the start of each turn.

**At the end, I verify my score matches my books:** final cash plus the sum of every purchase price I declared. If they don't match, I have an arithmetic error.