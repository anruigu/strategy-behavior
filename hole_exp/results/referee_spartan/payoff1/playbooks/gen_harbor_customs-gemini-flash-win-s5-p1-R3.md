---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 1309
---
- Identify the three crate values in my private hold: let $V_{max}$ be the heaviest crate, $V_{min}$ be the smallest crate, and $V_{total}$ be the sum of all three crates.
- In the declare stage, always declare exactly $V_{max}$ (the value of the heaviest crate). Never declare below $V_{max}$ to avoid the 40-point penalty and true-value duty reassessment. Never declare above $V_{max}$ to avoid paying unnecessary duty. Do not try to match or blend in with other players' past declarations; base the declaration strictly on my own top crate: output `[declare: V_max]`.
- In the route stage, compare the net payoffs between `main` and `night`:
  - Net on `main`: $V_{total} - \lfloor 0.30 \times V_{declared} \rfloor$.
  - Net on `night`: $V_{total} - V_{min} - \lfloor 0.15 \times V_{declared} \rfloor$.
  - Duty saved by choosing `night` is $\Delta_{duty} = \lfloor 0.30 \times V_{declared} \rfloor - \lfloor 0.15 \times V_{declared} \rfloor$.
  - With $V_{declared} = V_{max} \le 40$, $\Delta_{duty} \le 6$ points (specifically, $\Delta_{duty} = 6$ only if $V_{declared} \ge 34$, otherwise $\le 5$).
  - Choose `[route: night]` strictly when $V_{min} < \Delta_{duty}$ (i.e., when $V_{min} = 5$ and $V_{declared} \ge 34$).
  - In all other cases (where $V_{min} \ge \Delta_{duty}$), choose `[route: main]`.