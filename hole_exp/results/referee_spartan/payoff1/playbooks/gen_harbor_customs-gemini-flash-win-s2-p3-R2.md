---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 931
---
### Harbor Customs Playbook

- **Stage 1 (Declare):**
  - Identify the single heaviest crate in my current private hold (let its value be $H$).
  - Always declare exactly $H$ (`[declare: H]`). 
  - Never declare above $H$ (which pointlessly inflates duty) and never declare below $H$ (which triggers the -40 penalty and true-value duty).
  - Do not declare the full hold sum, regardless of what other players declare.

- **Stage 2 (Route):**
  - Let $S$ be the value of my smallest crate and $D = \text{declared value} = H$.
  - Calculate the duty difference: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - Note: Since max $D = 40$, $\Delta \text{duty} \le 6$, while min crate value is 5.
  - If $S < \Delta \text{duty}$, choose `[route: night]`.
  - If $S \ge \Delta \text{duty}$, choose `[route: main]`. (In practice, unless $S = 5$ and $D \ge 34$, `[route: main]` is strictly optimal).