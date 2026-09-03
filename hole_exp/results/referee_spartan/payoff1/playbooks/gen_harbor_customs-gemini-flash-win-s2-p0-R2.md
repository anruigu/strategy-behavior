---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1212
---
### Harbor Customs Playbook

- **Declare Stage:**
  - Inspect the three crates in my hold: identify `C_max` (the highest value) and `C_min` (the lowest value).
  - Always declare exactly `declare = C_max`.
  - Never declare below `C_max`; doing so triggers a spot-check failure, incurring a 40-point penalty and duty recomputed on the true total hold.
  - Never declare above `C_max` (such as true hold total); excess declaration provides zero protection and only wastes points on duty.

- **Route Stage:**
  - Compute duty savings for `night`: `Duty_Savings = floor(0.30 * declare) - floor(0.15 * declare)`.
  - Compare `Duty_Savings` to `C_min` (the value lost on `night`):
    - Choose `[route: night]` if and only if `Duty_Savings > C_min` (i.e., `C_min < floor(0.30 * declare) - floor(0.15 * declare)`).
    - Otherwise, choose `[route: main]`.
  - Note on values: Duty savings max out at 6 points (when `declare` is 34–40: `floor(0.30 * 40) - floor(0.15 * 40) = 12 - 6 = 6`). Since crate values are at least 5, `night` is only viable in the rare edge case where `C_min == 5` and `declare >= 34` (where duty savings = 6 > 5). In all other cases (`C_min >= 6` or lower `declare`), `main` is strictly optimal.