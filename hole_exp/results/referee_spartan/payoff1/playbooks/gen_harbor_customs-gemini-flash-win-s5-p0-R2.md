---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1144
---
### Optimal Declaration Strategy
- In the declare stage, identify the highest-value crate in my private hold ($C_{\max}$).
- Declare exactly $C_{\max}$: `[declare: C_max]`.
- Never declare below $C_{\max}$, as falling even 1 point below the heaviest crate incurs a -40 point penalty plus duty recomputed at 30% of the entire hold.
- Never declare above $C_{\max}$, as duty is strictly increasing in declared value with no added benefit.

### Optimal Route Selection
- In the route stage, compare the value of the smallest crate ($C_{\min}$) against the duty savings of taking the night route:
  - Duty saved = $\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$ (where $D = C_{\max}$).
  - Maximum possible duty savings is 6 points (since $D \le 40$, $\lfloor 12 \rfloor - \lfloor 6 \rfloor = 6$).
- If $C_{\min} < \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, choose `[route: night]`. (This can only happen if $C_{\min} = 5$ and $D \ge 34$, saving 6 duty points vs losing a 5-point crate).
- Otherwise, whenever $C_{\min} \ge \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, choose `[route: main]`.