---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1233
---
# Frontline Depot Playbook

- Each parameter (strike and guard) is capped independently at the maximum public garrison allowance (e.g., 10); strike and guard do not draw from a single shared pool within the round.
- In `allocate_strike` phase:
  - Submit the maximum allowed strike power (e.g., `[allocate_strike: 10]`) every round. Setting strike below the maximum leaves potential net damage on the table, as damage is `max(0, strike - enemy_guard)`.
- In `allocate_guard` phase:
  - Submit the maximum allowed guard power (e.g., `[allocate_guard: 10]`) every round. Setting guard to the maximum guarantees complete defense against enemy strikes and captures any surplus guard points (`max(0, guard - enemy_strike)`) if the opponent ever allocates less than max strike.
- When both players play maximum strike and guard (e.g., 10/10 vs 10/10), net damage and surplus guard are both 0, resulting in a 0-0 score. Playing (max_strike, max_guard) is weakly dominant; deviating downward strictly loses points if the opponent maintains max allocations.
- Output format: Provide one short line of reasoning followed by the exact bracketed token: `[allocate_strike: n]` or `[allocate_guard: n]`, where `n` is the public garrison allowance.