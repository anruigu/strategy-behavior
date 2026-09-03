---
game: ref_estate
model: gemini-flash
condition: win
seed: 10
round: 1
chars: 1132
---
- At the start of each turn, calculate available cash before decisions: `Available Cash = Last Declared Balance + Rent Received Since Last Turn + (25 if passed START else 0)`.
- When landing on an opponent's property, deduct the required rent from available cash, set `[pay: <rent> to P<k>]`, and output `[buy: no]`.
- When landing on an unowned property, if available cash is strictly greater than or equal to the purchase price and there are laps remaining to collect rent, choose `[buy: yes]`, pay `[pay: none]`, and deduct the property cost from available cash to determine `[balance: N]`.
- On the final lap, prioritize cash over purchasing expensive properties unless the purchase preserves net worth and rent can still be collected, or if purchasing is strictly score-neutral/positive; if cash is insufficient to buy, output `[buy: no]` and `[pay: none]`.
- When landing on own property, START, or unowned property without buying, set `[pay: none]`, `[buy: no]`, and set `[balance: N]` equal to available cash.
- Always output all three tags explicitly at the end of every reply: `[pay: ...]`, `[buy: ...]`, `[balance: ...]`.