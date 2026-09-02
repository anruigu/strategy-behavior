---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 834
---
# Playbook: 3-Player One-Card Poker (Sidebar)

### When Facing No Bet (Current Bet = 0, Pot = 3)
- When holding 2 through 10, choose `[bet: call]` to take the free showdown.
- When holding 11 through 14, choose `[bet: raise]` to extract value from weaker hands that check-call or fold.

### When Facing a Single Bet (Current Bet = 3, Pot = 6, 1 Opponent Raised/Called)
- When holding 2 through 10, choose `[bet: fold]`. Opponents raise with very strong holdings (11–14); calling with mediocre hands loses chips.
- When holding 11 through 14, choose `[bet: call]`.

### When Facing a Bet with an Opponent Call (Current Bet = 3, Pot = 9, 2 Opponents In)
- When holding 2 through 11, choose `[bet: fold]`. Against two active players, the winning card is heavily skewed toward 13 or 14.
- When holding 12, 13, or 14, choose `[bet: call]`.