---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 5
round: 3
chars: 3465
---
- When I land on an owned tile, I pay the listed rent to the deed holder with [pay: N to P<k>] and declare [buy: no] — an owned tile can never be bought.
- When I land on an unowned tile, I declare [pay: none] and decide on purchase based on rent-to-price value and my cash: if I can afford it without going below a small cash buffer (enough to survive one or two rent hits before the next salary), I buy; if not, I pass.
- A tile being unowned is not enough — I first confirm the price against my actual cash on hand. I once almost treated Depot (50) as buyable with only 36; check affordability before any other reasoning about value.
- When it is the final lap, I buy any unowned tile I can afford, because deed purchase price counts in the final score even at zero rent value — but only if the cash covers it; deed score is still cash converted, so there is no scoring loss in holding cash instead.
- Deeds count at full purchase price in the final score, so cash and deed value are interchangeable at the end — the real goal is maximizing total (rent income minus rent paid), not just cash or just deeds.
- When I pass or land on START, I always add the salary, plus any incoming transfers shown in the bank's book, before subtracting my payments, and I state that reasoning explicitly so my declared balance is auditable.
- Every turn I verify my opening balance against my own last declared balance plus the bank's book of transfers to and from me before computing anything.
- I always check the "Since your last turn you received N" line and fold it in — incoming rent is easy to miss and understates my cash; I also cross-check that N against the individual transfer lines in the book (e.g. 18+18=36) rather than trusting it blindly.
- I rank tiles by rent-per-cost before buying; mid-priced tiles like Quarry (12/60) and Terrace (14/70) have the same yield as the expensive ones, so buying cheap tiles early is a good way to start collecting rent from multiple sources.
- Early laps are the time to buy aggressively, since tiles owned longer collect rent more times over the game; I do not hoard cash in lap 1–3 if a buy fits my buffer rule. High-rent anchors like Exchange (30) are worth a deep buy if the salary cycle will refill me before the next likely rent hit.
- Even a good aggressive buy like Exchange left me at 36 and forced me to pass on Depot next turn — after spending down, I accept that I may miss the next tile and plan for surviving on salary plus incoming rent until I can buy again.
- Landing on START itself also pays the salary — I treat "pass or land" the same and collect, as confirmed when I landed directly on it.
- My pay token must be exactly [pay: N to P<k>] with the closing bracket immediately after k — I once wrote [pay: 30 to P1>], dropping the ] into the wrong place; I proofread every bracket before sending.
- Each of the three tokens goes on its own line, the reply ends with [balance: N], and I emit exactly three tokens — no extras like [paid: none], which I emitted once and which is not part of the format.
- I keep arithmetic simple and sequential: opening cash + salary + transfers in − rent/purchase out = declared balance, and I never declare a balance I cannot reconstruct from the public ledger.
- When I cannot afford a purchase, I buy nothing and hold cash; when I can afford everything of value, I still avoid spending down to so little that the next owned tile wipes out my buffer before salary arrives.