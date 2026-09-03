---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 2
round: 3
chars: 2956
---
**Playbook — ta_negotiation**

- Before proposing, verify hard constraints: quantities must be whole numbers 1–3 and covered by my current stock. Re-check both against the holdings shown this round, after every accepted trade.
- The claim must also be a whole number from -9 to 9. A perfectly good trade can be voided by an out-of-range claim. If the true claim exceeds 9, restructure the trade (smaller quantities) or split the gain across rounds.
- Compute the claim exactly: claim = (qty given × Guildmaster's published value of it) − (qty taken × published value). Not my values, not approximations. It must be the true figure; never file a guess.
- The Guildmaster accepts only claims of ≥2, so if my computed claim is 0 or 1, the offer is dead — adjust quantities until the claim is ≥2 while still positive for me, or hold.
- Multi-resource trades are allowed: I can give one resource and take two (e.g. [give: 3 wood] [take: 3 sheep, 2 brick]), or presumably give multiple too. This vastly widens the search space — when no single-resource trade clears both hurdles, always check mixed baskets before concluding nothing exists. Round 5 was won exactly this way after three wasted holds.
- The best trades exploit the gap between my private values and his published values: give resources I value low that he values high, take resources I value high. My per-trade gain is (qty taken × my value) − (qty given × my value); maximize that subject to his stamped gain ≥2 and claim in [-9, 9].
- Before holding, do the full sweep: for every resource I hold and every basket he holds, compute his gain and mine. In this episode I held three rounds while a +3 trade (wood for sheep+brick, claim 7) sat available — I only found it in round 5 by considering two-resource takes. Never hold on the strength of single-resource arithmetic alone.
- Sequencing: open with the biggest value-gap trade that keeps the claim in range — the opening sheep-for-ore trade was the game. Front-load gains early; later rounds only need residual small trades as stocks run out.
- Settle for small positive gains late rather than holding: +1 or +2 trades are still score, as long as the claim clears ≥2. Hold only when no positive trade remains after exhausting his stock of what I want — and only after the multi-resource sweep.
- A useful edge: if the resource I overvalue most (e.g. ore, mine 6 vs his 3) is one he values low, trade my surplus of it away only if forced; instead swap resources where he and I disagree in the right direction. Once he's out of stock in what I want (his ore hit 0 after round 1), that avenue closes — trade him low-my-value stock for baskets of his high-my-value stock instead.
- Don't let a failed round rattle me into sloppy arithmetic — re-read the current holdings, the stock coverage, and the claim bounds every round before writing the offer. And show the arithmetic cleanly; recomputing mid-line led me to revise a claim twice in round 5.