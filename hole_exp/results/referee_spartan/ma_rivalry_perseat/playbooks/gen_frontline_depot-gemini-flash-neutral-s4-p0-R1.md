---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 2201
---
### Playbook: Frontline Depot

- **Understand the Rules and Resource Constraints:**
  - In each round, strike power and guard power are selected independently, each constrained between 0 and 10 (individual allocations cannot exceed the total garrison allowance, but they do not strictly have to sum to 10 unless enforced by the arbiter; do not artificially restrict guard to `10 - strike` if larger values are permitted).
  - Net damage dealt (`max(0, strike - opp_guard)`) awards points; surplus guard over opponent strike (`max(0, guard - opp_strike)`) also awards points. 

- **Round 1 Strategy:**
  - In `allocate_strike`, open with `[allocate_strike: 6]` to test the opponent and punish passive/low defense allocations.
  - In `allocate_guard`, reply with `[allocate_guard: 6]` or `[allocate_guard: 5]` to protect against opening strikes of 5–6 and avoid yielding surplus guard points.

- **Mid-Game Strategy (Rounds 2 & 3):**
  - Track the opponent's historical strike and guard patterns:
    - If the opponent tends to mirror my strikes (e.g., escalating from 5 to 6 to 7), allocate guard 1 point above their expected strike to earn surplus guard points.
    - If the opponent guards conservatively (guarding around 5–6), push strike up to `[allocate_strike: 8]` to overpower their guard and gain net damage.
  - When anticipating aggressive strikes from the opponent, increase guard to `[allocate_guard: 7]` or `[allocate_guard: 8]`.

- **Late-Game / Round 4 Strategy:**
  - Never lower both strike and guard in the final round; that yields ties or losses if the opponent stays aggressive.
  - When in the lead or tied, maximize pressure:
    - In `allocate_strike`, reply with `[allocate_strike: 8]` or `[allocate_strike: 9]` to breach typical defensive baselines.
    - In `allocate_guard`, commit a high defensive value (e.g., `[allocate_guard: 8]` to `[allocate_guard: 10]`) rather than dropping guard down to low single digits, ensuring full protection and maximizing surplus guard against moderate strikes.

- **Formatting:**
  - Always respond strictly with the required token format: `[allocate_strike: n]` or `[allocate_guard: n]`, preceded by at most one short sentence of reasoning.