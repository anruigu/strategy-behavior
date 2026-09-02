---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 832
---
# Playbook: 3-Player One-Card Poker (Sidebar)

### When Facing No Bet (Current Bet = 0, Pot = 3)
- When holding 2 through 10, choose `[bet: call]` to take the free showdown.
- When holding 11 through 14, choose `[bet: raise]` to extract value from weaker hands that call or check-call.

### When Facing a Single Bet (Current Bet = 3, Pot = 6, 1 Opponent In)
- When holding 2 through 10, choose `[bet: fold]`. Opponent betting ranges are tight (frequently 12–14); calling with 9 or 10 consistently loses chips over time.
- When holding 11 through 14, choose `[bet: call]`.

### When Facing a Bet with an Opponent Call (Current Bet = 3, Pot = 9, 2 Opponents In)
- When holding 2 through 11, choose `[bet: fold]`. Two active opponents heavily weight the winning hand toward 13 or 14.
- When holding 12, 13, or 14, choose `[bet: call]`.