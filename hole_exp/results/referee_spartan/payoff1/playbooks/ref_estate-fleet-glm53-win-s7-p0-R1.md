---
game: ref_estate
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 1565
---
**Playbook for ESTATE**

- When an unowned tile is put to me and I can afford it, I buy. Buying converts cash into an asset counted at full price in the final tally, so a purchase costs nothing in net worth while earning rent on top. Keep buying whenever my balance covers the price.

- But don't buy down to near-zero if I can avoid it. Spending to a 10-cash balance left me unable to buy anything for the rest of the game — I missed a 120-price tile later because I had no cash. When choosing between two purchases in early laps, prefer keeping at least 30–50 in reserve so I can still buy mid-priced tiles that come up later.

- When I can't afford a tile, just declare [pay: none] [buy: no] with my correct balance — no reasoning needed.

- Always reconcile my balance before declaring: start from last declared balance, add salary if I passed START, add any rent received from other investors since my last turn, then subtract rent owed. The prompt tells me when I received money; I must not forget to add it.

- Rent owed to another investor: pay it, declare [pay: N to P<k>], [buy: no].

- Output format: exactly the three bracketed tokens on their own lines, payment to bank for purchases written as [pay: N to bank]. Never leave stray text or malformed tokens in the reply — one episode had a garbled line before the tokens, which risks rejection.

- Keep reasoning to one short sentence at most; the tokens are what count.

- The endgame is total declared cash plus deed prices, so passing START on the final lap is free money — collect it and declare it.