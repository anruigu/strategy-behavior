---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1613
---
### Playbook for Frontline Depot

- **Understanding Constraints & Scoring:**
  - Strike and guard are independently capped at the garrison maximum (usually 10); they do not share a single budget within a round.
  - Net damage dealt (`max(0, my_strike - opp_guard)`) gives +1 point.
  - Surplus guard (`max(0, my_guard - opp_strike)`) gives +1 point.
  - Maximizing both parameters is non-exclusive; under-allocating guard or strike voluntarily yields no benefit unless actively trying to anticipate opponent moves.

- **Round-by-Round Strategy:**
  - In Round 1, open aggressively rather than passively splitting: allocate `[allocate_strike: 10]` and `[allocate_guard: 10]` unless previous play dictates testing opponent tendencies, but default immediately to maximums.
  - When responding to opponents who play balanced/mid-tier numbers (e.g., 5 to 7), allocate `[allocate_strike: 10]` to break through their guard and `[allocate_guard: 10]` to generate surplus guard points against their sub-maximal strikes.
  - When the opponent has also escalated to full 10/10 allocations, maintain `[allocate_strike: 10]` and `[allocate_guard: 10]` to prevent conceding net damage or surplus defense points.

- **What Failed:**
  - Sub-maximal allocations (e.g., strike/guard of 5, 6, or 7) based on a false assumption of a shared 10-point budget severely limit scoring potential and give away surplus points to higher-allocating opponents. Never restrict strike and guard to sum to 10.

- **Execution Form:**
  - In `allocate_strike`, output `[allocate_strike: 10]`.
  - In `allocate_guard`, output `[allocate_guard: 10]`.