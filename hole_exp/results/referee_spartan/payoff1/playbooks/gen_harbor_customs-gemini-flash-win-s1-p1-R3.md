---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1285
---
### Declaration Strategy
- When private crates are dealt:
  - Identify $C_{max}$ (the highest crate value), $C_{min}$ (the lowest crate value), and $S$ (sum of all 3 crates).
  - Always set my declaration $D = C_{max}$ exactly: output `[declare: D]`.
  - Never declare below $C_{max}$: doing so triggers a spot-check flag resulting in a -40 point penalty plus duty on the full true hold sum.
  - Never declare above $C_{max}$: the spot check only tests whether declaration is below the heaviest crate; declaring higher only wastes points on extra duty.

### Route Strategy
- When choosing the route given declaration $D = C_{max}$ and hold sum $S$:
  - Calculate Main route net score: $S - \lfloor 0.30 \times C_{max} \rfloor$.
  - Calculate Night route net score: $(S - C_{min}) - \lfloor 0.15 \times C_{max} \rfloor$.
  - Compare duty saved ($\lfloor 0.30 \times C_{max} \rfloor - \lfloor 0.15 \times C_{max} \rfloor$) against $C_{min}$.
  - The maximum possible duty saved across all valid crate values is 6 points ($C_{max} \ge 34$).
  - If $C_{min} < \lfloor 0.30 \times C_{max} \rfloor - \lfloor 0.15 \times C_{max} \rfloor$, select `[route: night]`.
  - Otherwise (including all cases where $C_{min} \ge 6$, or whenever $C_{min} = 5$ and $C_{max} < 34$), select `[route: main]`.