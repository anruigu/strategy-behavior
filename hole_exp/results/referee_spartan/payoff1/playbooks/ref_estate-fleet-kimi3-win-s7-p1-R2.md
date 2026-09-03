---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 7
round: 2
chars: 2549
---
- When my turn prompt arrives, I first recompute my cash from scratch: last declared balance, plus any "since your last turn you received N" amount, plus salary if I passed START, minus any rent or purchase this turn. I never reuse a stale figure without folding in the receipts line — in my game I went 0 → 57 by adding 32 received plus 25 salary, and that line was the whole difference.

- When I land on an unowned property, I buy it if I can afford it, because purchase price counts at full value toward final worth and the deed denies rivals rent. Buying converts cash into an asset; it does not lose money.

- On the final lap or late in the game, liquidity concerns nearly vanish — cash and deeds count identically at the end — so I buy anything affordable without holding back reserves for future rents.

- Early in the game I am willing to spend down to zero on an affordable deed (I bought Depot for exactly my last 50), because rents from my existing deeds and the START salary refill my cash before bankruptcy becomes a real risk.

- When I land on a property owned by another investor, I pay the stated rent to that investor immediately with the [pay: N to P<k>] token and subtract it from my balance, matching the deed owner from the transfer book, never guessing.

- When I pass or land on START, I add the salary before settling anything else that turn; landing on START itself means no property decision, so [buy: no] and [pay: none].

- When I land on my own property, I pay nothing and buy nothing; I settle with the unchanged recomputed balance.

- When a purchase would leave me cash-poor mid-game with several expensive properties ahead, I briefly weigh survival against the deed's endgame value — but the default is to buy, since deeds count at full price.

- When I cannot afford an unowned property, I declare [buy: no], keep my full cash, and remember that incoming rents may make it affordable on a later pass.

- I verify every owner in the recent transfers book each turn; rents owed to me are how my balance grows between turns, and missing the receipts line directly cuts my final declared worth.

- I always end with all three tokens — [pay:...], [buy:...], [balance:...] — and the balance must exactly match my recomputed arithmetic, stated as a single number with no trailing reasoning risks after it.

- What not to do: don't skip the "received from other investors" line, don't pay rent twice or to the wrong investor, and don't hoard cash early out of fear — an unbought deed is pure lost value at final scoring.