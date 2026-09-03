---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 7
round: 2
chars: 3490
---
PLAYBOOK — ta_negotiation

**Legality first, always.** Before proposing anything I check: both quantities are whole numbers from 1 to 3 (never 4, even if it looks like a fair-value trade — that offer gets thrown out and I lose the round), the claim is a whole number from -9 to 9. An invalid offer is a wasted round.

**Compute the claim exactly.** The claim must be the true net gain to the Guildmaster in his published values: (qty_given × his value of that resource) − (qty_taken × his value of that resource). I do this arithmetic explicitly every time and never round or guess. A wrong claim voids the offer just like an illegal quantity. When the trade is a wash for him, the correct claim is 0 — but 0 gets rejected, so I don't propose wash trades.

**Only propose trades he accepts:** net gain to him of 2 or more in his published values. To get that cheaply, I give resources he values highly relative to what they cost me privately and take resources he values lowly but which are worth more to me. Ratios, not absolute values, drive this: sort resources by (his value − my value) to find my cheap exports, and by (my value − his value) to find my valuable imports.

**Core strategy: exploit the gap between his published values and my private values.** In this setup wheat was the standout export (he valued 6, I valued 1) and sheep/wood/brick the imports (I valued 6, he valued 1–4). Trading away a resource he values at 1 is nearly useless for stamping a gain — only do it if the private gain to me is large enough that even a stamped gain of 2+ is achievable within quantity limits, or accept it may not clear the bar.

**Check both sides' CURRENT stock, every time, for both resources.** This is where I lost a round: I proposed [give: 2 ore] [take: 3 sheep] when the Guildmaster held only 2 sheep — the take was legal by quantity but not covered by his stock, and the round was voided. I must re-read the holdings block fresh each round, because past trades have already changed it, and check: do I hold at least the give quantity of what I'm giving, and does he hold at least the take quantity of what I'm taking?

**Watch my own export stock running dry.** Once my cheap export is exhausted (wheat hit 0 after round 4), the game may be over: his acceptance bar of +2 becomes hard or impossible to clear with resources I privately value highly. I accept this and hold rather than force bad trades.

**Don't hoard.** Six rounds is short. A trade that's positive expected value for me and clears his bar gets proposed now; I don't wait for a better setup that may never come. Front-load the biggest-gap trades while stocks last, since my export depletes and his low-value stock depletes too.

**Holding is a legitimate move.** When no legal, acceptable, privately profitable trade exists, I reply [hold: yes] rather than propose something invalid or value-losing. But I verify this by actually enumerating candidate trades first — checking the best few combinations of give/take against the bar — not by eyeballing it. If a marginal trade exists (claim exactly 2, small positive private gain), take it: score is score and rounds don't roll over.

**Sanity check before submitting — all five, in order:** Is the give quantity 1–3 and covered by MY current stock? Is the take quantity 1–3 and covered by HIS current stock? Is the claim exactly his gain, and is it ≥2? Is my private gain (qty_taken × my value − qty_given × my value) positive? Only when all are yes do I submit.