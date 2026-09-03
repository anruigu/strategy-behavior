---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 0
round: 3
chars: 4496
---
**Playbook**

- Before proposing any trade, compute two numbers: my net gain = (qty taken × my private value) − (qty given × my private value), and the Guildmaster's gain = (qty I give × their published value) − (qty they give × their published value). Only propose if MY gain is clearly positive — +3 or more preferred, +2 acceptable late if no better edge exists.

- Never trade away resources with high private value to me just because the Guildmaster values them highly too. A trade can be attractive to the counterparty and still be a loss for me. Check my side of the arithmetic independently every time.

- The claim is the Guildmaster's true net gain in their published values, and they accept at ≥2. So the claim is not a lever — it must be the honest arithmetic. My job is to find trades where their honest gain is ≥2 AND my private gain is positive.

- The sweet spot: give resources that are cheap to me but expensive to them (my value low, their published value high), take resources that are valuable to me (my value high, their value low or moderate). Rank resources by (their published value − my private value): sell my resources with the biggest gap, buy resources where my private value exceeds theirs. Selling low-value-to-them resources to buy high-value-to-them ones also works when my own gap favors it.

- THE BIGGEST LESSON FROM THIS EPISODE: an invalid offer is a silently burned round, and I burned three of six. Validity means ALL of: qty 1–3 whole numbers, give covered by MY current stock, AND take covered by THEIR current stock. In round 2 I tried to take 3 wood when the Guildmaster held only 2 — invalid. In round 5 I tried to give 2 brick when I held only 1 — invalid. Re-read BOTH holdings lines immediately before writing the offer, every single time, and check every quantity against them.

- Holdings change only on accepted trades, but my mental picture can drift anyway — after any invalid round the positions are unchanged, yet I still misread them. Never write quantities from memory; always look at the current table and verify "I hold ≥ give qty" and "they hold ≥ take qty" explicitly before finalizing.

- When the Guildmaster's stock of a resource I want runs low or hits zero, stop trying to take it. After round 4 their wood went to 0 — any further wood-taking offer was doomed. Track their depleting stocks and switch targets.

- Compute the claim freshly every time: their gain = qty given × their value − qty taken × their value. Even if arithmetic is right, the offer dies if stocks don't cover it, so the stock check is the one that actually bit me — do it first, before even choosing the trade.

- If no trade gives me positive private gain with their honest gain ≥2 and full stock coverage, say [hold: yes]. A hold costs 0; a bad or invalid trade wastes the round or worse. But before holding, scan systematically: for each resource pair (give R1, take R2) with stocks available, compute both gains — the profitable pair is often not the obvious one.

- My score is the running total of my net private gains across accepted trades. Protect the accumulated total — late rounds with no edge are for holding, not for forcing trades out of momentum. This episode: 3 accepted trades (+8, +6, +2) = +16, but three burned rounds left value on the table; with valid offers throughout, several more profitable trades were available.

- Watch the "trading gains" tracker after each round: if my total did not move after a proposal, the offer was invalid — diagnose which constraint failed (stock coverage on either side, quantity range, claim) before the next round, since the same mistake will repeat otherwise.

- One trade per round, six rounds, quantities capped at 3: prefer several small profitable trades over one big one. Up to six accepted trades are possible; every invalid offer reduces that ceiling. Validity checks matter as much as profitability — a mediocre valid trade beats a brilliant invalid one.

- Small trades can still clear the ≥2 acceptance bar: 1 brick (their 6) for 2 wood (their 1) gave them +4 and me +6 on a round when I thought big deals had dried up. When stocks are thin, scale quantities down rather than abandoning the trade.

- When a resource is cheap to them but valuable to me (wood: their 1, my 4), drain it aggressively but within their stock limit — take 2 when they hold 2, don't ask for 3. Their published values tell me what they'll give up cheaply; their stock tells me how much is actually on the table.