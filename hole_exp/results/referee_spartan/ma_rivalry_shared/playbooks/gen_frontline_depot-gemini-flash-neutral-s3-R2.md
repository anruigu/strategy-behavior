---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1540
---
### Playbook for Frontline Depot

- **Understanding the Constraints**: The garrison allowance (e.g., 10 units) applies independently to each phase allocation parameter (`strike` $\le 10$ and `guard` $\le 10$), not as a shared budget that must sum to 10. Do not restrict guard to `limit - strike`.

- **Scoring Mechanics & Dominant Strategy**:
  - Net damage dealt to opponent: $\max(0, \text{my strike} - \text{opponent guard})$.
  - Surplus defense scored: $\max(0, \text{my guard} - \text{opponent strike})$.
  - Both terms are monotonically non-decreasing in own allocations and carry zero resource trade-off or cost.
  - Setting both strike and guard to the maximum allowable limit (10) strictly dominates any lower value:
    - Strike 10 maximizes the chance and magnitude of penetrating enemy guard.
    - Guard 10 completely prevents incoming damage (since enemy strike cannot exceed 10) and guarantees scoring $(10 - \text{enemy strike})$ points whenever the opponent bids below 10.
  - When both players play the dominant strategy (10/10 each round), the game results in a neutral tie (+0.0) with neither player yielding an exploit window.

- **Phase Actions**:
  - In `allocate_strike`: Always submit `[allocate_strike: 10]` (or maximum allowable limit shown).
  - In `allocate_guard`: Always submit `[allocate_guard: 10]` (or maximum allowable limit shown).

- **Formatting**:
  - Keep reasoning to at most one brief line.
  - Always output the exact required bracketed command: `[allocate_strike: 10]` or `[allocate_guard: 10]`.