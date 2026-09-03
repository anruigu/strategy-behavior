---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 2932
---
# Playbook: ref_estate

**Core principle:** Buying a property doesn't change my net worth (cash − price, deed + price = same total). The game is won by net rent collected. So my only real objective is to own the properties that generate the most rent from others, while avoiding or minimizing rent I pay to others.

**When an unowned property is available and I have cash:**
- Buy it if the rent-to-price ratio is decent (≥ 15% per lap). Over 6 laps with 2 opponents, I expect each property to be landed on ~2 times, so expected income ≈ 2 × rent.
- Prioritize by absolute expected income (2 × rent), then by ratio. Exchange (30) and Foundry (24) are the top targets; Depot (10) and Wharf (12) are the bottom.
- Don't hoard cash. Cash is dead weight. If I can buy and still keep enough to survive likely rent payments, buy.
- Rule of thumb for cash reserve: I'll pay rent on roughly 2–3 of my 6 laps. Keep enough for the highest rent I might face (usually 20–30) plus a small buffer.

**When I land on someone else's property:**
- Pay the rent. Track it. No negotiation, no option.
- If the property is cheap relative to its rent (e.g., I'm paying 20 on a 90-price property), note that the owner is building a strong asset. I can't do anything about it, but I should factor it into whether I want to keep buying more properties (spreading my rent income) or conserve.

**When I pass START:**
- Collect salary immediately. Never skip this. It's free money that compounds into my cash buffer.

**When I land on my own property:**
- Do nothing. No payment, no purchase. Just confirm balance is unchanged.

**Endgame (lap 5–6):**
- If I still have unspent cash and an unowned property is available, buy it only if I expect at least one more opponent to land on it (i.e., at least 1 lap remains with 2 opponents still rolling). Otherwise, holding cash is equally good as holding a deed.
- Do NOT buy a property in the very last lap unless an opponent is guaranteed to land on it (impossible to guarantee).

**Tracking:**
- After every turn, verify: my cash = last balance + salary collected + rent received − rent paid − purchase price. State the number explicitly.
- Keep a running tally of my total net rent (received minus paid). At the end, my score = 200 + total net rent + salary collected. This lets me sanity-check my final answer.

**What went wrong in my play:**
- I bought Wharf (ratio 15%) when I could have prioritized it over Terrace (ratio 20%) if both were available simultaneously. In practice both were available on different laps so this didn't matter, but going forward I should buy the highest-ratio unowned tile first when I have a choice in the same lap.
- I did not actively look for a third property to buy. If I had a buy opportunity mid-game (e.g., landing on an unowned tile with enough cash), I should have taken it even at a low ratio, because the marginal cost in cash is small relative to the rent stream.