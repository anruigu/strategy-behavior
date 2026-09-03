---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1394
---
### Optimal Declaration Strategy
- When in the declare stage, identify the single highest-value crate in my private hold ($C_{\max}$).
- Declare exactly $C_{\max}$: `[declare: C_max]`.
- Never declare higher than $C_{\max}$ merely to match what opponents are doing or to blend in; doing so only increases duty paid with zero protection or benefit.
- Never declare lower than $C_{\max}$, as falling even 1 point below the heaviest crate incurs a -40 point penalty plus full duty on the entire hold.

### Optimal Route Selection
- When in the route stage, calculate the net payout of both routes given declared value $D = C_{\max}$, crate values $C_{\min} \le C_{mid} \le C_{\max}$, and total hold value $T = C_{\min} + C_{mid} + C_{\max}$:
  - Main net payoff: $T - \lfloor 0.30 \times D \rfloor$
  - Night net payoff: $(T - C_{\min}) - \lfloor 0.15 \times D \rfloor$
- Compare the duty saved versus the crate lost:
  - Duty saved on `night` = $\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor \approx 0.15 \times D \le 6$ points (since $D \le 40$).
  - Value lost on `night` = $C_{\min} \ge 5$ points.
- If $C_{\min} < \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, choose `[route: night]`.
- In virtually all practical cases where $C_{\min} \ge 6$ (or whenever $C_{\min} \ge \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$), choose `[route: main]`.