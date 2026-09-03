---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 894
---
- **Stage 1 (Declare):**
  - Identify the single highest crate value in the hold: $C_{\max}$.
  - Always set the declaration exactly equal to $C_{\max}$: `[declare: C_max]`.
  - Never declare higher than $C_{\max}$ (declaring more only increases duty paid with zero additional benefit or safety).
  - Never declare lower than $C_{\max}$ (it triggers the 40-point spot-check penalty plus full recomputed duty).

- **Stage 2 (Route):**
  - Identify the smallest crate value in the hold: $C_{\min}$.
  - Compute the net payout for both routes under declaration $D = C_{\max}$:
    - `main` payout: $\text{Total Hold Value} - \lfloor 0.30 \times D \rfloor$
    - `night` payout: $(\text{Total Hold Value} - C_{\min}) - \lfloor 0.15 \times D \rfloor$
  - If $C_{\min} < (\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor)$, choose `[route: night]`.
  - Otherwise, choose `[route: main]`.