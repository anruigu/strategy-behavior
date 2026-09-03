---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 2530
---
## Ref Estate Playbook

- When landing on an unowned tile I can afford, I buy it. Final score counts cash plus purchase price of deeds, so buying converts cash into deed value at no net-worth cost and adds rent income. In my last game I bought Quarry early and Foundry on the final lap; both were correct — even a deed bought on the last turn counts at full price in scoring, so there is never a reason to skip an affordable purchase.

- Cash liquidity is not a real constraint: rent payments just transfer money, and salary plus incoming rents refill me. I don't hold back cash "for safety" when a purchase is available.

- Every turn I recompute my balance from scratch: last declared balance, plus salary when I passed or landed on START, plus rents received, minus purchases and rents owed. When the prompt says "you received N from other investors," I check the bank's transfer list to confirm the amount before adding it in. In my last game the 12s received matched the transfer list exactly — I keep that verification habit so a mismatch never silently corrupts my books.

- Rent received between my turns still needs to be added on my next declaration even when I land on my own tile or START — the "nothing due" turns are exactly where it's easy to forget the incoming rent. I always scan the turn text for "since your last turn you received N."

- When I land on a tile owned by someone else, I pay the exact listed rent to the named owner (check the transfer list if the owner isn't obvious) and subtract it immediately. No rounding, no skipping.

- When I land on my own tile or START, nothing is due and nothing can be bought: [pay: none], [buy: no], plus salary if START applies. I don't invent transactions.

- I only add the 25 salary when the prompt confirms I passed or landed on START — not merely because a new lap began.

- I always reply in the exact three-token format, ending with [balance: N], and I do the arithmetic out loud before committing so the declared cash matches my real books.

- Endgame: on the final lap I buy without hesitation since the deed scores at full purchase price; the only worse outcome would be leaving cash-idle while an unowned tile sits in front of me. My +225 finish came in part from buying Foundry on lap 6.

- I watch what opponents are buying via the transfer list, mainly to anticipate which upcoming tiles will charge me rent, but it doesn't change my buy/pay decisions — the rules make optimal play simple: buy everything affordable, pay exact rents, keep clean books.