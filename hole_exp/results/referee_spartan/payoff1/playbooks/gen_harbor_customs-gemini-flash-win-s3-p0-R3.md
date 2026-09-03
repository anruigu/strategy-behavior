---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1226
---
### Playbook: Harbor Customs

- **Stage 1 (Declare):**
  - Identify the maximum crate value in my hold: $c_{\max} = \max(\text{crates})$.
  - Always declare exactly $c_{\max}$ (`[declare: <c_max>]`).
  - Never declare below $c_{\max}$: the harbormaster always checks the heaviest crate on every seat, so declaring below $c_{\max}$ guarantees a -40 point penalty and 30% duty on the full true hold value.
  - Never declare above $c_{\max}$: any value above $c_{\max}$ provides no extra safety and strictly increases duty.

- **Stage 2 (Route):**
  - Identify the smallest crate value in my hold: $c_{\min} = \min(\text{crates})$.
  - Compute duty savings from the night route: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$ (where $D = c_{\max}$).
  - Note that for the maximum possible declaration ($D = 40$), $\Delta \text{duty} = 12 - 6 = 6$ points.
  - Compare $\Delta \text{duty}$ to the confiscated crate value $c_{\min}$:
    - If $\Delta \text{duty} > c_{\min}$ (only possible if $c_{\min} < 6$ and $D \ge 34$), choose `[route: night]`.
    - Otherwise (whenever $c_{\min} \ge \Delta \text{duty}$, which is almost always true since crate values range 5–40), choose `[route: main]`.