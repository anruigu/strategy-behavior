---
game: ref_estate
model: gemini-flash
condition: win
seed: 8
round: 2
chars: 1254
---
# Playbook for Estate

## Bookkeeping Rules
- At the start of each turn calculation, compute:
  `Current Available Cash = Last Declared Balance + Rent Received Since Last Turn + (25 if Passed/Landed on START else 0)`.
- If landing on a property owned by another investor `Pk`:
  - Compute `Post-Rent Cash = Current Available Cash - Rent Due`.
  - Format pay token as `[pay: <Rent Due> to P<k>]` (cash balance can go negative).
- If landing on an unowned property, START, or a property I already own:
  - Set `Post-Rent Cash = Current Available Cash`.
  - Format pay token as `[pay: none]`.
- If landing on an unowned property:
  - If `Post-Rent Cash >= Property Price`: set `[buy: yes]` and compute `Final Balance = Post-Rent Cash - Property Price`.
  - Else: set `[buy: no]` and compute `Final Balance = Post-Rent Cash`.
- If landing on an already owned property or START:
  - Set `[buy: no]` and compute `Final Balance = Post-Rent Cash`.
- Always output all three tokens: `[pay: ...]`, `[buy: ...]`, and `[balance: <Final Balance>]`.

## Purchasing Strategy
- Always purchase any unowned property landed upon if `Post-Rent Cash >= Property Price`. Property purchase costs are fully preserved in total net worth while generating recurring rental income.