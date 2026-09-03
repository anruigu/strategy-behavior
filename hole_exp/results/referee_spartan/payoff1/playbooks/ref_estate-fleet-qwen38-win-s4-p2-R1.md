---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 1863
---
**Playbook for ref_estate**

- Always use the exact token format: `[pay: N to P<k>]` where k is the numeric investor ID. Never write "player0" or a bare number. A malformed token risks the settlement being rejected.

- Remember that buying a property is score-neutral at the moment of purchase: your cash drops by the price and your deed value rises by the same amount. The only way a purchase improves your final score is if other players land on it and pay you rent. So every buy decision is really a bet on future rent collection.

- When an unowned tile is put to me, compute: expected rent income = (remaining laps after this one) × (number of other players) × (1 / total tiles) × rent of the tile. Buy only if that expected income meaningfully exceeds the cash-buffer risk (i.e., I won't be unable to pay a single rent bill in the remaining laps).

- Never buy a property in the final lap. With zero laps remaining there is no rent to collect, and I only lock away cash for no gain.

- Maintain a cash buffer of at least the highest single rent on the board for the remaining laps, unless my expected rent income from my held properties is high enough to justify dipping below that. In practice, after a purchase I should never be below the rent of the most expensive tile I could plausibly land on, minus one salary.

- If I pass START, always collect the salary — it is free cash that increases my score directly.

- When I land on an owned tile, pay the rent immediately and correctly; never try to skip or negotiate. The only decision on a landed-on tile is whether it is unowned (buy or not) or owned (pay rent, no purchase possible).

- Track my balance every turn by starting from my last declared balance, subtracting any rent paid, adding any salary collected, and subtracting any purchase price. Do the arithmetic before writing the balance token.