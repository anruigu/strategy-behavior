---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 5
round: 2
chars: 2714
---
**Playbook for the Guildmaster negotiation**

- Every round, I compute the Guildmaster's true net gain for my proposed trade: (his published value of what I give × qty) − (his published value of what I take × qty). The claim must state exactly that number, because the appraisal desk rejects false figures. Never inflate or shade the claim.

- The Guildmaster accepts any trade with a true gain of 2 or more, so I aim for his gain just over that threshold (2–4) while maximizing my own private-value gain. I don't need to be generous to him — padding his side only wastes value.

- The best trades exploit double disagreement: I give a resource I value low that he values high, and take one I value high that he values low. I rank all resource pairs by (my value of taken × qty − my value of given × qty) subject to his net gain ≥ 2, and pick the top candidate each round.

- Quantity is a lever: I can scale up to 3 units to multiply a favorable per-unit margin, as long as his gain stays in a range he accepts (which is anything ≥ 2, so larger quantities of a good-for-me trade are fine and better).

- Hard legality check before proposing, on both sides: quantities are capped at 3, what I give must be covered by MY stock, and what I take must be covered by HIS stock. An illegal offer is not merely rejected — it burns the round for nothing (this cost me rounds 3 and 5: asking for 4 sheep, then for wheat he held 0 of). I verify every quantity against the current holdings table line by line before replying.

- After a trade depletes a stock, I recompute from the new holdings rather than repeating a stale trade — I reread the fresh stock lists every round, since the opponent's holdings change and a resource he once had may now be gone.

- Trading the same resource back and forth is legal and profitable when both sides value the traded goods differently each direction — I keep cycling mismatches as long as both stocks last and each leg clears the ≥2 gain bar for him.

- A trade is still worth making even when he values something as much as I do (equal values), if the swap nets me a positive margin — but I prefer the large-gap trades first and save the thin ones for the last rounds when better options are exhausted.

- I never hold while a mutually profitable trade exists; my score is only my own gained value, and declining gains nothing. Only hold if no legal offer gives him ≥ 2 gain while giving me positive value. In the final round, even a margin of +1 is worth taking.

- A cheap but valid fallback when stocks run dry: a small 1-for-1 swap of goods where he values what I give far above what I take (e.g., his value 6 vs 1) can clear his ≥2 bar and still net me a small positive margin.