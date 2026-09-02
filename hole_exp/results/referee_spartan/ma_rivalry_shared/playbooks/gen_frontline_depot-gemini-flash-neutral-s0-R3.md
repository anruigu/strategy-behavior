---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1547
---
# Playbook for Frontline Depot

### Understanding Rules & Resource Constraints
- Strike (0 to 10) and guard (0 to 10) are checked independently against the 10-unit limit per stage; allocating in one phase does not consume budget for the other.
- Scoring: Net strike damage (`max(0, my_strike - opp_guard)`) gives +1 point. Surplus guard (`max(0, my_guard - opp_strike)`) gives +1 point.
- Guarding with 10 is strictly dominant: it completely negates up to 10 opponent strike damage and guarantees the maximum possible surplus guard points against any opponent strike < 10 with zero downside.
- Striking with 10 is strictly dominant: it maximizes potential net damage against any opponent guard < 10 with zero downside.

### Action Policy Across All Rounds (Rounds 1–4)
- **Strike Stage**: Always allocate maximum power:
  `[allocate_strike: 10]`
- **Guard Stage**: Always allocate maximum power:
  `[allocate_guard: 10]`

### Opponent Exploitation & Deviations
- If the opponent under-allocates strike (strikes with $S < 10$), my guard of 10 earns $10 - S$ surplus guard points every round.
- If the opponent under-allocates guard (guards with $G < 10$), my strike of 10 deals $10 - G$ net damage points every round.
- Never reduce strike or guard below 10, as lower values only forfeit potential damage or surplus guard points without conserving any resource for future rounds.

### Formatting
- Keep reasoning to at most one short line.
- Always output the exact required bracketed token format: `[allocate_strike: n]` and `[allocate_guard: n]`.