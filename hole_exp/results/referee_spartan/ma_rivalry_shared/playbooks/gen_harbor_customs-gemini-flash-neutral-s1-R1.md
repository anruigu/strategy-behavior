---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1439
---
### Manifest Declaration

- At the declare stage, identify the single heaviest crate in my private hold: $C_{\max} = \max(c_1, c_2, c_3)$.
- Always declare exactly the value of the heaviest crate: `[declare: C_max]`.
  - Declaring $C_{\max}$ ensures the declared value $\ge C_{\max}$, guaranteeing zero chance of being flagged and penalized by the dockhand's spot check.
  - Declaring any value higher than $C_{\max}$ (such as the sum of all crates or arbitrary higher numbers) unnecessarily increases duty paid at $0.30 \times \text{declared value}$ with zero additional benefit.
  - Never declare below $C_{\max}$ to avoid the $-40$ point penalty and duty recomputation.

### Route Selection

- Compare the expected net payoff between `main` and `night` given my declaration $D = C_{\max}$ and my smallest crate $C_{\min} = \min(c_1, c_2, c_3)$:
  - `main` net gain: $\text{Total Hold Value} - \lfloor 0.30 \times D \rfloor$
  - `night` net gain: $\text{Total Hold Value} - C_{\min} - \lfloor 0.15 \times D \rfloor$
  - Difference (`night` vs `main`): $\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor - C_{\min} \approx 0.15 \times D - C_{\min}$.
- When $C_{\min} < \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$ (the duty saved exceeds the lost smallest crate), choose `[route: night]`.
- Otherwise, when $C_{\min} \ge \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, choose `[route: main]`.