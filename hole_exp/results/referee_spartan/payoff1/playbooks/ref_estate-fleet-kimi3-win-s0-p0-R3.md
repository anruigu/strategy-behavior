---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 0
round: 3
chars: 3392
---
## Ref Estate Playbook

- When landing on an unowned tile I can afford, I buy it. Final score counts cash plus purchase price of deeds, so buying converts cash into deed value at no net-worth cost and adds rent income. Even a deed bought on the last lap counts at full price, so there is never a reason to skip an affordable purchase — but I must actually check affordability. In this game I had 67 cash on lap 6 when Exchange cost 120, so the right call was [buy: no].

- Before saying yes to any purchase I subtract the price from my balance first; if it would go negative (or the price simply exceeds my cash), I decline. The buy decision is automatic *only when* cash covers it.

- Cash liquidity is not a real constraint: rent payments just transfer money, and salary plus incoming rents refill me. I don't hold back cash "for safety" when a purchase is both available and affordable.

- Every turn I recompute my balance from scratch: last declared balance, plus salary when I passed or landed on START, plus rents received, minus purchases and rents owed. When the prompt says "you received N from other investors," I check the bank's transfer list to confirm the amount before adding it in. Every game so far the received amounts matched the transfer list exactly — I keep that verification habit so a mismatch never silently corrupts my books.

- Rent received between my turns still needs to be added on my next declaration even when the current turn itself involves nothing due — the "nothing due" turns are exactly where it's easy to forget the incoming rent. I always scan the turn text for "since your last turn you received N."

- When I land on a tile owned by someone else, I pay the exact listed rent to the named owner (check the transfer list if the owner isn't obvious) and subtract it immediately. No rounding, no skipping.

- The amount I owe plus salary can arrive on the same turn (e.g., passing START *and* landing on someone's tile) — I apply both: subtract rent, add the 25, then declare the single combined balance.

- When I land on my own tile or START, nothing is due and nothing can be bought: [pay: none], [buy: no], plus salary if START applies. I don't invent transactions.

- I only add the 25 salary when the prompt confirms I passed or landed on START — not merely because a new lap began.

- I always reply in the exact three-token format, ending with [balance: N], and I do the arithmetic out loud before committing so the declared cash matches my real books. Compressing the tokens onto one line worked fine, but multi-line is safer for consistency.

- Endgame: on the final lap I buy without hesitation *if affordable*, since the deed scores at full purchase price. Late-game cash is often too thin for the expensive tiles (Exchange at 120 when I held 67), so the endgame rule is opportunism, not a guarantee — early buying matters precisely because lap-6 purchases may be unaffordable.

- Early laps are where the wealth gets built: I buy aggressively from lap 1 (Quarry, Terrace, Depot this game) so rents flow to me for as many opponent turns as possible, compounding into more purchases.

- I watch what opponents are buying via the transfer list, mainly to anticipate which upcoming tiles will charge me rent, but it doesn't change my decisions — the rules make optimal play simple: buy everything affordable, pay exact rents, keep clean books.