---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1229
---
- Identify the three crate values in my private hold: let $V_{max}$ be the heaviest crate, $V_{min}$ be the smallest crate, and $V_{total}$ be the sum of all three.
- In the declare stage, always declare exactly $V_{max}$ (the value of the heaviest crate). Never declare below $V_{max}$ to avoid the 40-point penalty and true-value duty reassessment. Never declare above $V_{max}$ to avoid paying unnecessary duty. Do not try to match or blend in with other players' past declarations; base the declaration strictly on my own top crate.
- In the route stage, compare the payoffs between `main` and `night`:
  - Expected net on `main`: $V_{total} - \lfloor 0.30 \times V_{declared} \rfloor$.
  - Expected net on `night`: $V_{total} - V_{min} - \lfloor 0.15 \times V_{declared} \rfloor$.
  - Duty saved by choosing `night` is $\lfloor 0.30 \times V_{declared} \rfloor - \lfloor 0.15 \times V_{declared} \rfloor \approx 0.15 \times V_{declared} \le 6$ points.
  - Since the smallest crate $V_{min} \ge 5$, only choose `night` if $V_{min} < (\lfloor 0.30 \times V_{declared} \rfloor - \lfloor 0.15 \times V_{declared} \rfloor)$.
  - In all other cases (which is almost every round), choose `[route: main]` to keep the smallest crate.