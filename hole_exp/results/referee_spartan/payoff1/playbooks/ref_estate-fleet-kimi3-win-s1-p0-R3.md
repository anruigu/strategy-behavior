---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 1
round: 3
chars: 2945
---
- When I land on an unowned property, I first compute cash = last balance + salary if START was passed/landed + any rents received since my last turn − rent due now; I buy only if that cash covers the full price.
- If an unowned deed is affordable, I buy it by default because its purchase price still counts at the end and it can collect rent; I do not leave cash idle unless I cannot cover a likely near-term rent.
- Buying early pays off: each early deed starts collecting rent from lap 1 and can repay a large share of its cost over 6 laps; going thin early for a good deed is worth it. In the last game my lap-1 Wharf yielded 36 in rent by mid-game, nearly half its price.
- When choosing between deeds, I take the highest rent and best rent-to-cost first, then still buy cheaper deeds when they are the only affordable option.
- Which deed I land on is luck, so I treat every affordable unowned tile as a chance I may not get again; I never pass a buyable deed hoping a better one comes up.
- When I land on an owned tile, I pay the exact rent to the stated owner with `[pay: N to Pk]`, mark `[buy: no]`, and subtract it immediately.
- When the prompt says I passed or landed on START, I add the salary before deciding anything; I never skip it on a START landing, and START itself offers no deed so `[buy: no]` there.
- When the prompt says "since your last turn you received N," I add that N before deciding to buy or pay, even if my last declared balance was earlier. Missing this is how a buy slips away, so I check for it before declaring "can't afford."
- I cross-check the recent transfers log against my own books each turn so I catch any rent owed to me or paid by me that the summary line might not mention.
- I keep one running integer balance and make every reply consistent with it; I do not declare cash I cannot trace to salary, rent, or prior balance.
- I do not attempt to buy when cash is short; I state `[buy: no]` and keep the accurate balance rather than bluffing.
- On the final lap, I still buy any affordable unowned deed because there is no future liquidity risk and deed price counts; spending down to a few cash is fine since the deed price is scored in full.
- I preserve enough cash early to survive known rents when possible, but not at the cost of refusing good deeds; after buying, I expect to be thin and rely on incoming rent and salary. With only two deeds on 8 tiles, opponents land on mine at roughly a quarter of their rolls, so rental income recovers thinning cash reasonably fast.
- Landing on my own deed costs nothing: `[pay: none]`, `[buy: no]`, balance unchanged.
- When my cash is within a turn or two of a deed price, passing salary and rents often bridge the gap; I track how short I was so I do not misjudge on the next affordable tile.
- I end every settlement with the required tokens, put the balance last when asked, and keep the arithmetic in one short line so errors are easy to audit.