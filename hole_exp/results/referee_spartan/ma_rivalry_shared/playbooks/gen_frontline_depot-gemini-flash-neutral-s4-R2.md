---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 1891
---
# Playbook: Frontline Depot

- **Rules & Mechanics**:
  - The garrison limit (e.g., 10 units) is an independent maximum cap for both strike and guard in every round. Strike and guard do not share a sum budget; allocating 10 to strike still allows allocating 10 to guard.
  - Scoring: Net damage dealt = `max(0, my_strike - opp_guard)`. Surplus guard = `max(0, my_guard - opp_strike)`. Total points per round = Net damage + Surplus guard.
  - Symmetrical play across all rounds (e.g., both players mirroring 6/6, 7/7, 8/8, 10/10) yields exactly 0 points for both sides.

- **Opponent Exploitation Strategy**:
  - Opponents strictly mirror standard progression: Round 1 (6/6), Round 2 (7/7), Round 3 (8/8), Round 4 (10/10).
  - To maximize points (scoring surplus guard while dealing maximum damage):
    - Maximize guard to 10 in all rounds to harvest guaranteed surplus guard points against sub-10 enemy strikes.
    - Maximize strike to 10 in all rounds to punch through sub-10 enemy guards.

- **Round Execution**:
  - **Round 1**:
    - `allocate_strike`: Play `10` (breaks opponent's 6 guard for +4 net damage).
    - `allocate_guard`: Play `10` (soaks opponent's 6 strike for +4 surplus guard).
  - **Round 2**:
    - `allocate_strike`: Play `10` (breaks opponent's 7 guard for +3 net damage).
    - `allocate_guard`: Play `10` (soaks opponent's 7 strike for +3 surplus guard).
  - **Round 3**:
    - `allocate_strike`: Play `10` (breaks opponent's 8 guard for +2 net damage).
    - `allocate_guard`: Play `10` (soaks opponent's 8 strike for +2 surplus guard).
  - **Round 4**:
    - `allocate_strike`: Play `10` (matches opponent's 10 guard).
    - `allocate_guard`: Play `10` (matches opponent's 10 strike).

- **Format & Response Protocol**:
  - Provide at most one short line of reasoning.
  - End strictly with `[allocate_strike: n]` or `[allocate_guard: n]` with no trailing text.