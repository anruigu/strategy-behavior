---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1423
---
### Playbook for Frontline Depot

- **Rules & Mechanics Insight**: Strike and guard are evaluated independently up to the public garrison allowance (10 each). They do not share a single combined budget. Allocating the maximum allowed (10) for both strike and guard is strictly dominant and carries zero trade-off or downside. When both players play 10/10, net damage is 0 and surplus guard is 0, yielding a 0-0 tie.

- **Phase 1: `allocate_strike`**
  - In all rounds (1 through 4), always play `[allocate_strike: 10]` (or the maximum public garrison allowance specified).
  - Maximizing strike guarantees full net damage potential against any opponent who under-allocates guard, without costing any defensive garrison capability.

- **Phase 2: `allocate_guard`**
  - In all rounds (1 through 4), always play `[allocate_guard: 10]` (or the maximum public garrison allowance specified).
  - Maximizing guard guarantees zero net damage conceded while maximizing scoring potential from surplus guard points if the opponent plays anything less than maximum strike.

- **Response Formatting**:
  - Keep reasoning to at most one short line, followed immediately by `[allocate_strike: 10]` or `[allocate_guard: 10]`.

- **What Not To Do**:
  - Never play less than the maximum allowable units on either strike or guard.
  - Never treat the garrison allowance as a shared pool across phases (e.g., allocating 5 strike and 5 guard).