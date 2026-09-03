---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 2144
---
**Playbook for ref_estate**

- Always use the exact token format: `[pay: N to P<k>]` where k is the numeric investor ID. Never write "player0" or a bare number. A malformed token risks the settlement being rejected.

- Buying a property is score-neutral at the moment of purchase: cash drops by the price, deed value rises by the same amount. The only way a purchase changes your final score is through rent collected from other players landing on it. Every buy decision is a bet on future rent collection.

- When an unowned tile is put to me, compute expected rent income: (remaining laps after this one) × (number of other players) × (1 / total tiles) × rent of the tile. Buy only if that expected income exceeds the purchase price. In practice, on boards where the rent-to-price ratio of every tile is below roughly 0.25 (which is most boards I've seen), this condition is never met and the correct answer is always "no." The default should be not to buy; I should only buy when the numbers clearly say yes.

- Never buy in the final lap. Zero laps remain, no rent can be collected, and I only lock away cash.

- Maintain a cash buffer of at least the highest single rent on the board. Since I cannot predict where I'll land, being unable to pay a rent bill is catastrophic. After any purchase, verify I can still cover the most expensive rent I could face.

- If I pass START, always collect the salary. It is free cash that directly increases my score.

- When I land on an owned tile, pay the rent immediately and correctly. There is no negotiation. The only decision on a landed-on tile is: unowned (apply the buy formula above) or owned (pay rent, no purchase possible).

- Track my balance every turn: last declared balance − rent paid + salary collected − purchase price = new balance. Do the arithmetic before writing the balance token.

- The game is largely a survival game: I cannot control my rolls, so I cannot choose where I land or when I pass START. The only real strategic lever is the buy decision. On most boards that lever points to "no," and the best I can do is avoid going broke by keeping enough cash for rent bills.