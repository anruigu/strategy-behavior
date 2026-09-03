---
game: ref_estate
model: gemini-flash
condition: win
seed: 8
round: 1
chars: 1220
---
# Playbook for Estate

## Bookkeeping Rules
- At the start of each turn calculation, compute `Current Available Cash = Last Declared Balance + Rent Received Since Last Turn + (25 if Passed/Landed on START else 0)`.
- When landing on a property owned by another player `Pk`, compute `Post-Rent Cash = Current Available Cash - Rent Due` and format the token as `[pay: <Rent Due> to P<k>]`.
- When landing on an unowned property, START, or a property I already own, set `Post-Rent Cash = Current Available Cash` and format the token as `[pay: none]`.
- If an unowned property is available and `Post-Rent Cash >= Property Price`, always buy: output `[buy: yes]` and compute `Final Balance = Post-Rent Cash - Property Price`.
- If the property is owned, already owned by me, or `Post-Rent Cash < Property Price`, output `[buy: no]` and compute `Final Balance = Post-Rent Cash`.
- Always set `[balance: <Final Balance>]`.

## Purchasing Strategy
- Prioritize buying unowned properties whenever affordable, especially in early laps, to maximize rental income and lock in net worth (property price counts toward final score).
- Double-check the exact cash threshold before declaring `[buy: no]`; do not pass on affordable deeds.