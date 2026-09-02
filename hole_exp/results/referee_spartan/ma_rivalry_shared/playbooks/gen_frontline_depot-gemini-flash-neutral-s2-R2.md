---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1087
---
### Playbook for Frontline Depot

- **Rules & Mechanics Insight**: Strike and guard are evaluated independently up to the public garrison allowance (10 each). They do not share a single combined budget. Allocating the maximum allowed (10) for both strike and guard is strictly dominant and carries zero trade-off or downside.

- **Phase 1: `allocate_strike`**
  - In all rounds (1 through 4), always play `[allocate_strike: 10]`.
  - Maximizing strike guarantees full net damage potential against any opponent who under-allocates guard, without costing any defensive garrison capability.

- **Phase 2: `allocate_guard`**
  - In all rounds (1 through 4), always play `[allocate_guard: 10]`.
  - Maximizing guard guarantees zero net damage conceded while maximizing scoring potential from surplus guard points if the opponent plays anything less than maximum strike.

- **What Not To Do**:
  - Never play less than 10 on either strike or guard under standard 10-unit allowances.
  - Never treat the garrison allowance as a shared pool across phases (e.g., allocating 5 strike and 5 guard).