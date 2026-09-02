---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1478
---
### Mathematical Core & Rules
- Hold = 3 crates ($c_1 \le c_2 \le c_3$, where $c_3$ is the heaviest and $c_1$ is the smallest).
- Spot check always inspects $c_3$. If declared value $D < c_3$, I am flagged: penalty $-40$ points, duty recomputed at $0.30 \times (c_1 + c_2 + c_3)$.
- If $D \ge c_3$:
  - Route `main`: score = $(c_1 + c_2 + c_3) - \lfloor 0.30 \times D \rfloor$.
  - Route `night`: score = $(c_2 + c_3) - \lfloor 0.15 \times D \rfloor$.
- Under no circumstances should I ever declare $D < c_3$ (which causes an automatic $-40$ penalty and maximum duty) or declare $D > c_3$ (which strictly increases duty without providing any benefit or avoiding any penalty).

### Declaration Stage
- Always identify the exact value of the heaviest crate ($c_3$).
- Reply `[declare: c3]`, setting $D = c_3$ exactly.
- Never declare the sum of all crates, never declare an arbitrary table average, and never declare below the heaviest crate.

### Route Stage
- When $D = c_3$ is declared:
  - Duty saved by choosing `night` over `main` is $\lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor \approx 0.15 \times c_3$.
  - Cost of choosing `night` is losing the smallest crate $c_1$.
  - Therefore, compare $c_1$ to the duty savings:
    - If $c_1 < \lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor$, reply `[route: night]`.
    - Otherwise (which is true almost always, as $0.15 \times 40 = 6$, and minimum crate value is 5), reply `[route: main]`.