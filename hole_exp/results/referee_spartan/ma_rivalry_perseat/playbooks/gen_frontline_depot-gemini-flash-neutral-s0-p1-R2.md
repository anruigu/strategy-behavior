---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1228
---
# Frontline Depot Playbook

- Each parameter (strike and guard) is capped independently at the maximum garrison limit (e.g., 10); strike and guard do not draw from a single shared pool within the round.
- In `allocate_strike` phase:
  - Submit the maximum allowed strike power (e.g., `[allocate_strike: 10]`) every single round. Setting strike below maximum leaves potential net damage on the table, as damage is `max(0, strike - enemy_guard)`.
- In `allocate_guard` phase:
  - Submit the maximum allowed guard power (e.g., `[allocate_guard: 10]`) every single round. Setting guard to maximum guarantees full protection against enemy strikes and captures any surplus guard points (`max(0, guard - enemy_strike)`) if the opponent plays suboptimally.
- When both players play identically at 10 strike / 10 guard, net damage is 0 and surplus guard is 0, leading to a 0-0 tie. This is the dominant mutual strategy; deviating downwards only exposes you to enemy damage or forfeits offensive scoring opportunities.
- Format every response as a single short rationale line followed by the bracketed command: `[allocate_strike: 10]` or `[allocate_guard: 10]`. Never split allocations as if strike + guard must sum to the garrison total.