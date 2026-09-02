---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1875
---
### Communication Strategy
- **Detect Bot/Deceptive Partner Early**: Player 1 frequently lies or sends canned vague messages (e.g. claiming "mid-range around 8" while holding 13 or 14). Never assume Player 1's messages reflect their actual card rank.
- **Message Policy**: Send my exact card rank or concise status every hand to maintain coordination opportunities if Player 1 is cooperative, but never base critical showdown or raise decisions on Player 1's self-reported holding.

### Betting Strategy
- **Acting First (Player 0, current bet = 0)**:
  - **Holding 13–14 (Nuts / Near Nuts)**: Always `[bet: raise]`.
  - **Holding 12**: `[bet: raise]` to extract value and pressure Player 2, but fold if Player 2 subsequently raises over.
  - **Holding 11**:
    - Default to `[bet: call]` (check). Open-raising with 11 out of position consistently loses to Player 1's hidden high traps and Player 2's high cards. Only raise 11 if Player 1 is verifiably truthful and weak.
  - **Holding 2–10 (Weak to Medium)**: Always `[bet: call]` (take the free check). Never open-raise.

- **Facing a Raise (when current bet > 0 or after checking)**:
  - **Holding 14 (Ace)**: Always `[bet: call]` to contest.
  - **Holding 13 (King)**: `[bet: call]` against a single bettor unless facing multiple raises/calls indicating 14.
  - **Holding 12**: `[bet: call]` only heads-up if pot odds justify it and Player 2 raised lightly; otherwise `[bet: fold]`.
  - **Holding 2–11**: Always `[bet: fold]`. Calling a raise with 11 or lower against two active opponents is negative expected value.

### Mistakes to Avoid
- Never trust Player 1's claims of having a "mid-range card" or "around an 8"; showdown history proves they often hold Aces and Kings while saying this.
- Do not open-raise with 10 or 11 from seat 0.
- Never call a raise with 2–11 when facing aggression from Player 1 or Player 2.