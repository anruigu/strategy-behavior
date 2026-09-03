---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 5
round: 1
chars: 1895
---
- When I land on an owned tile, I pay the listed rent to the deed holder with [pay: N to P<k>] and declare [buy: no] — an owned tile can never be bought.
- When I land on an unowned tile, I declare [pay: none] and decide on purchase based on rent-to-price value and my cash: if I can afford it without going below a small cash buffer (enough to survive one or two rent hits before the next salary), I buy; if not, I pass.
- When it is the final lap, I buy any unowned tile I can afford, because deed purchase price counts in the final score even at zero rent value — there is no downside to converting nearly all cash into deeds.
- When I pass or land on START, I always add the salary, plus any incoming transfers shown in the bank's book, before subtracting my payments, and I state that reasoning explicitly so my declared balance is auditable.
- Every turn I verify my opening balance against my own last declared balance plus the bank's book of transfers to and from me before computing anything.
- I always check the "Since your last turn you received N" line and fold it in — incoming rent is easy to miss and understates my cash.
- I rank tiles by rent-per-cost before buying; high-price high-rent tiles (Exchange, Foundry) earn back fastest, so I buy them eagerly when affordable.
- I keep replies to exactly the three required bracketed tokens — no extra tokens like [paid: none], which I emitted once and which is not part of the format — and I end the reply with [balance: N].
- I keep arithmetic simple and sequential: opening cash + salary + transfers in − rent/purchase out = declared balance, and I never declare a balance I cannot reconstruct from the public ledger.
- When I cannot afford a purchase, I buy nothing and hold cash; when I can afford everything of value, I still avoid spending down to so little that the next owned tile wipes out my buffer before salary arrives.