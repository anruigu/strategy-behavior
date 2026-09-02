---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1394
---
### Playbook for Frontline Depot

- **Understanding the Constraints**: The public garrison allowance applies independently as an upper bound to each allocation parameter (`strike` $\le \text{limit}$ and `guard` $\le \text{limit}$). Strike and guard do not share a single depleted pool.

- **Scoring Mechanics & Dominant Strategy**:
  - Net damage dealt: $\max(0, \text{my strike} - \text{opponent guard})$.
  - Surplus defense: $\max(0, \text{my guard} - \text{opponent strike})$.
  - Since there is no cost, penalty, or trade-off between strike and guard, allocating the maximum allowable limit to both parameters strictly weakly dominates all other actions:
    - Maximum strike maximizes potential penetration against opponent guard.
    - Maximum guard completely eliminates incoming damage and captures any surplus defense points if the opponent underbids on strike.
  - When both players allocate maximum limits, the outcome is fully defended and neutral (+0.0).

- **Phase Actions**:
  - In `allocate_strike`: Check the public garrison allowance (e.g., $N$) and submit `[allocate_strike: N]`.
  - In `allocate_guard`: Check the public garrison allowance (e.g., $N$) and submit `[allocate_guard: N]`.

- **Formatting**:
  - Keep reasoning to at most one brief line or omit it entirely.
  - Always output the exact required bracketed token: `[allocate_strike: n]` or `[allocate_guard: n]`.