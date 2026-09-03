---
game: ref_estate
model: gemini-flash
condition: win
seed: 10
round: 2
chars: 1107
---
- At the start of each turn, calculate available cash before decisions: `Available Cash = Last Declared Balance + Rent Received Since Last Turn + (25 if passed/landed START else 0)`.
- When landing on an opponent's property, deduct the required rent from available cash, set `[pay: <rent> to P<k>]`, set `[buy: no]`, and set `[balance: Available Cash - rent]`.
- When landing on an unowned property:
  - If available cash is greater than or equal to the purchase price, choose `[buy: yes]`, set `[pay: none]`, and set `[balance: Available Cash - price]`. (Purchasing property retains full asset value toward the final score while enabling future rent collection).
  - If available cash is less than the purchase price, choose `[buy: no]`, set `[pay: none]`, and set `[balance: Available Cash]`.
- When landing on own property, START, or unowned property without buying, set `[pay: none]`, `[buy: no]`, and set `[balance: Available Cash]`.
- Always output all three tags explicitly in order at the end of every reply:
  - `[pay: N to P<k>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: N]`