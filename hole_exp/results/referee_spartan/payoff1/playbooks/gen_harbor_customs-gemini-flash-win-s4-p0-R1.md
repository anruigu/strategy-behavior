---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1154
---
### Strategy & Rules

- **Declare Stage:**
  - Let $C_{\max}$ be the maximum crate value in my hold.
  - Set my declaration strictly equal to $C_{\max}$ (`[declare: C_max]`).
  - Never declare more than $C_{\max}$ (doing so unnecessarily inflates duty without reducing penalty risk).
  - Never declare less than $C_{\max}$ (doing so triggers the 40-point harbormaster penalty and forces maximum duty).

- **Route Stage:**
  - Let $C_{\min}$ be the smallest crate value in my hold and $D = C_{\max}$ be my declared value.
  - Calculate the duty difference between routes: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - Compare $\Delta \text{duty}$ to $C_{\min}$:
    - If $\Delta \text{duty} > C_{\min}$, choose `[route: night]`.
    - If $\Delta \text{duty} \le C_{\min}$, choose `[route: main]`.
  - Since $\Delta \text{duty} \approx 0.15 \times D \le 0.15 \times 40 = 6$, and minimum crate value is at least 5, `night` is only profitable when $C_{\min} \le 5$ and $D \ge 34$ (where $\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor = 6 > 5$). In almost all standard hands, choose `[route: main]`.