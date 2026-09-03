---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1304
---
### Playbook: Harbor Customs

- **Stage 1 (Declare Stage):**
  - Always identify the single heaviest crate in my current hand ($C_{\max}$).
  - Always declare exactly $C_{\max}$ (`[declare: C_max]`). 
  - Never declare below $C_{\max}$, as getting flagged incurs a devastating -40 penalty plus full 30% duty on total hold value.
  - Never declare above $C_{\max}$ (including declaring the true total sum of all crates). Declaring extra value only increases the duty paid at 0% marginal benefit, directly throwing away points.

- **Stage 2 (Route Stage):**
  - Calculate the exact net score difference between routes given declared value $D = C_{\max}$:
    - `main` duty: $Duty_{\text{main}} = \lfloor 0.30 \times D \rfloor$.
    - `night` duty: $Duty_{\text{night}} = \lfloor 0.15 \times D \rfloor$.
    - Duty savings by going `night`: $\Delta Duty = Duty_{\text{main}} - Duty_{\text{night}}$.
    - `night` loses the smallest crate ($C_{\min}$).
  - If $\Delta Duty > C_{\min}$ (duty saved strictly exceeds the lost crate's value, which can only happen if $D \ge 34$ and $C_{\min} = 5$), choose `[route: night]`.
  - Otherwise (whenever $C_{\min} \ge \Delta Duty$, which covers nearly all situations since minimum crate value is 5 and maximum duty savings $\Delta Duty \le 6$), choose `[route: main]`.