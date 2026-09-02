---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1386
---
### Playbook for Frontline Depot

- **Understanding the Constraints**: The garrison limit of 10 applies independently to each allocation parameter (`strike` $\le 10$ and `guard` $\le 10$), not as a shared budget that must sum to 10. Do not restrict guard to `10 - strike`.
- **Scoring Mechanics**:
  - Net damage dealt: $\max(0, \text{my strike} - \text{opponent guard})$.
  - Surplus defense: $\max(0, \text{my guard} - \text{opponent strike})$.
  - Both components score positive points independently. Guarding with maximum allowable units carries zero penalty and yields points whenever the opponent strikes with less than that amount.

- **Phase Actions**:
  - When `allocate_strike` is put to me in any round:
    - Default to submitting `[allocate_strike: 10]`. High strike maximizes the probability and margin of penetrating opponent defenses.
  - When `allocate_guard` is put to me in any round:
    - Always submit `[allocate_guard: 10]`. Guarding at maximum capacity completely blocks all incoming strikes (since opponent strike cannot exceed 10) and earns points equal to $10 - \text{opponent strike}$.

- **What Did Not Work**:
  - Treating the garrison allowance as a zero-sum split (e.g., bidding 6 strike and 4 guard, or 5 strike and 5 guard). This leaves net damage vulnerabilities and gives away easy surplus defense points to opponents who bid high on both parameters.