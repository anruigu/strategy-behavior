---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1309
---
### Harbor Customs Playbook

- **Declare Stage:**
  - Inspect the three crates in my hold: $c_{\text{min}} \le c_{\text{mid}} \le c_{\text{max}}$.
  - Always declare exactly the value of the heaviest crate: `[declare: c_max]`.
  - Declaring $c_{\text{max}}$ completely avoids the dockhand spot-check penalty ($-40$ points and duty recalculation on full hold value) while minimizing assessed duty.
  - Never declare above $c_{\text{max}}$, as any excess declaration pointlessly increases duty.
  - Never declare below $c_{\text{max}}$, as the penalty and full recalculation guarantee a severe score deficit.

- **Route Stage:**
  - Calculate the duty savings: $\Delta \text{duty} = \lfloor 0.30 \times \text{declared} \rfloor - \lfloor 0.15 \times \text{declared} \rfloor$.
  - Compare $\Delta \text{duty}$ against $c_{\text{min}}$ (the crate lost on the night route):
    - If $\Delta \text{duty} > c_{\text{min}}$, choose `[route: night]`.
    - If $\Delta \text{duty} \le c_{\text{min}}$, choose `[route: main]`.
  - In practice, since crate values are at least 5 and declared values never exceed 40 (max $\Delta \text{duty} = 12 - 6 = 6$), `[route: main]` is strictly optimal or tied in almost every case. Always verify the condition $\Delta \text{duty} > c_{\text{min}}$ before selecting `[route: night]`.