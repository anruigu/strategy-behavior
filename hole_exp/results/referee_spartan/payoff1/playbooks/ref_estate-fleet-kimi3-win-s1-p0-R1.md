---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 1781
---
- When I land on an unowned property, I first compute cash = last balance + salary if START was passed/landed + any rents received since my last turn − rent due now; I buy only if that cash covers the full price.
- If an unowned deed is affordable, I buy it by default because its purchase price still counts at the end and it can collect rent; I do not leave cash idle unless I cannot cover a likely near-term rent.
- When choosing between deeds, I take the highest rent and best rent-to-cost first, then still buy cheaper deeds when they are the only affordable option.
- When I land on an owned tile, I pay the exact rent to the stated owner with `[pay: N to Pk]`, mark `[buy: no]`, and subtract it immediately.
- When the prompt says I passed or landed on START, I add the salary before deciding anything; I never skip it on a START landing.
- When the prompt says “since your last turn you received N,” I add that N before deciding to buy or pay, even if my last declared balance was earlier.
- I keep one running integer balance and make every reply consistent with it; I do not declare cash I cannot trace to salary, rent, or prior balance.
- I do not attempt to buy when cash is short; I state `[buy: no]` and keep the accurate higher/lower balance rather than bluffing.
- On the final lap, I still buy any affordable unowned deed because there is no future liquidity risk and deed price counts, but if the price exceeds cash I cleanly decline.
- I preserve enough cash early to survive known rents when possible, but not at the cost of refusing good deeds; after buying, I expect to be thin and rely on incoming rent.
- I end every settlement with the required tokens, put the balance last when asked, and keep the arithmetic in one short line so errors are easy to audit.