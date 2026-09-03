---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 1
round: 2
chars: 1692
---
When I land on an unowned property, I buy it if I can pay the listed price and still have at least 50 cash remaining afterward; otherwise I do not buy.

When I land on a property owned by another investor, I immediately pay the stated rent to that investor and update my cash.

When I pass or land on START, I immediately collect the salary and declare the new balance.

I keep my own books: my declared balance is my cash after I record each payment or receipt.

When the bank's book shows recent transfers, I reconcile any transfers involving me before my next decision: if the book shows I received money, I add it to my balance; if it shows I paid money, I ensure I have recorded that payment and my balance reflects it.

When asked to report a turn, I declare exactly what I paid (or [pay: none]), whether I bought the property ([buy: yes] or [buy: no]), and my resulting balance ([balance: N]).

When buying a property I record the payment as [pay: X to Pbank] and update my balance accordingly.

When paying rent I record the payment to the correct player as [pay: X to P<k>] and update my balance accordingly.

I will not attempt to buy properties that are already owned; I simply pay any rent due and move on.

If a required payment (rent or other) would drop my cash below 0, I prioritize resolving the payment (declare and record it) and thereafter avoid any purchases until my balance is restored; I do not attempt further purchases that would worsen a shortfall.

I maintain a mental minimum-cash threshold of 50 for discretionary purchases; mandatory payments (rent) are paid even if they reduce me below that threshold, but I will not initiate purchases that leave me below 50.