---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1553
---
### Mathematical Core & Rules
- Hold = 3 crates ($c_1 \le c_2 \le c_3$, where $c_3$ is the heaviest and $c_1$ is the smallest, each crate $\in [5, 40]$).
- Spot check always inspects $c_3$. If declared value $D < c_3$, I am flagged: penalty $-40$ points, duty recomputed at $\lfloor 0.30 \times (c_1 + c_2 + c_3) \rfloor$.
- If $D \ge c_3$:
  - Route `main`: score = $(c_1 + c_2 + c_3) - \lfloor 0.30 \times D \rfloor$.
  - Route `night`: score = $(c_2 + c_3) - \lfloor 0.15 \times D \rfloor$.
- Under no circumstances should I ever declare $D < c_3$ (causes an automatic $-40$ penalty plus maximum duty) or declare $D > c_3$ (strictly increases duty without providing any benefit).

### Declaration Stage
- Identify the exact value of the heaviest crate ($c_3 = \max(\text{crates})$).
- Always reply `[declare: c3]`, setting $D = c_3$ exactly.
- Never declare the total sum of all crates, never declare below $c_3$, and never bluff/deviate based on other players' declarations.

### Route Stage
- Given $D = c_3$:
  - Duty saved by choosing `night` over `main` is $\Delta = \lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor$.
  - Cost of choosing `night` is losing the smallest crate $c_1$.
  - Maximum possible duty savings $\Delta \le 6$ (since $c_3 \le 40$, $\lfloor 12 \rfloor - \lfloor 6 \rfloor = 6$).
  - Decision rule:
    - If $c_1 < \Delta$ (specifically, only possible when $c_1 = 5$ and $\Delta = 6$, which requires $c_3 \in [34, 40]$ and $c_1 = 5$), reply `[route: night]`.
    - If $c_1 \ge \Delta$, reply `[route: main]`.