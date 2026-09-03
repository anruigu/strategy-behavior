---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 996
---
- **Stage 1 (Declare):**
  - Identify the single highest crate value in the hold: $C_{\max}$.
  - Always set the declaration exactly equal to $C_{\max}$: `[declare: C_max]`.
  - Never declare higher than $C_{\max}$ (declaring more only increases duty paid with zero additional benefit or safety).
  - Never declare lower than $C_{\max}$ (it triggers the 40-point spot-check penalty plus full recomputed duty on the true total hold value).

- **Stage 2 (Route):**
  - Identify the smallest crate value in the hold: $C_{\min}$.
  - Duty savings on night route = $\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, where $D$ is the declared value.
  - Compare the duty savings against the lost crate value $C_{\min}$:
    - If $C_{\min} < (\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor)$, choose `[route: night]`.
    - Otherwise (which is almost always true since max duty savings is at most 6 points at $D=40$ while min crate value is $\ge 5$), choose `[route: main]`.