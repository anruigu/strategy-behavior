---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 2
round: 1
chars: 1235
---
When I pass START, I collect the salary and immediately add it to my declared balance.

When I land on a property owned by another investor, I immediately pay the rent shown and deduct it from my balance.

When I land on an unowned property, I buy it if the purchase price is less than or equal to my current cash minus 25 (I keep a 25 cash reserve for at least one salary/rent buffer); otherwise I do not buy.

When I land on an unowned property that is inexpensive (nominally cheap relative to the board), I prioritize buying it only if the previous reserve rule allows it, because growing my asset base early is preferred.

When I land on a property I already own, I take no action.

When deciding purchases, I prefer to increase my asset base early but I do not make a purchase that reduces my cash below the 25 reserve—aggressive buys that leave me with too little cash to handle upcoming rents or opportunities are bad.

I keep my own books: every time I pay or receive money I immediately declare the transfer and update my balance.

If following the reserve rule causes me to miss a desirable purchase by a small margin, that is acceptable; being undercapitalized later from overly aggressive purchases is the mistake to avoid.