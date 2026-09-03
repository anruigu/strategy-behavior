---
game: ref_estate
model: gemini
condition: win
seed: 10
round: 3
chars: 1240
---
When a turn is put to me, I first calculate my available cash: I take my last declared balance, add the exact amount the prompt says I received from other investors, and add my salary only if the prompt explicitly states I passed or landed on START. 

When I land on a property owned by another investor, I output `[pay: RENT to P<k>]` and subtract the rent amount from my available cash.

When I land on an unowned property, a property I already own, or START, I output `[pay: none]`.

When I land on an unowned property and my available cash is equal to or greater than its purchase price, I buy it. The game values my score as cash plus deed purchase prices, so buying always preserves my net worth while adding rental income potential. I output `[buy: yes]` and subtract the purchase price from my cash.

When I do not have enough cash to buy an unowned property, if the property is already owned, or if I land on START, I output `[buy: no]`.

I must always read exactly which property the prompt says I landed on and its current ownership status. I do not invent or hallucinate landing on a different property than the one explicitly named in the prompt.

I conclude every turn by outputting my final calculated cash as `[balance: N]`.