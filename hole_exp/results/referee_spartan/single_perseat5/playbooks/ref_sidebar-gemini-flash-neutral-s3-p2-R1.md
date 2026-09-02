---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1075
---
# Playbook: 3-Player One-Card Poker (Sidebar)

### When Facing No Bet (Current Bet = 0, Pot = 3)
- When holding a weak or medium card (2 through 10), choose `[bet: call]` to take the free showdown.
- When holding a strong card (11 through 14) in late position after checks, choose `[bet: raise]` to extract value from weaker calling ranges.

### When Facing a Single Bet (Current Bet = 3, Pot = 6, 1 Opponent In)
- When holding a weak card (2 through 8), choose `[bet: fold]`. Do not chase with undercards.
- When holding a strong card (11 through 14), choose `[bet: call]`.
- When holding a borderline card (9 or 10), choose `[bet: call]` if closing the action or if pot odds justify it, but avoid re-raising unless holding the absolute top of the deck.

### When Facing Multiple Bets (Current Bet = 3, Pot = 9, 2 Opponents In)
- When holding anything below 12 (Queen), choose `[bet: fold]`. Facing bets from both opponents heavily concentrates their ranges toward high cards (10–14).
- When holding 12, 13, or 14, choose `[bet: call]` to take advantage of the 3:1 pot odds.