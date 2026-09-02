---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1338
---
### Manifest Declaration

- At the declare stage, identify the single heaviest crate in my private hold: $C_{\max} = \max(c_1, c_2, c_3)$.
- Always declare exactly the value of the heaviest crate: `[declare: C_max]`.
  - Declaring $C_{\max}$ ensures the declared value meets or exceeds the sampled crate, guaranteeing zero chance of being flagged and penalized by the dockhand's spot check.
  - Declaring any value higher than $C_{\max}$ unnecessarily increases duty paid with zero additional benefit.
  - Declaring below $C_{\max}$ triggers a $-40$ point penalty and recomputed full-hold duty, which is always net negative.

### Route Selection

- Compare the net payoff between `main` and `night` given my declaration $D = C_{\max}$ and my smallest crate $C_{\min} = \min(c_1, c_2, c_3)$:
  - `main` duty: $\lfloor 0.30 \times D \rfloor$, keep all 3 crates.
  - `night` duty: $\lfloor 0.15 \times D \rfloor$, lose $C_{\min}$.
  - Duty saved on `night`: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
- If $\Delta \text{duty} > C_{\min}$ (e.g., $D \ge 34$ such that $\Delta \text{duty} = 6$ and $C_{\min} = 5$), choose `[route: night]`.
- Otherwise (whenever $C_{\min} \ge \Delta \text{duty}$, which holds in virtually all standard draws since crates are worth 5-40), always choose `[route: main]`.