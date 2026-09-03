---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 4
round: 2
chars: 1396
---
### Manifest Declaration Strategy

- Always identify the exact value of the heaviest crate in my private hold ($C_{max}$).
- In Stage 1 (declare), declare exactly $C_{max}$ (`[declare: C_max]`).
- Never declare less than $C_{max}$, as falling below the heaviest crate incurs a massive 40-point penalty plus full duty recalculation.
- Never declare more than $C_{max}$ (such as the total hold value or arbitrary high numbers), as duty is calculated strictly as a percentage of the declared value, and over-declaring unnecessarily inflates the duty paid with zero added benefit.

### Route Choice Strategy

- Let $C_{min}$ be the value of the smallest crate in my hold.
- When choosing the route in Stage 2 with a declaration $D = C_{max}$:
  - Calculate the duty difference: $\Delta \text{Duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor \approx 0.15 \times D$.
  - Note: Since crate values range between 5 and 40, $D \le 40$ means $\Delta \text{Duty} \le \lfloor 12 \rfloor - \lfloor 6 \rfloor = 6$.
  - Compare $\Delta \text{Duty}$ against $C_{min}$:
    - If $C_{min} < \Delta \text{Duty}$ (which can only occur if $C_{min} < 6$ and $D \ge 34$, e.g., $C_{min} = 5$ with $D \ge 34$ yields $\Delta \text{Duty} = 6 > 5$), choose `[route: night]`.
    - In virtually all other standard hands where $C_{min} \ge \Delta \text{Duty}$, choose `[route: main]` to preserve the crate.