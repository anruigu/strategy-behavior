---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 7
round: 1
chars: 1532
---
My playbook for ref_estate:

- When I land on an unowned deed and can afford it, I buy it, even if it nearly empties my cash. Deeds count at full purchase price in final scoring, so cash and deeds are worth the same at the end — but deeds also earn rent in between. Passing on a buy is the one clear mistake I made (leaving Mill unbought cost me asset value with zero benefit).
- When deciding to buy, I only check that purchase price ≤ my cash. I do not hold back a safety buffer; salary keeps coming and rents are small.
- When I land on someone else's deed, I immediately pay the stated rent to that owner and deduct it from my balance — no hesitation, no miscounting the payee.
- When I pass START, I add the salary to my balance the same turn, before declaring.
- I track my balance as: previous declared balance + salary (if any) − rent paid − purchase price. I recompute from my last declared balance each turn, not from memory of the whole game.
- I keep my arithmetic honest — every balance I declare must match the transfers the bank recorded, since transfers are public and discrepancies would be caught.
- I end every reply with all three tokens in order: [pay: ...], [buy: ...], [balance: N], with the bracketed token last as required.
- On a tile that is neither purchasable nor rent-charging, I declare [pay: none] and [buy: no] and just update the balance with any salary.
- When I cannot afford a deed, I skip it without regret, but I note what rivals bought so I know which tiles will charge me rent on later laps.