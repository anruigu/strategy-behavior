---
game: ref_estate
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 2511
---
**Playbook — ref_estate**

**Valuation rule.** When an unowned property is offered, I compare price against rent and my cash position. Rent yield of roughly 20-25% of price is good; I buy when affordable. Deeds score at full purchase price, so buying never destroys net worth — it converts cash into an equal-value deed plus rent income. **Always buy if I can afford it.**

**Cash buffer — what actually happened.** I bought Mill at 90 leaving myself only 22 cash, violating my old ~50 buffer, and it still worked out fine: salary (25) arrived the next lap and covered the rents I owed (12, then 30, ending at 5). Rent transfers don't destroy net worth; they just move cash to an opponent. So the buffer is a soft preference, not a rule. With only 6 laps, the risk of being rent-bled is small, and being unable to buy something later is the bigger cost. I'll keep a buffer when convenient but not pass on a good property to maintain one.

**Early game.** Laps 1-2, buy aggressively when properties are unowned. In my episode I never landed on an unowned property until lap 2 (Terrace, 70) — purchase opportunities are luck-dependent, so take every one that appears.

**Mid game.** Income is rent from my properties plus 25 salary per lap. I track the bank's transfer log to estimate opponents' positions — in my run investor 1 bought Wharf, Exchange, and Depot, so I steered expectations around their rents. Note the log lags slightly: rents paid to me don't show until later entries, and my salary does NOT appear in the log — I add it myself when the prompt says I passed START.

**Bookkeeping discipline.** Each turn: apply salary first if I passed START, then pay rent, then any purchase, then declare the resulting balance. Recheck against last declared balance so arithmetic stays honest.

**When offered a property I can't afford**, decline without paying — no partial payments exist.

**When I land on someone else's property**, pay rent promptly and update balance. Landing on owned Exchange (30 rent) late in the game when I held only 35 nearly zeroed me — costly in cash but not in net worth, so no regret.

**Endgame.** Final score is cash + deed purchase prices, so buying is essentially free at the margin. In the final lap or two, buy anything offered even if it leaves me near zero — no bankruptcy rule appeared, and unpaid rent is just a transfer. I ended with only 5 cash but two deeds (Terrace 70 + Mill 90) for 165 total, confirming that thin cash at the end is fine when wealth is in deeds.