---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 2712
---
PLAYBOOK — ta_negotiation

**Legality first, always.** Before proposing anything I check: both quantities are whole numbers from 1 to 3 (never 4, even if it looks like a fair-value trade — that offer gets thrown out and I lose the round), I hold enough of what I give, the opponent holds enough of what I take, and the claim is a whole number from -9 to 9. An invalid offer is a wasted round; I lost two rounds this way.

**Compute the claim exactly.** The claim must be the true net gain to the Guildmaster in his published values: (qty_given × his value of that resource) − (qty_taken × his value of that resource). I do this arithmetic explicitly every time and never round or guess. A wrong claim voids the offer just like an illegal quantity. When the trade is a wash for him, the correct claim is 0 — but 0 gets rejected, so I don't propose wash trades.

**Only propose trades he accepts:** net gain to him of 2 or more in his published values. To get that cheaply, I give resources he values highly relative to what they cost me (in this setup: ore at 6, wheat and sheep at 3) and take resources he values lowly (brick at 1, wood at 2) but which are worth more to me privately.

**Core strategy: exploit the gap between his published values and my private values.** Before each offer I scan for the resource where his value most exceeds mine (my cheap export) and the resource where my value most exceeds his (my valuable import), and build the trade around those. Trading away brick (his value 1) is nearly useless for stamping a gain — only do it if the private gain to me is large enough that even a stamped gain of 2+ is achievable within quantity limits, or accept it may not clear the acceptance bar.

**Watch his stock.** He can only pay what he holds. If I want his ore and he's down to 3, a take of 3 is the cap; if his wood drops to 1, I can't take 2. I check his current holdings, not the initial ones.

**Watch my own stock the same way.** After a few rounds of giving away my export resource, I may run dry. When my best export is exhausted, I move to the next-best ratio, or hold.

**Don't hoard.** Six rounds is short. A trade that's positive expected value for me and clears his bar gets proposed now; I don't wait for a better setup that may never come. When no legal, acceptable, privately profitable trade exists, I reply [hold: yes] rather than propose something invalid or value-losing.

**Sanity check before submitting:** Is the give quantity 1–3 and covered by my stock? Is the take quantity 1–3 and covered by his stock? Is the claim exactly his gain, and is it ≥2? Is my private gain (qty_taken × my value − qty_given × my value) positive? Only when all four are yes do I submit.