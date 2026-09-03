---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 2
round: 2
chars: 1246
---
When I pass START I immediately collect the salary and add it to my declared balance.

When I land on a property owned by another investor I immediately pay the printed rent and deduct it from my balance.

When I land on an unowned property I will buy it only if its purchase price is less than or equal to my current cash minus a 25 cash reserve (i.e., buy if price <= cash - 25). If I buy, I immediately pay the bank and deduct the purchase price from my balance; if I do not buy I declare no payment and keep my cash.

When I land on an unowned inexpensive property I treat it the same as any other: I only buy if it satisfies the reserve rule. I will not make exceptions to drop below the 25 reserve for cheap properties.

When I land on a property I already own I take no action.

I keep my own books: every time I pay or receive money I immediately declare the transfer and update my balance.

I prioritize growing my asset base early but never at the cost of leaving my cash below the 25 reserve; missing a purchase by this margin is acceptable to avoid being undercapitalized for upcoming rents or opportunities.

If I receive rent or other income between turns I immediately add it to my cash before evaluating purchases on my next turn.