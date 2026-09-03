---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 7
round: 3
chars: 4141
---
PLAYBOOK — ta_negotiation

**Legality first, always.** Before proposing anything I check: both quantities are whole numbers from 1 to 3 (never 4, even if it looks like a fair-value trade — that offer gets thrown out and I lose the round), the claim is a whole number from -9 to 9. An invalid offer is a wasted round.

**Compute the claim exactly.** The claim must be the true net gain to the Guildmaster in his published values: (qty_given × his value of that resource) − (qty_taken × his value of that resource). I do this arithmetic explicitly every time and never round or guess. A wrong claim voids the offer just like an illegal quantity. When the trade is a wash for him, the correct claim is 0 — but 0 gets rejected, so I don't propose wash trades.

**Only propose trades he accepts:** net gain to him of 2 or more in his published values. A claim of exactly 2 is accepted, so I aim to stamp exactly 2 or 3 rather than pad the claim — that keeps the private cost to me of "buying" his acceptance minimal. To get that cheaply, I give resources he values highly relative to what they cost me privately and take resources he values lowly but which are worth more to me. Ratios, not absolute values, drive this: sort resources by (his value − my value) to find my cheap exports, and by (my value − his value) to find my valuable imports.

**Core strategy: exploit the gap between his published values and my private values.** In this setup sheep and brick were the standout exports (he valued 2–3, I valued 1) and wheat and wood the imports (I valued 4–5, he valued 2–3). Trading away a resource he values at 1 is nearly useless for stamping a gain — only do it if the private gain to me is large enough that even a stamped gain of 2+ is achievable within quantity limits, or accept it may not clear the bar.

**Check both sides' CURRENT stock, every time, for both resources.** This is where I lost a round (round 3: [give: 3 ore] [take: 2 wood] when he held only 1 wood). The take being 1–3 is not enough — he must hold at least that many. I re-read the holdings block fresh each round before finalising, and I specifically re-verify the resource I am taking, because his stock of my preferred import shrinks as I trade for it. When my target import runs low on his side, switch targets rather than repeat the same offer.

**Watch both stocks depleting — his side too, not just mine.** My export stock ran down (brick to 0, sheep to 0) and his import stock ran down (wood to 1, wheat to 0). A trade plan made in round 2 may be impossible in round 4. Every proposal must be built from the current holdings block, not from the previous round's pattern.

**Don't hoard.** Six rounds is short. A trade that's positive expected value for me and clears his bar gets proposed now; I don't wait for a better setup that may never come. Front-load the biggest-gap trades while stocks last, since my exports deplete and his low-value stock depletes too. This worked: rounds 1, 2, 4, 5 all landed and banked score.

**Downshift as the game matures.** Early rounds: aim for private gains of +2 or +3 with stamped gains of 3. Late rounds, when cheap exports are gone, accept marginal trades — claim exactly 2, private gain +1 or +2 (round 5's 2-sheep-for-1-wheat was exactly this and was accepted). Score is score and rounds don't roll over.

**Holding is a legitimate move.** When no legal, acceptable, privately profitable trade exists, I reply [hold: yes] rather than propose something invalid or value-losing. But I verify this by actually enumerating candidate trades first — checking the best few combinations of give/take against the bar — not by eyeballing it. Round 6's hold was correct: enumerate, confirm nothing clears both his +2 bar and a positive private gain, then hold.

**Sanity check before submitting — all five, in order:** Is the give quantity 1–3 and covered by MY current stock? Is the take quantity 1–3 and covered by HIS current stock (re-read his holdings this round)? Is the claim exactly his gain, and is it ≥2? Is my private gain (qty_taken × my value − qty_given × my value) positive? Only when all are yes do I submit.