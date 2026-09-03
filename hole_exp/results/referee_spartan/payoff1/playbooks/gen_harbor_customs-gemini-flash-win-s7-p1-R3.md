---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1264
---
### Harbor Customs Playbook

- **Declare Stage:**
  - Identify the maximum crate value in my private hold: $C_{\max} = \max(\text{crates})$.
  - Always declare exactly $C_{\max}$: `[declare: C_max]`.
  - Never declare above $C_{\max}$: declaring higher only inflates duty with zero benefit, as the dockhand spot checks only the single heaviest crate.
  - Never declare below $C_{\max}$: failing the spot check is guaranteed, triggering a -40 point penalty and resetting duty to 30% of the true total hold value.

- **Route Stage:**
  - Identify the smallest crate value in my hold: $C_{\min} = \min(\text{crates})$.
  - Compute duty savings from the night route: $\Delta \text{Duty} = \lfloor 0.30 \times C_{\max} \rfloor - \lfloor 0.15 \times C_{\max} \rfloor$.
  - Compare $\Delta \text{Duty}$ against $C_{\min}$ (the lost crate value):
    - If $\Delta \text{Duty} > C_{\min}$, choose `[route: night]`.
    - If $\Delta \text{Duty} \le C_{\min}$, choose `[route: main]`.
  - Since max crate value is 40, $\Delta \text{Duty} \le 6$. Because crates are worth at least 5 points, $\Delta \text{Duty} > C_{\min}$ only occurs if $C_{\max} \ge 34$ (where $\Delta \text{Duty} = 6$) and $C_{\min} = 5$. In virtually all other hands, `[route: main]` is strictly superior.