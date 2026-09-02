---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1787
---
### Garrison Mechanics & Rules of Thumb
- The garrison limit (e.g., 10 units) applies independently to each phase: `strike` can be up to 10 and `guard` can be up to 10 in the same round without sharing a combined 10-unit pool.
- Scoring awards:
  1. Net damage dealt: `max(0, my_strike - opponent_guard)`
  2. Surplus guard: `max(0, my_guard - opponent_strike)`
- Playing `strike: 10` and `guard: 10` strictly dominates any lower allocation:
  - Strike 10 maximizes net damage if the opponent under-guards and prevents the opponent from earning surplus guard points.
  - Guard 10 prevents the opponent from dealing net damage and earns surplus points whenever the opponent strikes below 10.
- When both players play 10/10, the round outcome is 0-0. Deviating downward unilaterally concedes points.

### Strike Phase Protocol
- In every round (Rounds 1 to 4):
  - Submit `[allocate_strike: M]`, where `M` is the maximum public garrison allowance (typically 10).
  - Format response strictly as the bracketed token with an optional single brief line of reasoning:
    `[allocate_strike: 10]`

### Guard Phase Protocol
- In every round (Rounds 1 to 4):
  - Submit `[allocate_guard: M]`, where `M` is the maximum public garrison allowance (typically 10).
  - Format response strictly as the bracketed token with an optional single brief line of reasoning:
    `[allocate_guard: 10]`

### What Not To Do
- Do not assume a shared budget where `strike + guard <= garrison_limit`. The arbiter validates each parameter independently against the limit.
- Never reduce strike below maximum; lowering strike gives the opponent free surplus guard points (`opp_guard - my_strike`).
- Never reduce guard below maximum; lowering guard gives the opponent free net damage points (`opp_strike - my_guard`).