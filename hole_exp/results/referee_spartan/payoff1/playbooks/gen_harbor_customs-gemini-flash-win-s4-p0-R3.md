---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 1254
---
### Strategy & Rules

- **Declare Stage:**
  - Let $C_{\max}$ be the maximum crate value in my private hold.
  - Set my declaration strictly equal to $C_{\max}$ (`[declare: C_max]`).
  - Never declare more than $C_{\max}$ (doing so unnecessarily inflates duty without reducing penalty risk).
  - Never declare less than $C_{\max}$ (the dockhand always samples the heaviest crate, so any declaration below $C_{\max}$ triggers the 40-point penalty and forces full duty recalculation).

- **Route Stage:**
  - Let $C_{\min}$ be the smallest crate value in my hold and $D = C_{\max}$ be my declared value.
  - Calculate duty savings from taking the night route: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - Compare $\Delta \text{duty}$ to the cost of losing the smallest crate ($C_{\min}$):
    - If $\Delta \text{duty} > C_{\min}$, choose `[route: night]`.
    - If $\Delta \text{duty} \le C_{\min}$, choose `[route: main]`.
  - Concrete rule: Since maximum crate value is 40, $\Delta \text{duty} \le 6$, while crate values are at least 5. The only case where `[route: night]` is optimal is when $C_{\min} = 5$ and $D \in [34, 40]$ ($\Delta \text{duty} = 6 > 5$). In every other scenario, choose `[route: main]`.