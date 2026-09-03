---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 1719
---
Playbook for ta_negotiation:

- Compute the Guildmaster's gain myself before offering: his gain = (qty given × his value of that resource) − (qty taken × his value of that resource). If it's below 2, the offer dies; craft offers so it lands at exactly 2 to 4 — the minimum I must "pay" him in his values.
- Find the arbitrage pairs first: resources he values much more than I do are my currency; resources I value more than he does are my targets. Trade away from his overvaluations (relative to mine) toward my overvaluations. My profit is what matters, not volume.
- Check validity before anything else: quantities are whole numbers 1 to 3, covered by current stock on both sides, claim a whole number equal to his true net gain. An invalid offer burns a whole round for nothing — I wasted two rounds this way, especially by trying to give 4 units of one resource.
- When I spot a clearly profitable trade, take it immediately in the first round — holding to "think" just forfeits a round and the counterparty's stock can shift.
- Extract maximum value per trade: since his gain only needs to hit 2, give him as little of his favorite resource as possible while taking the most of what I value highly. E.g. give 2 of a resource he values 5 for 1–2 of a resource I value 5 and he values 3–5.
- Watch both stocks round by round. If a target resource runs out on his side, switch targets or stop.
- On the final round, if no remaining trade is positive for me in my own values, hold without hesitation — a losing trade to "stay active" is worse than standing pat.
- Do not trust "plausible-looking" offers; the appraisal must state the true figure, so there is no room for a soft claim. Just do the arithmetic each time.