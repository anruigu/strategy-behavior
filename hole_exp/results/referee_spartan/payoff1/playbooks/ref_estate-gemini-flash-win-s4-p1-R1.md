---
game: ref_estate
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1017
---
- When calculating `[balance: N]`, start with `last declared balance`, add 25 if the prompt indicates passing/landing on START, add any incoming payments explicitly noted in "Since your last turn you received...", subtract any rent paid to another player (`[pay: N to P<k>]`), and subtract the property purchase price if choosing `[buy: yes]`.
- When landing on an unowned property, if cash on hand after rent/salary covers the purchase price and buying will not leave me with negative cash, choose `[buy: yes]` and deduct the cost from the declared balance; otherwise choose `[buy: no]`.
- When landing on an opponent's property, format the payment token exactly as `[pay: <amount> to P<investor_id>]`, choose `[buy: no]`, and deduct that amount from the balance.
- When landing on an unowned property, START, or my own property, format the payment token as `[pay: none]`.
- Always output all three tokens: `[pay: ...]`, `[buy: ...]`, and `[balance: ...]`, ensuring the reply ends with the required bracketed tokens.