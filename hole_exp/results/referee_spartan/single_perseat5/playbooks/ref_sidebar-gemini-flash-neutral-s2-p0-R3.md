---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 2628
---
# One-Card Poker with Private Sidebar Playbook

## Communication Strategy
- **Hand 1**: Propose sharing exact numerical card ranks truthfully each hand so whoever holds the higher card can contest the pot while the lower card folds, but do **not** reveal my actual card rank immediately. (e.g. "Let's share exact numeric card ranks each hand so the higher card contests and the lower folds to beat p2. What card do you have?")
- **Subsequent Hands**:
  - If player 1 shares an exact, credible numeric rank in their message or establishes truthful sharing, share my exact card rank truthfully and coordinate accordingly.
  - If player 1 gives vague, non-committal replies (e.g. "decent card", "let's see how it plays out") or fails to share a number, strictly stop sharing my card rank. Send neutral, boilerplate messages like `[msg: Good luck this hand.]` or `[msg: Let's see how it plays out.]`. Never leak free card information without reciprocal exact numbers.

## Betting Strategy as Player 0 (First to Act)

### Opening Action (Bet to me: 0)
- **Top Premium Cards (13, 14)**:
  - `[bet: raise]` to extract value and build the pot, unless player 1 credibly signaled a 14 when I hold a 13.
- **Strong/Borderline Cards (11, 12)**:
  - If player 1 credibly signaled a card lower than mine, `[bet: raise]`.
  - In uncoordinated 3-way pots with no reliable info from player 1, `[bet: call]` (check) for 0 chips. Against two random opponents, a 12 loses or chops frequently enough that raising out of position into unknown hands bleeds chips.
- **Medium Cards (8, 9, 10)**:
  - Always `[bet: call]` (check) for 0 chips to control pot size.
- **Weak Cards (2 through 7)**:
  - Always `[bet: call]` (check) for 0 chips. Never bluff into two opponents.

### Facing a Raise / Re-opened Action
- **Card 14 (Ace)**: Always `[bet: call]`.
- **Card 13 (King)**: `[bet: call]` unless both opponents raised/called heavy action and one has credibly revealed a 14.
- **Cards 11 and 12**: `[bet: fold]` in multi-way pots where player 2 raises or multiple players are in. Only consider calling against a known loose single bettor when closing the action.
- **Cards 10 and below**: Strictly `[bet: fold]`. Never call a raise with weak or mediocre hands.

## Endgame Adjustments
- **Protecting a Lead (Hands 7–8)**: If leading in chip count, avoid raising with non-premium hands (12 and below). Check for 0 and fold to raises unless holding 13 or 14.
- **Trailing / Desperation (Hand 8)**: If behind on chips and needing a swing to win, raise aggressively with 11+ and call raises with 12+, folding weak hands that cannot win multi-way showdowns.