---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 4054
---
# Playbook: ref_estate

**Core principle:** Buying a property doesn't change my score (cash − price, deed + price = same total). Score = final cash + sum of deed prices = 200 + total salary collected + total net rent (received − paid). The only way to increase my score is to collect salary and net rent. Every purchase is a bet that the property will generate rent from opponents before the game ends.

**When an unowned property is available and I have cash:**
- Buy it if the rent-to-price ratio is ≥ 15% per lap. Over 6 laps with 2 opponents, I expect each property to be landed on ~2 times, so expected income ≈ 2 × rent.
- Prioritize by absolute expected income (2 × rent), then by ratio. Exchange (30) and Foundry (24) are the top targets; Depot (10) and Wharf (12) are the bottom.
- **Cash reserve rule depends on how many properties I already own:**
  - Buying my **first** property: keep a reserve of at least 50. I have no income stream yet, so I need to survive potential rent payments until I either collect salary or (if I've already bought) receive rent.
  - Buying a **second or third** property: I can go to 0 or near 0. Existing properties make it very likely I'll receive rent within 1–2 laps, which funds survival. In practice, with 2 opponents rolling each lap, the chance of at least one hitting my property is high. Going all-in on a high-ratio buy (e.g., Exchange at 25%) is fine when I already have one or more income-generating properties.
- Don't hoard cash. Cash is dead weight in the score formula.
- Owning multiple properties has a compounding benefit: each additional property increases the chance that at least one opponent lands on my property in a given lap. Three properties is the sweet spot — it gave me 295 (45 cash + 250 in deeds) in my last game.

**When I land on someone else's property:**
- Pay the rent. Track it. No negotiation, no option.

**When I pass START:**
- Collect salary immediately. Never skip this.

**When I land on my own property:**
- Do nothing. No payment, no purchase. Just confirm balance.

**Endgame (laps 5–6):**
- If I still have unspent cash and an unowned property is available in lap 5, buy it if I expect at least one opponent to land on it in lap 6 (one more roll from each of 2 opponents). The expected value is still positive.
- Do NOT buy in the very last lap (lap 6). No opponent will get another turn after me, so the deed generates zero additional rent. Cash and deed are score-equivalent, so there's no benefit to spending.
- In practice, if I've already bought three properties, I likely won't have enough cash for a fourth buy in the endgame anyway.

**Tracking:**
- After every turn, verify: my cash = last balance + salary collected + rent received − rent paid − purchase price. State the number explicitly.
- Keep a running tally of my total net rent (received minus paid). At the end, my score = 200 + total net rent + salary collected. Sanity-check against cash + deed values.

**Lessons from play:**
- Going to 0 on a second buy (Exchange) was fine because I collected 30 in rent the very next lap. The "keep a 40–50 reserve" rule is too conservative once I have an existing income stream. The real question is: can I survive until my next expected income event? With one property already generating rent, the answer is almost always yes.
- Three properties = 295 score. The marginal value of a third property (Depot, 50 cost, 10 rent) was positive: it generated 10 in rent and added 50 to my deed total. Net score impact: +10 from rent. Always worth it if I can afford it.
- I never paid rent to anyone in this game, which was lucky but also a function of owning three spread-out properties (Wharf, Exchange, Depot) that don't cluster on the same side of the board. If I get the chance to buy properties that are spread across the circuit, prefer that over clustering — it means opponents are more likely to hit at least one of mine per lap.
- The 15% threshold is fine. All three buys (22.5%, 25%, 20%) were comfortably above it and all generated positive returns.