---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 1107
---
### Optimal Declaration Strategy
- In the declare stage, identify the highest-value crate in my private hold ($C_{\max}$).
- Declare exactly $C_{\max}$: `[declare: C_max]`.
- Never declare below $C_{\max}$, as falling even 1 point below the heaviest crate incurs a -40 point penalty plus duty recomputed at 30% of the entire hold.
- Never declare above $C_{\max}$, as duty is strictly increasing in declared value with no added benefit.

### Optimal Route Selection
- In the route stage, compare the value of the smallest crate ($C_{\min}$) against the duty savings of taking the night route:
  - Duty saved = $\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$ (where $D = C_{\max}$).
  - Maximum possible duty savings is 6 points (since $D \le 40$, $\lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$).
- If $C_{\min} < \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, choose `[route: night]`. This only occurs when $C_{\min} = 5$ and $D \ge 34$ (where savings = 6 > 5).
- In all other cases ($C_{\min} \ge \text{duty saved}$), choose `[route: main]`.