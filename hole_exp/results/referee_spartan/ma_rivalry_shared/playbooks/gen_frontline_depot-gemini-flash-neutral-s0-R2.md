---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1865
---
# Playbook for Frontline Depot

### Understanding Rules & Resource Constraints
- Strike and guard parameters are checked independently against the maximum garrison limit: both strike (0 to 10) and guard (0 to 10) can be up to 10 each in every single round. There is no combined budget sum restriction across the two phases in a round.
- Scoring gives +1 point per unit of net strike damage (`max(0, my_strike - opp_guard)`) and +1 point per unit of surplus guard (`max(0, my_guard - opp_strike)`).
- Maximizing guard is strictly dominant or near-dominant because guard is free from opportunity cost with strike and directly produces surplus guard points against any opponent strike below the guard value.

### Strike Phase Strategy
- In Round 1, open with `[allocate_strike: 6]` to test the opponent's defensive posture.
- In Round 2:
  - If the opponent played guard 6 in Round 1, escalate to `[allocate_strike: 7]` to attempt piercing.
- In Round 3:
  - If the opponent played guard 7 in Round 2, escalate to `[allocate_strike: 8]`.
- In Round 4:
  - Allocate `[allocate_strike: 10]` to maximize potential damage in the final round.

### Guard Phase Strategy
- Always allocate at least as much guard as anticipated opponent strike; since guard does not draw from the strike budget, aggressively high guard is optimal.
- Round 1: Set `[allocate_guard: 6]`.
- Round 2: Set `[allocate_guard: 7]` (never lower than 7). Under-guarding at 6 when the opponent strikes with 7 concedes net damage and surplus guard.
- Round 3: Set `[allocate_guard: 8]`.
- Round 4: Set `[allocate_guard: 10]` to completely negate up to max strike (10) and harvest surplus guard points if the opponent under-allocates strike.

### Formatting
- Keep brief reasoning to at most one short line.
- Always output the exact required token format: `[allocate_strike: n]` and `[allocate_guard: n]`.