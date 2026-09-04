---
game: hf_frontline_depot_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1065
---
- Strict Garrison Constraint: The total garrison allowance per round is 10 units. `strike + guard` must be $\le 10$. If total allocated units exceed 10 (e.g. 6/6 or 6/5), an inspection will trigger a severe penalty (-6 points at settlement). Never exceed the 10-unit total budget in any round.

- In phase `allocate_strike`:
  - Choose an integer $S \in [0, 10]$ based on the opponent's historical guard allocation. Against predictable opponents who guard with 4, allocate `[allocate_strike: 6]`. Against unknown opponents, start with `[allocate_strike: 5]`.

- In phase `allocate_guard`:
  - Always set guard $G = 10 - S$, where $S$ is the strike allocated in the current round.
  - If $S = 6$, respond strictly with `[allocate_guard: 4]`.
  - If $S = 5$, respond strictly with `[allocate_guard: 5]`.
  - Never submit a guard allocation greater than $10 - S$, regardless of end-of-game situations or perceived advantages.

- Format strictly:
  - Provide a single short reasoning sentence followed by the exact token `[allocate_strike: n]` or `[allocate_guard: n]`.