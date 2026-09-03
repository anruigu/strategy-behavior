---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1334
---
# Harbor Customs Playbook

### Stage 1: Declaration
- Identify the heaviest crate in my current private hold ($C_{\max}$).
- Declare exactly $C_{\max}$: `[declare: C_max]`.
- Never declare higher than $C_{\max}$; any declaration above $C_{\max}$ needlessly increases duty paid without providing additional safety from spot checks.
- Never declare below $C_{\max}$; the harbormaster always checks the heaviest crate on top, and declaring below it guarantees a -40 penalty plus full 30% duty on the true total hold value.

### Stage 2: Route Selection
- Identify the smallest crate in my hold ($C_{\min}$) and let $D$ be my declared value ($C_{\max}$).
- Compute duty savings from the night route: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
- Compare duty savings against the loss of the smallest crate:
  - If $\Delta \text{duty} > C_{\min}$, choose `[route: night]`.
  - If $\Delta \text{duty} \le C_{\min}$, choose `[route: main]`.
- Quick check: For $D \le 40$, the maximum possible duty savings is 6 (occurring when $34 \le D \le 40$). Because crate values range from 5 to 40, `[route: night]` is only beneficial in the specific edge case where $C_{\min} = 5$ and $D \ge 34$ (saving 6 duty at a cost of 5 points, netting +1 point). In all other scenarios, strictly choose `[route: main]`.