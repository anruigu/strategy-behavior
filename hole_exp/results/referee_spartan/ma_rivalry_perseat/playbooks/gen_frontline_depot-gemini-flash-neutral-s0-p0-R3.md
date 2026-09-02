---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1485
---
### Playbook: Frontline Depot

- **Core Mechanics & Game Theory**:
  - The garrison limit (e.g., 10) applies independently to each parameter (`allocate_strike` and `allocate_guard`), not as a shared pool across both actions. Allocating full strike does not deplete available guard units.
  - Scoring per round:
    - Net Damage Dealt = $\max(0, \text{MyStrike} - \text{EnemyGuard})$
    - Guard Surplus = $\max(0, \text{MyGuard} - \text{EnemyStrike})$
  - Both scoring components are monotonically non-decreasing with respect to my own strike and guard allocations, with zero cost or penalty for maximizing both.
  - Maximal allocation (10 strike, 10 guard) is the strictly dominant strategy. If both players play 10/10, the round ends 0–0. Any sub-maximal play strictly harms defensive safety or misses potential offensive/surplus points.

- **Strike Allocation Strategy**:
  - In every round, always allocate the full public garrison allowance (e.g., `[allocate_strike: 10]`).
  - Never allocate below the maximum allowance.

- **Guard Allocation Strategy**:
  - In every round, always allocate the full public garrison allowance (e.g., `[allocate_guard: 10]`).
  - Never allocate below the maximum allowance.

- **Response Formatting**:
  - Provide at most one short line of reasoning before the action token.
  - Output the required bracketed action token:
    - `[allocate_strike: n]` (where $n$ is the full allowance)
    - `[allocate_guard: n]` (where $n$ is the full allowance)