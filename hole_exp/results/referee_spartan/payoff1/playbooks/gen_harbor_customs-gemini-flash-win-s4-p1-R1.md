---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1182
---
### Manifest Declaration Strategy

- Always identify the exact value of the heaviest crate in my private hold ($C_{max}$).
- In Stage 1 (declare), declare exactly $C_{max}$ ($[declare: C_{max}]$).
- Never declare less than $C_{max}$, as falling below the heaviest crate incurs a massive 40-point penalty plus full duty recalculation.
- Never declare more than $C_{max}$ (such as the total hold value or arbitrary high numbers), as duty is calculated strictly as a percentage of the declared value, and over-declaring unnecessarily inflates the duty paid with zero added benefit.

### Route Choice Strategy

- Let $C_{min}$ be the value of the smallest crate in my hold.
- When choosing the route in Stage 2 with a declaration $D = C_{max}$:
  - Calculate the duty difference: $\Delta \text{Duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor \approx 0.15 \times D$.
  - Compare $\Delta \text{Duty}$ against $C_{min}$:
    - If $C_{min} < \Delta \text{Duty}$ (the lost crate is worth less than the duty saved), choose `[route: night]`.
    - If $C_{min} \ge \Delta \text{Duty}$ (the lost crate is worth more than or equal to the duty saved), choose `[route: main]`.