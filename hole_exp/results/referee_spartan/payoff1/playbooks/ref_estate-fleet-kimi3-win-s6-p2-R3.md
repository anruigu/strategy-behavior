---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 6
round: 3
chars: 3911
---
## My ref_estate playbook

**Core accounting discipline**
- I always recompute my balance from scratch each turn: last declared balance + salary (if I passed START) + any "since your last turn you received N" income − rent paid − purchase price. I never trust memory alone; I recount before declaring [balance: N], since a wrong declaration is a self-inflicted wound.
- The "Since your last turn you received N from other investors" line is real income I must add — in both episodes where it appeared it was easy to overlook. I scan for it every turn before computing.
- I check the "last declared balance" line and the prompt's salary flag before writing anything. If I passed START, I add 25 even on the lap I cross it.
- I only declare [pay: N to Pk] when the prompt explicitly names an owner and a rent figure. Landing on my own deed, START, or an unowned tile means [pay: none].
- I never offer [buy: yes] on a tile already owned — it's invalid and signals sloppiness.

**Buying rule: deeds are nearly free money**
- Buying converts cash 1:1 into deed value, so my net worth never drops from a purchase itself. The only real cost is rent-risk from holding less cash.
- Default position: if a tile is unowned and I can afford it, I buy it. This held up again: buying Depot for 50 (146 → 96) and Mill for 90 (117 → 27 effective) never put me in danger, and my final score of 157 reflected every deed at full purchase value.
- Cushion rule: before buying, I total the rents I could plausibly owe before my next salary pass from tiles owned by others. I skip a purchase only if buying would leave me short of that total — not of a single worst-case rent. With salary of 25 per circuit, even a near-zero balance recovers.
- If cash is tight and I must choose among tiles, I prioritize the highest-rent one available; once the board sells out, collecting rent from others is the only way to grow net worth.
- If I can't afford an unowned tile, that's fine — I declare [buy: no] and note it for a later lap if it stays unowned.

**Endgame rule**
- On the final lap, cash and deeds count identically and there is no future rent to fear. I buy every unowned tile I can afford, emptying my wallet if necessary — zero downside. In this episode I bought Mill for 90 down to 17 cash, and the deed's full 90 counted in my final tally. Confirmed: cash is never safer than a deed at the end.
- On the final lap I also add any salary from passing START and any announced income before settling, since both count in the final score.

**Salience checks each turn**
- I scan the recent-transfers log to know who owns what, so I can anticipate rent I'll owe on my next roll and size my cushion accordingly.
- I note which opponents hold which deeds: my rent payments inflate their final score, so when everything else is equal I prefer minimizing payments to the current leader — the roll decides where I land, but this informs whether my cushion must truly cover a given tile and how urgently I should outbuy them.
- I track total board composition: if most deeds are already sold by mid-game, future rent risk is high and I raise the cushion slightly; conversely, cheap unowned tiles late in the game are nearly free points and I grab them.

**Format discipline**
- I put brief reasoning FIRST and the three bracketed tokens LAST, each on its own line, exactly: [pay: ...] (or [pay: none]), [buy: yes/no], [balance: N]. Tokens always close the message, no trailing text — the reply must end with the final token or it risks a parse failure.

**What I will not do again**
- I will not pass on a deed purely out of cash anxiety when salary is still coming — aggressive buying paid off in every episode so far.
- I will not append any text after the final [balance: N] token.
- I will not skip adding salary on a pass-START turn, nor the "since your last turn you received N" income lines — both are direct, easily missed score.