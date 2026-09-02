---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 1434
---
# Playbook: Frontline Depot

- **Rules & Mechanics**:
  - The garrison limit (e.g., 10 units) is an independent maximum cap for both strike and guard in every round. Allocating the max in strike does not deplete guard capacity.
  - Scoring: Net damage dealt = `max(0, my_strike - opp_guard)`. Surplus guard = `max(0, my_guard - opp_strike)`. Total points per round = Net damage + Surplus guard.
  - When both players allocate equal values (e.g., 10 strike and 10 guard), net damage is 0 and surplus guard is 0, yielding a draw (+0.0).

- **Core Strategy**:
  - Against an opponent who always plays full capacity (10 strike / 10 guard) every round, playing 10/10 is strictly required to prevent conceding net damage (if guard < 10) while neutralizing their defense.
  - Against any sub-maximal allocations, playing the maximum limit (10/10) maximally breaches opponent guard and captures maximum surplus guard points.
  - Therefore, playing maximum strike and maximum guard across all rounds is the dominant safe and exploitative strategy.

- **Round Execution**:
  - In every round and phase, allocate the full garrison allowance (10):
    - `allocate_strike`: Respond with `[allocate_strike: 10]`
    - `allocate_guard`: Respond with `[allocate_guard: 10]`

- **Format & Response Protocol**:
  - Provide at most one short line of reasoning.
  - End strictly with `[allocate_strike: n]` or `[allocate_guard: n]` with no trailing text.