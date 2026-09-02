---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1473
---
### Playbook: Frontline Depot

- **Core Mechanics & Game Theory**:
  - The garrison limit (e.g., 10) applies independently to each parameter (`allocate_strike` and `allocate_guard`), not as a shared sum. Allocating full strike does not reduce guard capacity.
  - Scoring per round:
    - Net Damage Dealt = $\max(0, \text{MyStrike} - \text{EnemyGuard})$
    - Guard Surplus = $\max(0, \text{MyGuard} - \text{EnemyStrike})$
  - Because points are strictly non-negative and monotonically non-decreasing in own allocations, maximal allocation (10 in both strike and guard) is the dominant strategy regardless of opponent moves.
  - When both players play 10/10, score is 0–0. Playing less than 10 in either parameter strictly exposes you to point loss or missed scoring opportunities.

- **Strike Allocation Strategy**:
  - In every round, always allocate the maximum allowed garrison limit: `[allocate_strike: 10]`.
  - Never lower strike allocation. This ensures maximum damage extraction if the opponent under-guards.

- **Guard Allocation Strategy**:
  - In every round, always allocate the maximum allowed garrison limit: `[allocate_guard: 10]`.
  - Never lower guard allocation. This prevents all enemy damage and extracts maximum surplus points if the opponent under-strikes.

- **Response Formatting**:
  - Always respond with exactly one concise line of reasoning followed immediately by the bracketed token:
    - `[allocate_strike: 10]`
    - `[allocate_guard: 10]`