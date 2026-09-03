---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1240
---
# Harbor Customs Playbook

### Stage 1: Declaration
- Find the heaviest crate in my current private hold ($C_{\max}$).
- Declare exactly $C_{\max}$: `[declare: C_max]`.
- Never declare higher than $C_{\max}$; any declaration above $C_{\max}$ needlessly increases duty paid without providing additional safety from spot checks.
- Never declare below $C_{\max}$; the harbormaster always checks the heaviest crate on top, and declaring below it guarantees a -40 penalty plus full duty on the true hold value.

### Stage 2: Route Selection
- Let $C_{\min}$ be the value of my smallest crate and $D$ be my declared value ($C_{\max}$).
- Calculate duty savings from night route: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
- Compare duty savings against the sacrifice of the smallest crate:
  - If $C_{\min} < \Delta \text{duty}$, choose `[route: night]`.
  - If $C_{\min} \ge \Delta \text{duty}$, choose `[route: main]`.
  - Since max duty savings $\Delta \text{duty} \le 6$ (for $D \le 40$) and crates are worth 5–40, `[route: main]` is strictly better unless $C_{\min} = 5$ and $D \ge 34$ (where savings equal 6, netting +1 point on night route). In almost all other cases, default to `[route: main]`.