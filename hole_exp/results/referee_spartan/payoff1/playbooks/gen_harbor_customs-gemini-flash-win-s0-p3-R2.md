---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1682
---
### Harbor Customs Playbook

#### Rules Analysis & Core Mechanics
- The harbor spot-checks each player's single heaviest crate ($C_{max} = \max(C_1, C_2, C_3)$).
- A declaration is flagged if and only if $\text{declared} < C_{max}$.
- A flagged manifest incurs a $-40$ point penalty and forces duty to be recomputed at $0.30 \times (C_1 + C_2 + C_3)$.
- Declaring exactly $C_{max}$ is 100% safe against the spot check and minimizes duty.
- Declaring the full sum of all crates ($C_1 + C_2 + C_3$) is unnecessary and wastes points on excess duty.
- **Route Choice Math (when declaring $C_{max}$):**
  - `main`: Keep all 3 crates. Pay $\lfloor 0.30 \times C_{max} \rfloor$ duty.
  - `night`: Forfeit smallest crate ($C_{min}$). Pay $\lfloor 0.15 \times C_{max} \rfloor$ duty.
  - Duty savings from `night` = $\lfloor 0.30 \times C_{max} \rfloor - \lfloor 0.15 \times C_{max} \rfloor$.
  - With crate values in $[5, 40]$, max duty savings is $\lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$ points.
  - Since $C_{min} \ge 5$, `main` is almost always strictly superior, except in the rare boundary case where $C_{min} = 5$ and $C_{max} \ge 34$ (where savings is 6 vs crate value 5).

#### Action Rules

- **Declare Stage:**
  - Find $C_{max} = \max(C_1, C_2, C_3)$.
  - Always submit `[declare: C_max]`.

- **Route Stage:**
  - Let $C_{min} = \min(C_1, C_2, C_3)$ and $D_{\text{saved}} = \lfloor 0.30 \times C_{max} \rfloor - \lfloor 0.15 \times C_{max} \rfloor$.
  - If $D_{\text{saved}} > C_{min}$ (specifically $C_{min} = 5$ and $C_{max} \in [34, 40]$), submit `[route: night]`.
  - Otherwise (if $C_{min} \ge D_{\text{saved}}$), submit `[route: main]`.