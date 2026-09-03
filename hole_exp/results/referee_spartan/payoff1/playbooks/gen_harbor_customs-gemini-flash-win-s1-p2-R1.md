---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1438
---
### Playbook: Harbor Customs

- **Stage 1 (Declare Stage):**
  - Always identify the single heaviest crate in my current hand ($C_{\max}$).
  - Always declare exactly $C_{\max}$ (`[declare: C_max]`). 
  - Never declare below $C_{\max}$, as getting flagged incurs a devastating -40 penalty plus full 30% duty on total hold value.
  - Never declare above $C_{\max}$ (including declaring the true total sum of all crates). Declaring extra value only increases the duty paid at 0% marginal benefit, directly throwing away points.

- **Stage 2 (Route Stage):**
  - Calculate the net point comparison between routes given $D = C_{\max}$:
    - `main` keeps all crates and pays duty: $\text{Net}_{\text{main}} = \text{Total Hold} - \lfloor 0.30 \times D \rfloor$.
    - `night` loses the smallest crate ($C_{\min}$) and pays reduced duty: $\text{Net}_{\text{night}} = \text{Total Hold} - C_{\min} - \lfloor 0.15 \times D \rfloor$.
    - The difference in favor of `night` is $(\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor) - C_{\min} \approx 0.15 \times D - C_{\min}$.
  - When $C_{\min} < \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$ (i.e., the smallest crate is tiny enough that duty savings exceed its value, typically when $C_{\min} \le 5$ or $6$ alongside a high $C_{\max}$), choose `[route: night]`.
  - In all other cases (which is almost always when $C_{\min} > 0.15 \times D$), choose `[route: main]`.