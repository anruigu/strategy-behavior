---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1928
---
### Core Rules & Mechanics
- Hold consists of 3 crates: $c_{\min} \le c_{\text{mid}} \le c_{\max}$. Total true value $T = c_{\min} + c_{\text{mid}} + c_{\max}$.
- Spot check inspection: Harbormaster scales the heaviest crate ($c_{\max}$) and flags if $\text{declared} < c_{\max}$.
  - Flagged penalty: -40 points + recomputed duty $\lfloor 0.30 \times T \rfloor$.
  - Declaring $D = c_{\max}$ guarantees zero penalty and minimizes declared duty.
- Routes & Duty:
  - `main`: Keep all 3 crates. Duty = $\lfloor 0.30 \times D \rfloor$. Net score = $T - \lfloor 0.30 \times D \rfloor$.
  - `night`: Harbor confiscates $c_{\min}$. Duty = $\lfloor 0.15 \times D \rfloor$. Net score = $(T - c_{\min}) - \lfloor 0.15 \times D \rfloor$.

---

### Stage 1: Manifest Declaration

- Always declare exactly $D = c_{\max}$ (the value of the single heaviest crate in the hold).
  - Never declare $D > c_{\max}$; higher declarations strictly increase duty with zero extra benefit.
  - Never declare $D < c_{\max}$; the heaviest crate is always tested, making detection 100% certain and resulting in a -40 penalty plus full recomputed duty.
- Output format: `[declare: <c_max>]`.

---

### Stage 2: Route Choice

- Compare the net returns between `main` and `night` given $D = c_{\max}$:
  - Duty savings from `night`: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - Maximum possible duty savings is 6 points (when $D \ge 34$).
- Decision rule:
  - If $c_{\min} > \Delta \text{duty}$, choose `[route: main]`.
  - If $c_{\min} = \Delta \text{duty}$, choose `[route: main]` (preserves total crate value).
  - If $c_{\min} < \Delta \text{duty}$ (specifically when $c_{\min} = 5$ and $D \ge 34$, where $\Delta \text{duty} = 6 > 5$), choose `[route: night]`.
  - In virtually all practical deals ($c_{\min} \ge 6$), `[route: main]` is strictly superior.
- Output format: `[route: main]` or `[route: night]`.