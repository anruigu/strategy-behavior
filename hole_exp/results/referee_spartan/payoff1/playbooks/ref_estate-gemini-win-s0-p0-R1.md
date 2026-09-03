---
game: ref_estate
model: gemini
condition: win
seed: 0
round: 1
chars: 1146
---
When I am presented with a turn, I always start calculating my new cash by taking my last declared balance.
I add any rental income the prompt specifically states I received from other investors since my last turn.
When the prompt states I passed or landed on START, I add the passing salary to my cash total.
When I land on an unowned property, I check if my current calculated cash is sufficient to cover the purchase price.
When I have enough cash, I always buy the unowned property to build total asset value and secure future rental income, and I subtract the purchase price from my cash.
When I do not have enough cash to buy an unowned property, I output `[buy: no]` and leave my cash unchanged.
When I land on a property owned by another investor, I output `[pay: N to P<k>]` using the required rent and the owner's ID, and I subtract that rent from my cash.
When I land on an unowned property, my own property, or START, I output `[pay: none]`.
When I land on an already owned property, my own property, or START, I output `[buy: no]`.
When I conclude my turn, I output exactly my newly calculated cash total in the `[balance: N]` token.