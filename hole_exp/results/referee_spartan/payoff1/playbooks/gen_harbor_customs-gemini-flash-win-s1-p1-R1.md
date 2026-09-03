---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1164
---
### Declaration Strategy
- When private crates are dealt:
  - Identify $C_{max}$ (the highest crate value), $C_{min}$ (the lowest crate value), and $S$ (sum of all 3 crates).
  - Always set my declaration $D = C_{max}$ exactly.
  - Never declare below $C_{max}$: doing so triggers a spot-check flag resulting in a -40 point penalty plus duty on the full true sum.
  - Never declare above $C_{max}$: there is no inspection mechanic comparing declarations to other players or total value, so declaring anything above $C_{max}$ purely inflates duty paid without any protective benefit.

### Route Strategy
- When choosing the route given my declaration $D = C_{max}$ and hold sum $S$:
  - Calculate Main route net score: $S - \lfloor 0.30 \times C_{max} \rfloor$.
  - Calculate Night route net score: $(S - C_{min}) - \lfloor 0.15 \times C_{max} \rfloor$.
  - Compare the duty savings against the lost crate: duty saved on Night is $\lfloor 0.30 \times C_{max} \rfloor - \lfloor 0.15 \times C_{max} \rfloor \approx 0.15 \times C_{max}$.
  - If $C_{min} < 0.15 \times C_{max}$, select `[route: night]`.
  - If $C_{min} \ge 0.15 \times C_{max}$, select `[route: main]`.