---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1826
---
### Core Rules & Mechanics
- Hold consists of 3 crates: $c_{min} \le c_{mid} \le c_{max}$. Total true value $T = c_{min} + c_{mid} + c_{max}$.
- Spot check inspection: Ref checks if $\text{declared} < c_{max}$.
  - If flagged: lose 40 points penalty + pay full true duty $\lfloor 0.30 \times T \rfloor$.
  - To avoid penalty with 100% certainty, declare $D \ge c_{max}$.
- Duty & Routes:
  - `main`: Keep all crates. Score = $T - \lfloor 0.30 \times D \rfloor$.
  - `night`: Harbor confiscates $c_{min}$. Score = $(T - c_{min}) - \lfloor 0.15 \times D \rfloor$.

---

### Stage 1: Manifest Declaration

- When asked to declare, calculate the optimal declare value:
  - Always set $D = c_{max}$ (the value of the single heaviest crate).
  - Never declare true total $T$ or anything above $c_{max}$; exceeding $c_{max}$ only raises the duty paid without providing any safety benefit.
  - Never declare below $c_{max}$ because the heaviest crate is always checked and the 40-point penalty severely undermines total score.
- Output format: `[declare: <c_max>]`.

---

### Stage 2: Route Choice

- Compare the net returns between `main` and `night` given $D = c_{max}$:
  - `main` net gain: $T - \lfloor 0.30 \times D \rfloor$
  - `night` net gain: $T - c_{min} - \lfloor 0.15 \times D \rfloor$
  - Difference (`main` vs `night`): $c_{min} - (\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor) \approx c_{min} - 0.15 \times D$.
- Decision rule:
  - When $c_{min} > \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, choose `[route: main]` (saving the smallest crate is worth more than the duty discount).
  - When $c_{min} < \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, choose `[route: night]` (the duty savings exceed the loss of the tiny crate).
  - When equal, choose `[route: main]`.