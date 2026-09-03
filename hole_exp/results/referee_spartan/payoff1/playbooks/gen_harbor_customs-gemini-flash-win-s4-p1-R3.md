---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 1296
---
### Manifest Declaration Strategy

- Always identify the exact value of the heaviest crate in my private hold ($C_{max}$).
- In Stage 1 (declare), declare exactly $C_{max}$ (`[declare: C_max]`).
- Never declare less than $C_{max}$, as falling below the heaviest crate incurs a massive 40-point penalty plus full duty recalculation based on total true value.
- Never declare more than $C_{max}$ (such as the total hold value or arbitrary high numbers), as duty is calculated strictly as a percentage of the declared value, and over-declaring unnecessarily inflates the duty paid with zero added benefit.

### Route Choice Strategy

- Let $C_{min}$ be the value of the smallest crate in my hold.
- When choosing the route in Stage 2 with a declaration $D = C_{max}$:
  - Calculate exact duty savings on the night route: $\Delta \text{Duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - Compare $\Delta \text{Duty}$ against $C_{min}$:
    - If $\Delta \text{Duty} > C_{min}$ (which happens only when $C_{min} = 5$ and $D \ge 34$, giving $\Delta \text{Duty} = 6 > 5$), choose `[route: night]`.
    - If $\Delta \text{Duty} \le C_{min}$ (the vast majority of cases, since $C_{min} \ge 5$ and max $\Delta \text{Duty} = 6$), choose `[route: main]` to preserve the smallest crate.