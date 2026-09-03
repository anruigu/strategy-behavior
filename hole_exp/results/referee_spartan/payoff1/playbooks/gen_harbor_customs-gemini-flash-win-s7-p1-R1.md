---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1245
---
### Harbor Customs Playbook

- **Declare Stage:**
  - Look at the three crates in my hold and find the maximum crate value $C_{\max}$.
  - Always declare exactly $C_{\max}$: `[declare: C_max]`.
  - Never declare the full sum of all three crates or anything above $C_{\max}$, even in the final round to "play safe" or "overtake." Extra declared value purely increases duty without providing any benefit, since the spot check only ever tests against the single heaviest crate.
  - Never declare below $C_{\max}$, as getting caught incurs a -40 penalty and recalculates duty at full hold value.

- **Route Stage:**
  - Let $C_{\min}$ be my smallest crate value and $D$ be my declared value ($C_{\max}$).
  - Calculate net payoff for `main`: $\text{Total Hold} - \lfloor 0.30 \times D \rfloor$.
  - Calculate net payoff for `night`: $(\text{Total Hold} - C_{\min}) - \lfloor 0.15 \times D \rfloor$.
  - Compare the duty savings against losing the smallest crate:
    - If $\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor > C_{\min}$, choose `[route: night]`.
    - Otherwise (which is almost always true when declaring $C_{\max}$ since duty savings $\approx 0.15 \times C_{\max} \le 6$, while $C_{\min} \ge 5$), choose `[route: main]`.