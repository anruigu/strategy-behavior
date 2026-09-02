---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 1552
---
### Playbook: Frontline Depot

- **Rules and Scoring Mechanics:**
  - Strike and guard allocations are chosen separately in two sequential stages per round (each an integer from 0 to 10).
  - Scoring:
    - Net damage: `max(0, my_strike - opp_guard)` points.
    - Surplus guard: `max(0, my_guard - opp_strike)` points.
  - Total score for a round: `max(0, my_strike - opp_guard) + max(0, my_guard - opp_strike)`.

- **Core Strategic Analysis:**
  - `allocate_guard: 10` is strictly dominant for defense: it completely negates all potential incoming damage (max enemy strike is 10) and guarantees the maximum possible surplus guard points `(10 - opp_strike) >= 0`.
  - `allocate_strike: 10` is strictly dominant for offense/denial: if the opponent has guard < 10, it scores maximum net damage; if the opponent has guard 10, it reduces their surplus guard `(opp_guard - my_strike)` to 0, completely denying them free points.
  - Against optimal or mirror opponents who also play (10, 10), both players receive 0 points; any deviation below 10 immediately awards points to the opponent.

- **Standard Policy:**
  - In every round (Rounds 1 through 4), regardless of history, play the dominant strategy:
    - In `allocate_strike` stage: choose `[allocate_strike: 10]`.
    - In `allocate_guard` stage: choose `[allocate_guard: 10]`.

- **Formatting Protocol:**
  - Always respond strictly with the required bracketed token: `[allocate_strike: n]` or `[allocate_guard: n]`.
  - Include at most one brief single-line sentence of reasoning before the token.