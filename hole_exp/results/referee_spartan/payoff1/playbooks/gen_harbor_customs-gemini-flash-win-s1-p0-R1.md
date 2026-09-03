---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 970
---
# Harbor Customs Playbook

### Stage 1: Declaration
- Find the heaviest crate in my current private hold ($C_{\max}$).
- Declare exactly $C_{\max}$: `[declare: C_max]`.
- Never declare the true total hold value when it exceeds $C_{\max}$, and never declare higher than $C_{\max}$; any declaration above $C_{\max}$ needlessly increases duty paid without providing additional safety from spot checks.
- Never declare below $C_{\max}$, as the heaviest crate is always checked and falling below it triggers the -40 penalty and full 30% duty.

### Stage 2: Route Selection
- Let $C_{\min}$ be the value of my smallest crate and $D = C_{\max}$ be my declaration.
- Calculate the duty difference: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
- Compare the duty savings against the lost smallest crate:
  - When $C_{\min} < \Delta \text{duty}$, choose `[route: night]`.
  - When $C_{\min} \ge \Delta \text{duty}$, choose `[route: main]`.