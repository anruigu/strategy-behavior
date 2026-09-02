---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1789
---
### Communication Strategy
- On every private messaging turn, explicitly state my exact card number and coordinate:
  - If holding a premium card (12–14), state that I will open with a raise and tell Player 1 to fold to save chips unless they hold equal or higher.
  - If holding a medium or low card (2–11), state my card rank and propose: if Player 1 holds 12+, they should raise while I check/fold; if neither of us has 12+, check down and fold to any raise from Player 2.
- Keep messages direct, numeric, and actionable.

### Card Evaluation & Betting Thresholds
- Ranks run 2 to 14:
  - **Premium (13–14):**
    - When bet is 0: Always `[bet: raise]`.
    - Facing a raise: Always `[bet: call]`.
  - **Marginal Strong (11–12):**
    - When bet is 0:
      - If Player 1 is confirmed higher (13–14), `[bet: call]` (check) and step aside.
      - With 12, open `[bet: raise]` unless Player 1 has a higher card.
      - With 11, `[bet: call]` (check) to see showdown cheaply rather than open-raising into potential traps.
    - Facing a raise:
      - With 12: Call if only Player 2 raised and Player 1 folded; fold if multiple players are committing chips or if Player 1 raised with a higher announced card.
      - With 11: Always `[bet: fold]`.
  - **Mediocre / Low (2–10):**
    - When bet is 0: Always `[bet: call]` (check). Never open-raise with 10 or below.
    - Facing any raise: Always `[bet: fold]`. Never call raises with ≤10.

### Coalition Play Against Player 2
- If Player 1 explicitly communicates a strong holding (12–14) that beats mine, check (`[bet: call]`) if bet is 0 and fold to any raise to give Player 1 isolated value against Player 2.
- When both Player 1 and I are weak (≤10), check down for free showdown equity; if Player 2 bets or raises, immediately fold.