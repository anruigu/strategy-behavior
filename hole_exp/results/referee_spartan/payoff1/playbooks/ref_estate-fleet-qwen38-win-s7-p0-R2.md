---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 2944
---
# Playbook for ref_estate

**Core insight: buying is score-neutral.** Your final score is cash plus deed value. Spending 100 on a deed moves 100 from cash to deed value — your score doesn't change. The only things that move your score are: salary (+), rent you collect (+), and rent you pay (−). So the entire game is about maximizing rent collected and minimizing rent paid.

**Purchase priority: rent level first, then ratio.** Rank properties by absolute rent. In an 8-tile circuit with 3 players over 6 laps, each opponent has roughly 6/8 ≈ 0.75 expected visits per property per lap, so a 24-rent property is worth about 2×1.5 ≈ 36 expected rent over 3 laps, while a 10-rent property is worth about 15. The gap matters. Concretely, I prioritize:
- Tier 1 (rent ≥ 24): Exchange, Foundry — buy on first chance.
- Tier 2 (rent 18–20): Wharf, Mill — buy if cash allows.
- Tier 3 (rent ≤ 14): Terrace, Quarry, Depot — buy only if I have surplus cash after covering Tier 1–2.

**Cash buffer = option value, not score protection.** Since buying is score-neutral, holding cash doesn't protect my score. The only reason to keep cash is to afford a Tier 1 or 2 property if one comes up later. Guideline: after each purchase, keep enough to buy one more property in the 80–120 range. If buying a Tier 3 property would leave me unable to afford a Tier 1 property that appears next lap, skip it.

**I buy on the lap a good property comes up, not on a fixed schedule.** There is no score penalty for buying in lap 4 versus lap 1 (deed value is the same). The only benefit of buying earlier is more laps of rent collection. So: if a Tier 1 property is unowned when I land on it, buy it immediately regardless of lap. For Tier 2, buy if my cash buffer rule above is satisfied. For Tier 3, only buy if I'm confident no Tier 1 or 2 property will come up in the remaining laps, or if I already own all higher tiers.

**I do not buy a property I cannot afford.** No leverage, no IOUs. If the price exceeds my cash, I pass.

**When I land on an owned property (not mine), I pay the rent immediately and correctly.** Check the bank's records for the owner. The rent is a fixed score cost.

**When I pass START, I collect salary without hesitation.** It's free score. Add it to my running balance before handling rent or purchases.

**When I land on my own property, nothing is due.** No rent, no purchase opportunity. Balance unchanged.

**At the end, I verify my score matches my books:** final cash plus the sum of every purchase price I declared. If they don't match, I have an arithmetic error somewhere.

**Tracking between turns:** I maintain a running total of my cash. Each turn I add: salary (if passed START), rent received (from other players landing on my properties). I subtract: rent paid (if I landed on someone else's property), purchase price (if I bought). I cross-check against the "since your last turn you received X" line the game provides.