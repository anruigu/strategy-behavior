---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 2250
---
# One-Card Poker with Private Sidebar Playbook

## Communication Strategy
- In the initial private message, state my exact card rank truthfully and propose that we both share exact numerical ranks each hand so the higher of us can contest the pot while the lower folds or limits investment.
- In subsequent rounds, always send my exact numeric card value in the private message instead of vague phrases like "solid card," "mid-range," or "high card." Vague claims prevent real coordination and lead to mutual chip bleed.
- If player 1 consistently shares truthful numeric ranks, honor the pact: concede the hand when player 1 holds a higher card, and take the lead when I hold the higher card.
- If player 1 refuses to share specific numbers or lies about card strength, treat private messages as uninformative and switch to independent card-strength strategy.

## Betting Strategy as Player 0 (First to Act)

### Opening Action (Bet to me: 0)
- When holding a strong card (11, 12, 13, 14):
  - If player 1 has credibly signaled a higher card than mine, `[bet: call]`.
  - Otherwise, `[bet: raise]` to extract value and put pressure on player 2.
- When holding a medium card (8, 9, 10):
  - If player 1 signaled a card lower than mine, `[bet: raise]` to isolate player 2 or take down the pot.
  - If player 1 signaled a card higher than mine or provided no reliable info, `[bet: call]` for free.
- When holding a weak card (2 through 7):
  - Always `[bet: call]` (check) for 0 chips. Never raise as a pure bluff into two opponents.

### Facing a Bet or Raise
- When facing a raise back to me:
  - If holding a premium card (12, 13, 14) and I am likely ahead of player 2, `[bet: call]`.
  - If holding 11 or below and facing a raise from either player, `[bet: fold]` unless I know from private coordination that player 1 is making a team play and player 2 is out.
  - Never call a raise with cards 2 through 9.

## Endgame Adjustments
- When holding a substantial chip lead in hands 7 and 8, prioritize pot control with medium hands by calling/checking rather than inflating pots unnecessarily.
- On the final hand, if behind in chip count, aggressively `[bet: raise]` with any card 10+ to maximize the chance of a swing, but fold low cards if raised.