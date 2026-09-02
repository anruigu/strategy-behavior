---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 2328
---
# Playbook for Frontline Depot

### Understanding Rules & Resource Constraints
- The garrison limit applies independently per parameter (strike $\le 10$, guard $\le 10$) or as a round budget depending on arbiter checks, but allocations must strictly adhere to the per-phase limit (0 to 10).
- Scoring gives $+1$ point per unit of net strike damage (`max(0, my_strike - opp_guard)`) and $+1$ point per unit of surplus guard (`max(0, my_guard - opp_strike)`).
- When the opponent allocates moderate strike and guard (e.g. 5–6), allocating matching or slightly superior guard yields reliable points from surplus defense, while matching or slightly exceeding their guard captures net damage.

### Strike Phase Strategy
- In Round 1, open with `[allocate_strike: 6]` to test the opponent's guard while maintaining high baseline offensive pressure.
- In subsequent rounds:
  - If the opponent consistently plays balanced splits (around 5–6 strike and 4–6 guard), allocate `[allocate_strike: 6]` or `[allocate_strike: 7]` to reliably pierce guard while keeping allocations stable.
  - If the opponent escalates their numbers, increase strike power to `[allocate_strike: 8]` to overpower their guard.
  - In Round 4, if the opponent has previously mirrored high escalation or if the arbiter permits independent parameter scaling, allocate `[allocate_strike: 10]` (or `[allocate_strike: 6]` if maintaining a conservative 10-total sum split).

### Guard Phase Strategy
- In Round 1, set `[allocate_guard: 5]` or `[allocate_guard: 6]` to safely block baseline 5–6 strikes and earn surplus guard points against under-invested attacks.
- In subsequent rounds:
  - Track the opponent's previous strike power; allocate guard equal to or 1 unit higher than their anticipated strike (e.g., if they strike with 6, allocate `[allocate_guard: 6]` or `[allocate_guard: 7]`).
  - Never under-guard (e.g., allocating guard $\le 4$) against an opponent who strikes for 6+, as this concedes both net strike damage and forfeits surplus guard points.
  - In Round 4, allocate `[allocate_guard: 10]` when pushing maximum garrison values to eliminate incoming damage and maximize defensive surplus.

### Formatting
- Keep the brief reasoning to one sentence.
- Always output the exact required token format: `[allocate_strike: n]` and `[allocate_guard: n]`.