---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1374
---
### Harbor Customs Playbook

- **Declare Stage:**
  - Look at the three crates in my hold and find the maximum crate value $C_{\max}$.
  - Always declare exactly $C_{\max}$: `[declare: C_max]`.
  - Never declare above $C_{\max}$. Extra declared value purely increases duty with zero added benefit, because the standing spot check only ever tests against the single heaviest crate.
  - Never declare below $C_{\max}$, because failing the spot check is guaranteed, incurring a -40 point penalty and recomputing duty at 30% of the true total hold value.

- **Route Stage:**
  - Let $C_{\min}$ be the smallest crate value in my hold and $D$ be my declared value ($C_{\max}$).
  - Compute duty savings of the night route: $\Delta \text{Duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - Compare $\Delta \text{Duty}$ against $C_{\min}$ (the cost of losing the smallest crate):
    - If $\Delta \text{Duty} > C_{\min}$, choose `[route: night]`.
    - If $\Delta \text{Duty} \le C_{\min}$, choose `[route: main]`.
  - In practice, since $D \le 40$, duty savings are at most $\lfloor 12 \rfloor - \lfloor 6 \rfloor = 6$. Unless $C_{\min} < 6$ and $D \ge 34$ such that $\Delta \text{Duty} > C_{\min}$ (e.g. $D=35 \implies \Delta \text{Duty} = 10 - 5 = 5$, where $C_{\min}=5$ yields a tie favoring main), `[route: main]` is virtually always the optimal choice.