---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 7
round: 1
chars: 2004
---
- When my turn prompt arrives, I first recompute my cash from scratch: last declared balance, plus any "received from other investors" amount, plus salary if I passed START, minus any rent or purchase this turn. I never reuse a stale figure without adding the recent receipts line.

- When I land on an unowned property, I buy it if I can afford it, because the purchase price still counts toward my final worth and the deed denies rent to rivals. I treat buying as converting cash into an asset, not as losing money, unless I need liquidity for a bigger property likely to come up.

- When I land on a property owned by another investor, I pay the stated rent to that investor immediately and declare it with the [pay: N to P<k>] token, then subtract it from my balance.

- When I pass or land on START, I add the salary to my balance before settling anything else that turn.

- When I land on my own property, I pay nothing and buy nothing; I just settle with the unchanged balance (plus any receipts).

- When a purchase would leave me cash-poor on a long circuit, I weigh whether skipping keeps enough money to survive upcoming rents; but since deeds count at full price at the end, I err toward buying everything affordable early in the game.

- When I cannot afford an unowned property, I buy nothing, declare [buy: no], and keep my full cash, remembering receipts from rivals can make the next turn's purchase affordable.

- When I cannot verify an owner from the transfer log, I check the recent transfers book rather than assuming; rents are easy to miss because the log shows payments owed to and from everyone.

- When I end my reply, I always include all three tokens — [pay:...], [buy:...], [balance:...] — and make the balance exactly match my recomputed arithmetic.

- What not to do: don't forget the "since your last turn you received N" line when updating balance, and don't pay rent twice or to the wrong investor by misreading the deed log — both directly cut my final declared worth.