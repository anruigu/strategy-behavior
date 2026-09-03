---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 1
round: 1
chars: 1180
---
When I land on an unowned property, I buy it if I can pay the price and still have at least 50 cash left afterward; otherwise I do not buy.

When I land on a property owned by another investor, I immediately pay the stated rent to that investor and update my cash.

When I pass or land on START, I immediately collect the salary and declare the new balance.

When I receive money from another investor or the bank between turns, I add it to my declared balance before the next decision.

When asked to report a turn, I declare exactly what I paid (or none), whether I bought (yes/no), and my resulting balance.

When the bank's book shows recent transfers, I reconcile them against my own books and adjust my declared balance if any incoming payments to me are recorded.

When buying a property, I record the payment to Pbank and the new balance; when paying rent, I record the payment to the correct P<k> and the new balance.

When my cash would drop below 0 from a required payment, I do not attempt further purchases and prioritize resolving the shortfall (declare payments and avoid buys).

Do not attempt to buy properties that are already owned; simply pay rent and move on.