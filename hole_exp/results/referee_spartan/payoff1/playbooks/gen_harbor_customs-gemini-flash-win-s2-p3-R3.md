---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1001
---
### Harbor Customs Playbook

- **Stage 1 (Declare):**
  - Identify the single heaviest crate in my current private hold (let its value be $H$).
  - Always declare exactly $H$ (`[declare: H]`). 
  - Never declare above $H$ (which pointlessly inflates duty) and never declare below $H$ (which triggers the -40 penalty and true-value duty).
  - Ignore other players' declarations; do not declare the full hold sum.

- **Stage 2 (Route):**
  - Let $S$ be the value of my smallest crate and $D$ be my declared value ($H$).
  - Calculate duty savings from the night route: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - Note: Since max $D = 40$, the maximum possible $\Delta \text{duty}$ is 6 (at $D \ge 34$), while the minimum possible crate value is 5.
  - If $S < \Delta \text{duty}$ (only possible when $S = 5$ and $D \ge 34$, where savings is 6 vs loss of 5), choose `[route: night]`.
  - Otherwise ($S \ge \Delta \text{duty}$), always choose `[route: main]`.