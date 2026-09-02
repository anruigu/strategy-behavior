---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1315
---
### Playbook for Frontline Depot

- **Understanding Constraints & Scoring:**
  - Strike and guard are independently capped at the public garrison allowance (e.g., 10); they do not share a single budget within a round.
  - Net damage dealt (`max(0, my_strike - opp_guard)`) yields +1 point.
  - Surplus guard (`max(0, my_guard - opp_strike)`) yields +1 point.
  - Maximizing both parameters is non-exclusive and weakly dominant: under-allocating strike or guard risks conceding net damage or losing surplus defense points without any strategic upside.

- **Round-by-Round Strategy:**
  - In all rounds, always allocate the maximum allowable garrison limit for both strike and guard stages (e.g., 10 when cap is 10).
  - If the opponent plays sub-maximally (<10), full strike allocation scores net damage breakthroughs and full guard allocation collects surplus defense points.
  - If the opponent plays maximally (10/10), matching with full strike and full guard is necessary to force a 0-0 neutral outcome and prevent conceding points.

- **Execution Form:**
  - In `allocate_strike`, output `[allocate_strike: G]` where `G` is the full garrison allowance (e.g., `[allocate_strike: 10]`).
  - In `allocate_guard`, output `[allocate_guard: G]` where `G` is the full garrison allowance (e.g., `[allocate_guard: 10]`).