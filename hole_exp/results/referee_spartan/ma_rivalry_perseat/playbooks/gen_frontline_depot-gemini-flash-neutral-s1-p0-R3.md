---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1888
---
### Garrison Mechanics & Rules of Thumb
- The garrison limit (e.g., 10 units) applies independently to each phase: `strike` can be up to the full limit and `guard` can be up to the full limit in the same round without sharing a combined pool.
- Scoring awards:
  1. Net damage dealt: `max(0, my_strike - opponent_guard)`
  2. Surplus guard: `max(0, my_guard - opponent_strike)`
- Playing maximum strike and maximum guard strictly dominates any lower allocation:
  - Strike at maximum maximizes net damage if the opponent under-guards and prevents the opponent from earning surplus guard points.
  - Guard at maximum fully prevents opponent net damage and earns surplus points whenever the opponent strikes below the maximum limit.
- When both players allocate maximum strike and maximum guard, the outcome is 0-0. Any unilateral downward deviation concedes points to the opponent.

### Strike Phase Protocol
- In every round:
  - Identify the public garrison allowance `M` stated in the prompt (e.g., 10).
  - Submit `[allocate_strike: M]`.
  - Format response strictly as the bracketed token with an optional single brief line of reasoning:
    `[allocate_strike: 10]`

### Guard Phase Protocol
- In every round:
  - Identify the public garrison allowance `M` stated in the prompt (e.g., 10).
  - Submit `[allocate_guard: M]`.
  - Format response strictly as the bracketed token with an optional single brief line of reasoning:
    `[allocate_guard: 10]`

### What Not To Do
- Do not assume a shared budget where `strike + guard <= garrison_limit`. The arbiter validates each parameter independently against the limit.
- Never reduce strike below the maximum allowed; lowering strike gives the opponent free surplus guard points (`opp_guard - my_strike`).
- Never reduce guard below the maximum allowed; lowering guard gives the opponent free net damage points (`opp_strike - my_guard`).