---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1499
---
### Understanding the Rules and Mechanics

- Garrison allowance allows submitting independent strike and guard values up to 10 each per round.
- Scoring rules per round:
  - Net damage dealt: `max(0, my_strike - opp_guard)`
  - Surplus guard: `max(0, my_guard - opp_strike)`
- Strategy analysis:
  - Playing `strike: 10` maximizes offensive damage if opponent guard < 10, and reduces opponent surplus guard to 0.
  - Playing `guard: 10` prevents all opponent net damage, and maximizes surplus guard points if opponent strike < 10.
  - Allocating `10` strike and `10` guard is a dominant strategy: any lower strike awards surplus guard to the opponent, and any lower guard awards net damage to the opponent.

### Playbook

- In Round 1:
  - When `allocate_strike` is prompted, submit `[allocate_strike: 10]`.
  - When `allocate_guard` is prompted, submit `[allocate_guard: 10]`.

- In Subsequent Rounds (Rounds 2–4):
  - In `allocate_strike`, always submit `[allocate_strike: 10]`. This punishes opponent guard reductions and prevents opponent surplus guard.
  - In `allocate_guard`, always submit `[allocate_guard: 10]`. This prevents opponent net damage and scores surplus guard if opponent strike drops below 10.
  - Never lower either strike or guard below 10, regardless of past opponent actions or score state.

- Response Format:
  - Output either purely the bracketed action or at most one short sentence of reasoning followed immediately by `[allocate_strike: 10]` or `[allocate_guard: 10]`.