---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 4
round: 2
chars: 1157
---
### Strategy & Rules

- **Declare Stage:**
  - Let $C_{\max}$ be the maximum crate value in my hold.
  - Set my declaration strictly equal to $C_{\max}$ (`[declare: C_max]`).
  - Never declare more than $C_{\max}$ (doing so unnecessarily inflates duty without reducing penalty risk).
  - Never declare less than $C_{\max}$ (doing so triggers the 40-point harbormaster penalty and forces duty recomputed on full hold value).

- **Route Stage:**
  - Let $C_{\min}$ be the smallest crate value in my hold and $D = C_{\max}$ be my declared value.
  - Calculate the duty difference between routes: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - Compare $\Delta \text{duty}$ to $C_{\min}$:
    - If $\Delta \text{duty} > C_{\min}$, choose `[route: night]`.
    - If $\Delta \text{duty} \le C_{\min}$, choose `[route: main]`.
  - In practice: $\Delta \text{duty} \le 6$ across all valid $D \le 40$, while $C_{\min} \ge 5$. The only condition where `[route: night]` strictly beats `[route: main]` is when $C_{\min} = 5$ and $D \in [34, 40]$ (where $\Delta \text{duty} = 6 > 5$). In all other cases, choose `[route: main]`.