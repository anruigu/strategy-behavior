---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 6
round: 2
chars: 3456
---
## My ref_estate playbook

**Core accounting discipline**
- I always recompute my balance from scratch each turn: last balance + salary (if I passed START) − rent paid − purchase price. I never trust memory alone; I recount before declaring [balance: N], since a wrong declaration is a self-inflicted wound.
- I check the "last declared balance" line and the prompt's salary flag before writing anything. If I passed START, I add 25 even on the lap I cross it.
- I only declare [pay: N to Pk] when the prompt explicitly names an owner and a rent figure. Landing on my own deed, START, or an unowned tile means [pay: none].
- I never offer [buy: yes] on a tile already owned — it's invalid and signals sloppiness.

**Buying rule: deeds are nearly free money**
- Buying converts cash 1:1 into deed value, so my net worth never drops from a purchase itself. The only real cost is rent-risk from holding less cash.
- Default position: if a tile is unowned and I can afford it, I buy it. This was borne out: buying Exchange for 120 left me at 42 cash, and the small cushion (three potential rent hits of 24–30 never materialized at once) carried me through. Aggression paid.
- Cushion rule: before buying, I total the rents I could plausibly owe before my next salary pass. I skip a purchase only if buying would leave me short of that total — not of a single worst-case rent. With several laps left and salary of 25 per circuit, even a near-zero balance recovers.
- If a purchase would leave me short, I prioritize the highest-rent tile available; when cash is tight, rent collection from others is the only way to grow net worth after the board sells out.
- If I can't afford an unowned tile (as with Mill at 42 cash), that's fine — I declare [buy: no] and note it for a later lap if it stays unowned.

**Endgame rule**
- On the final lap, cash and deeds count identically and there is no future rent to fear. I buy every unowned tile I can afford, emptying my wallet if necessary — there's zero downside. Also on the final lap I add any salary from passing START before settling, since it counts in the final tally.

**Salience checks each turn**
- I scan the recent-transfers log to know who owns what, so I can anticipate rent I'll owe on my next roll and size my cushion accordingly.
- I note which opponents hold which deeds: my rent payments inflate their final score, so when everything else is equal I prefer routes/behavior that minimize paying the current leader — though the roll decides where I land, this matters when choosing whether a cushion truly must cover a given tile.
- I track total board composition: if most deeds are already sold by mid-game, future rent risk is high and I moderate the cushion upward slightly.

**Format discipline**
- I put brief reasoning FIRST and the three bracketed tokens LAST, each on its own line, exactly: [pay: ...] (or [pay: none]), [buy: yes/no], [balance: N]. In one episode I put reasoning after the tokens — that risks a parse failure since the reply must end with the tokens. Tokens always close the message, no trailing text.

**What I will not do again**
- I will not pass on a deed purely out of cash anxiety when salary is still coming — the Exchange purchase at 42 cash remaining was the right call and I'll make that call again.
- I will not append any text after the final [balance: N] token.
- I will not skip re-adding salary on a pass-START turn; that +25 was easy to miss and direct score.