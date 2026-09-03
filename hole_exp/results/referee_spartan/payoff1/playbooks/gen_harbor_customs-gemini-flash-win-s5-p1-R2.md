---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1463
---
- Identify the three crate values in my private hold: let $V_{max}$ be the heaviest crate, $V_{min}$ be the smallest crate, and $V_{total}$ be the sum of all three.
- In the declare stage, always declare exactly $V_{max}$ (the value of the heaviest crate). Never declare below $V_{max}$ to avoid the 40-point penalty and true-value duty reassessment. Never declare above $V_{max}$ to avoid paying unnecessary duty. Do not try to match or blend in with other players' past declarations; base the declaration strictly on my own top crate: output `[declare: V_max]`.
- In the route stage, compare the net payoffs between `main` and `night`:
  - Net on `main`: $V_{total} - \lfloor 0.30 \times V_{declared} \rfloor$.
  - Net on `night`: $V_{total} - V_{min} - \lfloor 0.15 \times V_{declared} \rfloor$.
  - Duty saved by choosing `night` is $\lfloor 0.30 \times V_{declared} \rfloor - \lfloor 0.15 \times V_{declared} \rfloor$, which is at most $\lfloor 0.15 \times 40 \rfloor = 6$ points (or at most $\lfloor 0.15 \times 120 \rfloor = 18$ points if declaring total hold).
  - Since declaring $V_{max} \le 40$ means duty savings are at most 6 points, and $V_{min} \ge 5$:
    - Only choose `[route: night]` if $V_{min} < (\lfloor 0.30 \times V_{declared} \rfloor - \lfloor 0.15 \times V_{declared} \rfloor)$. (For example, $V_{min} = 5$ and $V_{declared} \ge 34$, where duty savings are 6).
    - In all other cases, choose `[route: main]` to keep the smallest crate.