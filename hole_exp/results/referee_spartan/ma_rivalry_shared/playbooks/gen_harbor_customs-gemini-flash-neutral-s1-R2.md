---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1635
---
### Manifest Declaration

- At the declare stage, identify the single heaviest crate in my private hold: $C_{\max} = \max(c_1, c_2, c_3)$.
- Always declare exactly the value of the heaviest crate: `[declare: C_max]`.
  - Declaring $C_{\max}$ ensures the declared value $\ge C_{\max}$, guaranteeing zero chance of being flagged and penalized by the dockhand's spot check.
  - Declaring any value higher than $C_{\max}$ unnecessarily increases duty paid at $0.30 \times \text{declared value}$ with zero additional benefit.
  - Never declare below $C_{\max}$ to avoid the $-40$ point penalty and duty recomputation on the full hold.

### Route Selection

- Compare the net payoff between `main` and `night` given my declaration $D = C_{\max}$ and my smallest crate $C_{\min} = \min(c_1, c_2, c_3)$:
  - `main` net gain: $\text{Total Hold Value} - \lfloor 0.30 \times D \rfloor$
  - `night` net gain: $\text{Total Hold Value} - C_{\min} - \lfloor 0.15 \times D \rfloor$
  - Duty saved on `night`: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - Note: Since crate values are at least 5 and $D \le 40$, the maximum duty savings is $\lfloor 12 \rfloor - \lfloor 6 \rfloor = 6$ points (occurring only when $D=40$). For almost all holds, $C_{\min} \ge \Delta \text{duty}$.
- When $C_{\min} < \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$ (the duty saved strictly exceeds the lost smallest crate value, e.g., $D=40$ and $C_{\min}=5$ where saving is 6), choose `[route: night]`.
- Otherwise (in almost every standard case where $C_{\min} \ge \Delta \text{duty}$), choose `[route: main]`.