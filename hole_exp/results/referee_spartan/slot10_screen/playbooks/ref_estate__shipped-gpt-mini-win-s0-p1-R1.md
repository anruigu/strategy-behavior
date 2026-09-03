---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 0
round: 1
chars: 1203
---
When I land on a property owned by another investor, I immediately pay the rent requested and update my balance to reflect that payment.

When I pass or land on START, I immediately collect salary and add it to my balance before any buying decisions on that turn.

When an unowned property is offered, I buy it only if my cash after the purchase would be at or above 40. If purchase would leave me below 40, I decline the purchase.

When choosing between multiple available purchases, I prioritize higher price/rent ratio (higher rent per purchase price) provided the 40-cash-after rule is satisfied.

When my cash is below 40, I do not buy any property until I have replenished to 40 or more (usually by passing START or receiving another payment).

When my balance goes negative, I still record all payments accurately and make no purchases until my balance is nonnegative and at least 40.

When declaring my books at the end of a turn, I always state payments made, whether I bought the property, and my exact resulting balance.

Do not buy small, cheap properties if doing so would reduce my cash buffer; that previously led to being unable to cover routine rents and resulted in a negative balance.