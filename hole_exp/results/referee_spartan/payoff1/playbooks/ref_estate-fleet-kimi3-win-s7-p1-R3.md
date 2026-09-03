---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 7
round: 3
chars: 3174
---
- When my turn prompt arrives, I first recompute my cash from scratch: last declared balance, plus any "since your last turn you received N" amount, plus salary if I passed START, minus any rent or purchase this turn. I never reuse a stale figure without folding in the receipts line.

- I read the prompt's information in a fixed order each turn: the receipts line first, then the START/salary flag, then ownership of the tile I landed on, then the transfers book to confirm who owns what. Skipping the order is how figures go stale.

- When I land on an unowned property, I buy it if I can afford it, because purchase price counts at full value toward final worth and the deed earns rent from rivals. Buying converts cash into an asset one-for-one; it does not lose me worth.

- Buying when my cash exactly equals the price is fine — I did this with Exchange at 120 and Depot at 50 and recovered via rents and salary. Beginning-of-game deed value beats cash even down to zero balance.

- On the final lap or late in the game, liquidity concerns vanish entirely — cash and deeds count identically at the end — so I buy anything affordable with zero reserve held back.

- Early in the game I am willing to spend down to zero on an affordable deed, because rents from my existing deeds and the START salary refill my cash before bankruptcy becomes a real risk. This proved out: after hitting 0, I collected 60 in rents within one round.

- When I land on a property owned by another investor, I pay the stated rent to that investor with the [pay: N to P<k>] token and subtract it from my balance, cross-checking the owner in the transfer book — never guessing at owner or amount.

- When I land on my own property, or land on an unowned property I cannot afford, I settle with [pay: none] and [buy: no] and simply declare the recomputed balance. On a tile I passed START to reach, I still add the salary into that balance.

- When I pass or land on START, I add the salary before settling anything else that turn; landing on START itself means no property decision, so [buy: no] and [pay: none].

- When I cannot afford an unowned property, I declare [buy: no], keep my full cash, and remember that incoming rents and salary may make it or the next deed affordable on a later pass — every pass adds roughly 25-plus-rents to my buying power.

- Every declaration I make becomes my next "last declared balance," so I state purchases, payments, and salary in the same turn I incur them — the bank records transfers, but I am responsible for keeping my running total honest turn to turn.

- I verify every owner in the recent transfers book each turn; rents owed to me are how my balance grows between turns, and missing the receipts line directly cuts my final declared worth.

- I always end with all three tokens — [pay:...], [buy:...], [balance:...] — and the balance must exactly match my recomputed arithmetic, stated as a single number with nothing after it.

- What not to do: don't skip the "received from other investors" line, don't pay rent twice or to the wrong investor, and don't hoard cash early out of fear — an unbought deed is pure lost value at final scoring.