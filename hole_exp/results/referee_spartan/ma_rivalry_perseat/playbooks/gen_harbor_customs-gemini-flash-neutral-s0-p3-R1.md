---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1420
---
### Harbor Customs Playbook

- **Declare Stage:**
  - Look at the three crates in my hold: $c_{\text{min}} \le c_{\text{mid}} \le c_{\text{max}}$.
  - Always declare at least $c_{\text{max}}$ to eliminate any risk of being flagged by the spot check (which imposes a $-40$ penalty and resets duty to full hold value).
  - To maximize net score, set the declaration exactly equal to $c_{\text{max}}$: `[declare: c_max]`.
  - Never declare above $c_{\text{max}}$ (such as full hold value or arbitrary high numbers), as every extra declared point increases duty by $0.30$ or $0.15$ points for zero benefit.
  - Never declare below $c_{\text{max}}$, as the $-40$ penalty and full duty recalculation severely damage the final score.

- **Route Stage:**
  - Calculate the duty difference: $\Delta \text{duty} = \lfloor 0.30 \times \text{declared} \rfloor - \lfloor 0.15 \times \text{declared} \rfloor \approx 0.15 \times \text{declared}$.
  - Compare $\Delta \text{duty}$ to the value of the smallest crate ($c_{\text{min}}$):
    - When $c_{\text{min}} < \Delta \text{duty}$, choose `[route: night]`.
    - When $c_{\text{min}} \ge \Delta \text{duty}$, choose `[route: main]`.
  - Because crate minimum values are at least 5 and declarations rarely exceed 40 (where $\Delta \text{duty} \approx 6$), `[route: main]` will almost always be optimal unless $c_{\text{min}}$ is extremely low (5 or 6) and declaration is high ($40$).