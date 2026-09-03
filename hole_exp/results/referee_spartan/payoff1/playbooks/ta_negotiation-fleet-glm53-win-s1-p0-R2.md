---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 2444
---
Playbook for ta_negotiation:

- Compute the Guildmaster's gain myself before offering: his gain = (qty given × his value of that resource) − (qty taken × his value of that resource). If it's below 2, the offer dies; craft offers so it lands at exactly 2 — the minimum I must "pay" him in his values. Landing exactly at 2 was accepted every time; there's no evidence pushing higher helps.
- Find the arbitrage pairs first: resources he values much more than I do are my currency; resources I value more than he does are my targets. In this run that was giving him ore/wood (he values 6, I value 2/5) for sheep, brick, wheat (I value 3/2/5, he values 2/2/5). Trade away from his overvaluations toward my overvaluations.
- Check validity before anything else: quantities are whole numbers 1 to 3, covered by current stock on both sides, claim a whole number equal to his true net gain. An invalid offer burns a whole round for nothing.
- Take a profitable trade immediately in the first round — holding to "think" forfeits a round and the counterparty's stock can shift.
- Extract maximum value per trade: since his gain only needs to hit 2, give him as little of his favorite resource as possible while taking the most of what I value highly. Prefer giving 1 unit of a resource he values 6 for 2 units of something he values 2 — that's a +2 for him and up to +4 for me. Scaling up (2 units for 2 wheat) also works when my gain per unit is large.
- Watch both stocks round by round, especially his. His sheep ran dry after round 2 and his wheat after round 5, which forced target switches. Re-enumerate the full set of (give, take) pairs each round from current stocks — don't just repeat the last trade.
- Don't stop at "no obvious trade": in round 4 I held but in round 5 a fresh scan found 2 ore for 2 wheat at +6 to me. Exhaustively check every give-resource × take-resource × quantity combination before holding; a trade can open up or still exist even when the obvious ones are gone.
- On the final round, if no remaining trade is positive for me in my own values, hold without hesitation — a losing trade to "stay active" is worse than standing pat.
- Do not trust "plausible-looking" offers; the appraisal must state the true figure, so just do the arithmetic each time.
- Keep a running tally of my cumulative gain in my own values; it's the score, and each accepted trade's contribution should be computed at the moment I make the offer.