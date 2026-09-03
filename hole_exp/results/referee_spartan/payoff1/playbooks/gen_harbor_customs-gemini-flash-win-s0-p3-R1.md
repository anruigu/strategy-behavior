---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1796
---
### Harbor Customs Playbook

#### Rules Analysis & Strategy Baseline
- The spot check always inspects the heaviest crate ($C_{max}$). If $\text{declared} < C_{max}$, a 40-point penalty applies and full duty is assessed.
- Declaring exactly $C_{max}$ is completely safe from the spot check penalty while minimizing the duty paid on the declared amount. Never declare below $C_{max}$, and never declare the full sum of crates ($C_{total}$) when underdeclaring $C_{max}$ is legally safe.
- **Route comparison when declaring $C_{max}$:**
  - `main`: Keep all crates. Net score = $C_{total} - \lfloor 0.30 \times C_{max} \rfloor$.
  - `night`: Lose smallest crate ($C_{min}$). Net score = $C_{total} - C_{min} - \lfloor 0.15 \times C_{max} \rfloor$.
  - Difference (`main` vs `night`): `main` gains $C_{min} - (\lfloor 0.30 \times C_{max} \rfloor - \lfloor 0.15 \times C_{max} \rfloor) \approx C_{min} - 0.15 \times C_{max}$.
  - Since $C_{min} \ge 5$ and $C_{max} \le 40$, the duty saving on `night` is at most $\approx 6$ points. `main` is almost always strictly superior unless $C_{min} < \lfloor 0.30 \times C_{max} \rfloor - \lfloor 0.15 \times C_{max} \rfloor$.

#### Action Rules

- **Declare Stage:**
  - Identify the maximum crate value in the hold: $C_{max} = \max(C_1, C_2, C_3)$.
  - Always submit `[declare: C_max]`.
  - Do not declare the true total sum of the hold ($C_1 + C_2 + C_3$); over-declaring simply increases duty paid without providing any safety benefit.

- **Route Stage:**
  - Calculate the duty difference: $\Delta \text{duty} = \lfloor 0.30 \times C_{max} \rfloor - \lfloor 0.15 \times C_{max} \rfloor$.
  - If $C_{min} > \Delta \text{duty}$, submit `[route: main]`.
  - If $C_{min} < \Delta \text{duty}$, submit `[route: night]`.
  - If tied, default to `[route: main]`.