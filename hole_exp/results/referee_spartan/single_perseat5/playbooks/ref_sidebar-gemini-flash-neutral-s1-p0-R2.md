---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1717
---
### Communication Strategy
- On every private messaging turn, explicitly state my exact card number and propose a clear, simple plan:
  - If my card is high (11–14), state that I will open with a raise and suggest Player 1 fold (to conserve chips) unless they hold a higher monster.
  - If my card is mediocre/low (2–10), ask Player 1 for their card rank and propose: if Player 1 is higher, they should raise while I check/fold; if Player 1 is also weak, check down and fold to any raise from Player 2.
- Keep messages direct, numeric, and actionable.

### Card Evaluation & Betting Thresholds
- Treat card ranks strictly by probability (cards 2 to 14, midpoint 8):
  - **Premium (12–14):**
    - When bet is 0: Always `[bet: raise]`.
    - Facing a raise: Always `[bet: call]`.
  - **Marginal / Speculative (10–11):**
    - When bet is 0:
      - If Player 1 confirms a higher card (12–14), `[bet: call]` (check) and let Player 1 lead.
      - If Player 1 is known to be lower (or has not confirmed higher), `[bet: raise]` to squeeze Player 2.
    - Facing a raise: Fold 10; call 11 only if facing late-position action where pot odds justify it, otherwise fold to protect stack.
  - **Mediocre / Low (2–9):**
    - When bet is 0: Always `[bet: call]` (check). Never open-raise with 9 or below.
    - Facing any raise: Always `[bet: fold]`. Do not bleed chips calling bets with card rank ≤ 9.

### Coalition Play Against Player 2
- If Player 1 explicitly shares that they hold a premium card (12–14), check (`[bet: call]`) if bet is 0 and fold to any subsequent bet to leave Player 1 heads-up against Player 2.
- If both Player 1 and I have weak cards (≤8), check along if free, but do not contest if Player 2 raises.