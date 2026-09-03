---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1171
---
### Harbor Customs Playbook

- **Declare Stage:**
  - Inspect the three crates in my hold: identify `C_max` (the highest value) and `C_min` (the lowest value).
  - Always declare exactly `declare = C_max`.
  - Never declare below `C_max`; doing so triggers a spot-check failure, incurring a 40-point penalty and duty recomputed on the true total hold.
  - Never declare above `C_max` (such as true hold total); excess declaration provides zero additional protection and only wastes points on duty.
  - Reply with `[declare: C_max]`.

- **Route Stage:**
  - Compute duty savings for `night`: `Duty_Savings = floor(0.30 * declare) - floor(0.15 * declare)`.
  - Compare `Duty_Savings` to `C_min` (the value of the smallest crate lost on `night`):
    - Choose `[route: night]` if and only if `Duty_Savings > C_min`.
    - Otherwise, choose `[route: main]`.
  - Practical threshold: Maximum possible duty savings is 6 points (achieved when `declare >= 34`). Since minimum crate value is 5, `night` is only optimal if `C_min == 5` and `declare >= 34` (saving 6 points vs losing 5). In all other scenarios (`C_min >= 6` or `declare < 34`), `[route: main]` is strictly superior.