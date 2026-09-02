---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 2625
---
### Playbook: Frontline Depot

- **Understand the Rules and Resource Constraints:**
  - Strike and guard allocations are chosen separately each round, each an integer from 0 to 10.
  - Scoring:
    - Net damage: `max(0, my_strike - opp_guard)` points.
    - Surplus guard: `max(0, my_guard - opp_strike)` points.
  - Total round points for a player: `max(0, my_strike - opp_guard) + max(0, my_guard - opp_strike)`.
  - Opponent play reveals they consistently allocate `guard: 10` every single round (rendering offensive damage via strike <= 10 impossible, earning 0 net damage) and use heavy strikes (typically 8 to 10).
  - Maximizing strike against an opponent with guard 10 earns 0 offensive points, while failing to max guard lets the opponent harvest easy surplus guard or damage points against me.

- **Optimal Allocation Strategy:**
  - **Always maximize guard:** Set `[allocate_guard: 10]` in every single round (Rounds 1–4). A guard of 10 completely blocks any enemy strike (up to 10) so the opponent gets 0 net damage, while also guaranteeing maximum surplus guard points (`10 - opp_strike`) whenever the opponent strikes with less than 10.
  - **Maximize strike defensively to deny surplus guard:** When the opponent sets high guard (e.g., 10), allocating `[allocate_strike: 10]` forces their surplus guard `(opp_guard - my_strike)` down to 0, completely denying them surplus points.
  - Therefore, unless the opponent demonstrates a specific flaw (e.g., persistent guard < 10 where a lower strike is irrelevant, or low strike where surplus guard is guaranteed), default strictly to maximizing both parameters: `[allocate_strike: 10]` and `[allocate_guard: 10]` across all rounds to achieve perfect defense and deny all opponent surplus.

- **Round-by-Round Execution:**
  - **Round 1:**
    - `allocate_strike`: `[allocate_strike: 10]` (prevents opponent surplus guard on turn 1).
    - `allocate_guard`: `[allocate_guard: 10]` (prevents all incoming damage and maximizes potential surplus points).
  - **Rounds 2–4:**
    - Inspect previous round results:
      - If opponent guard is 10: keep `[allocate_strike: 10]` to deny opponent surplus points.
      - If opponent guard is consistently low (< 10): maintain `[allocate_strike: 10]` to score net damage `10 - opp_guard`.
      - In all cases: keep `[allocate_guard: 10]` to eliminate all incoming damage and extract maximum surplus whenever opponent strikes with less than 10.

- **Formatting:**
  - Always respond strictly with the required token format: `[allocate_strike: n]` or `[allocate_guard: n]`, preceded by at most one short sentence of reasoning.