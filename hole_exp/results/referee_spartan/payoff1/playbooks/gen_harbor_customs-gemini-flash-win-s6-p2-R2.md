---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 6
round: 2
chars: 1755
---
### Core Rules & Mechanics
- Hold consists of 3 crates: $c_{\min} \le c_{\text{mid}} \le c_{\max}$. Total true value $T = c_{\min} + c_{\text{mid}} + c_{\max}$.
- Spot check inspection: Ref checks if $\text{declared} < c_{\max}$.
  - If flagged: lose 40 points penalty + pay full true duty $\lfloor 0.30 \times T \rfloor$.
  - To avoid penalty with 100% certainty, declare $D \ge c_{\max}$.
- Duty & Routes:
  - `main`: Keep all crates. Score = $T - \lfloor 0.30 \times D \rfloor$.
  - `night`: Harbor confiscates $c_{\min}$. Score = $(T - c_{\min}) - \lfloor 0.15 \times D \rfloor$.

---

### Stage 1: Manifest Declaration

- Always declare exactly $D = c_{\max}$ (the value of the single heaviest crate).
  - Never declare above $c_{\max}$; exceeding $c_{\max}$ only raises the duty paid without providing any safety benefit.
  - Never declare below $c_{\max}$; the dockhand always measures the heaviest crate, so declaring $< c_{\max}$ triggers a certain 40-point penalty and full duty.
- Output format: `[declare: <c_max>]`.

---

### Stage 2: Route Choice

- Compare the net returns between `main` and `night` given $D = c_{\max}$:
  - Duty savings from `night`: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - Note: Since $D \le 40$, $\Delta \text{duty} \le \lfloor 12 \rfloor - \lfloor 6 \rfloor = 6$.
  - Since minimum crate value is at least 5 (and usually $\ge 6$), losing $c_{\min}$ is almost always worse than paying full duty.
- Decision rule:
  - If $c_{\min} \ge \Delta \text{duty}$, choose `[route: main]`.
  - If $c_{\min} < \Delta \text{duty}$ (e.g., $c_{\min} = 5$ and $D \ge 34$, where $\Delta \text{duty} = 6$), choose `[route: night]`.
  - Output format: `[route: main]` or `[route: night]`.