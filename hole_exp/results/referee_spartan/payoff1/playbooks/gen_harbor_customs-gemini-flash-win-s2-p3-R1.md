---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 891
---
### Harbor Customs Playbook

- **Stage 1 (Declare):**
  - Identify the single heaviest crate in my current private hold (let its value be $H$).
  - Always declare exactly $H$ (`[declare: H]`). 
  - Never declare above $H$ (which pointlessly inflates duty) and never declare below $H$ (which triggers the -40 penalty and true-value duty).
  - Do not declare the full hold sum, even if it feels "natural" or "matches group trends."

- **Stage 2 (Route):**
  - Let $S$ be the value of my smallest crate and $D = \text{declared value} = H$.
  - Calculate the duty difference between routes: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor \approx 0.15 \times D$.
  - If $S < \Delta \text{duty}$, choose `[route: night]` because the duty savings exceed the crate value lost.
  - If $S \ge \Delta \text{duty}$, choose `[route: main]` to retain all three crates.