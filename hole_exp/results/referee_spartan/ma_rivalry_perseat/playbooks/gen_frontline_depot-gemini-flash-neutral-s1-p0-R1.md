---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1997
---
### Garrison Mechanics & Rules of Thumb
- The garrison limit (e.g., 10 units) applies independently to each phase, or per action: `strike` can be up to 10 and `guard` can be up to 10 in the same round without sharing a combined pool.
- Never hold back guard thinking it must be `10 - strike`. Allocating low guard (like 2 or 3) gives the opponent free net damage points and surrenders surplus guard points.
- Scoring awards:
  1. `max(0, my_strike - opponent_guard)`
  2. `max(0, my_guard - opponent_strike)`
- Therefore, maximizing both strike and guard simultaneously dominates conservative splits whenever the garrison allowance resets every round.

### Strike Phase Protocol
- In Round 1:
  - When prompted for `[allocate_strike: n]`, submit `[allocate_strike: 10]` (or the maximum allowed garrison value) to maximize damage potential against opening defensive setups.
- In Subsequent Rounds:
  - Track opponent guard patterns:
    - If the opponent frequently guards at maximum (10), maintain `[allocate_strike: 10]` to prevent them from earning surplus guard points on me.
    - If the opponent under-guards (e.g., 4–7), submit `[allocate_strike: 10]` to score maximum net damage.

### Guard Phase Protocol
- In Round 1:
  - When prompted for `[allocate_guard: n]`, submit `[allocate_guard: 10]` (or maximum allowed garrison value) to block full strikes and harvest surplus guard points if they play low strike.
- In Subsequent Rounds:
  - When prompted for `[allocate_guard: n]`, submit `[allocate_guard: 10]`. Never reduce guard below the maximum possible enemy strike unless a rule specifically enforces a shared strike/guard budget across rounds.

### What Not To Do
- Do not artificially constrain `strike + guard = 10`. Setting guard to `10 - strike` (such as `[allocate_guard: 4]` after `strike: 6` or `[allocate_guard: 2]` after `strike: 8`) needlessly bleeds points.
- Do not play "balanced" mid-values like 5/5 or 6/4 when independent 10/10 allocations are accepted by the arbiter.