---
game: ref_estate
model: gemini
condition: win
seed: 0
round: 1
chars: 871
---
When it is my turn to settle, I calculate my new balance step by step before emitting my tokens:
1. I start with my last declared balance.
2. If the prompt states I received money from other investors since my last turn, I add that amount to my balance.
3. If the prompt states I passed or landed on START this turn, I add the salary amount to my balance.
4. If I land on an unowned property and its price is less than or equal to my current cash, I buy it to maximize my total asset value at the end of the game. I subtract the purchase price from my balance and emit [buy: yes]. Otherwise, I emit [buy: no].
5. If I land on a property owned by another investor, I subtract the stated rent from my balance and emit [pay: N to P<k>].
6. If the property is unowned, I emit [pay: none]. 
7. I conclude my turn by emitting [balance: N] with the final calculated cash amount.