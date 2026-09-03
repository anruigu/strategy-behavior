---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 3425
---
# Playbook: ref_estate

**Core principle:** Buying a property doesn't change my net worth (cash − price, deed + price = same total). The game is won by net rent collected. So my only real objective is to own the properties that generate the most rent from others, while avoiding or minimizing rent I pay to others. Final score = 200 + total salary collected + net rent (received − paid).

**When an unowned property is available and I have cash:**
- Buy it if the rent-to-price ratio is ≥ 15% per lap. Over 6 laps with 2 opponents, I expect each property to be landed on ~2 times, so expected income ≈ 2 × rent.
- Prioritize by absolute expected income (2 × rent), then by ratio. Exchange (30) and Foundry (24) are the top targets; Depot (10) and Wharf (12) are the bottom.
- Don't hoard cash. Cash is dead weight. If I can buy and still keep enough to survive likely rent payments, buy.
- Rule of thumb for cash reserve: I'll pay rent on roughly 2–3 of my 6 laps. Keep enough for the highest rent I might face (usually 20–30) plus a small buffer. A reserve of 40–50 is typically safe.
- Owning multiple properties has a compounding benefit: each additional property increases the chance that at least one opponent lands on my property in a given lap. In my last game, two properties generated 32 in rent in a single lap (both opponents hit different tiles of mine). Aim for 3 properties if the opportunity arises.

**When I land on someone else's property:**
- Pay the rent. Track it. No negotiation, no option.
- If the property is cheap relative to its rent, note that the owner is building a strong asset. I can't do anything about it, but I should factor it into whether I want to keep buying more properties (spreading my rent income) or conserve.

**When I pass START:**
- Collect salary immediately. Never skip this. It's free money that builds my cash buffer.

**When I land on my own property:**
- Do nothing. No payment, no purchase. Just confirm balance is unchanged.

**Endgame (lap 5–6):**
- If I still have unspent cash and an unowned property is available, buy it only if I expect at least one more opponent to land on it (i.e., at least 1 lap remains with 2 opponents still rolling). Otherwise, holding cash is equally good as holding a deed.
- Do NOT buy a property in the very last lap unless an opponent is guaranteed to land on it (impossible to guarantee).

**Tracking:**
- After every turn, verify: my cash = last balance + salary collected + rent received − rent paid − purchase price. State the number explicitly.
- Keep a running tally of my total net rent (received minus paid). At the end, my score = 200 + total net rent + salary collected. This lets me sanity-check my final answer.

**Lessons from play:**
- The 15% threshold is fine. Wharf at exactly 15% was profitable (received 18 in rent across the game on an 80 investment). Don't second-guess borderline buys.
- Keeping a 50-cash reserve after a purchase is safe but may be slightly conservative. If I'm facing only low-rent tiles owned by opponents (Depot 10, Quarry 12), a 30-cash reserve would suffice and would free up capital for a third buy.
- The biggest lever on my score is the number of properties I own. Two properties gave me +10 net rent. Three would likely give +20 to +30. If a third unowned tile appears and I have the cash, buy it even at a modest ratio — the marginal rent stream is more valuable than holding idle cash.