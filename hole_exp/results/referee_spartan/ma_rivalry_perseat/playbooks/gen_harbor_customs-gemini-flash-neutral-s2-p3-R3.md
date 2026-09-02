---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1489
---
# Harbor Customs Playbook

## Rules of Thumb & Core Mechanics
- The spot check always tests whether `declared_value >= heaviest_crate`.
- Declaring below the heaviest crate triggers a severe -40 penalty and forces duty to `0.30 * true_hold_total`.
- Declaring above the heaviest crate pays unnecessary duty on both routes without providing any additional protection.
- Route comparison when declaring `D = heaviest_crate`:
  - `main` payout: `Total_Hold - floor(0.30 * D)`
  - `night` payout: `Total_Hold - smallest_crate - floor(0.15 * D)`
  - Duty savings from night route: `duty_saved = floor(0.30 * D) - floor(0.15 * D)`.
  - Max possible duty savings is 6 points (when `D >= 34`).
  - Since minimum crate value is 5, `main` strictly dominates `night` in nearly all hands, except the rare edge case where `smallest == 5` and `duty_saved == 6`.

---

## Stage 1: Declare Stage
- Identify the three crate values in my hold and find the maximum value `H = max(c1, c2, c3)`.
- Always set declaration exactly equal to `H`:
  - Reply `[declare: H]`.
- Under-declaring (`< H`) triggers -40 penalty; over-declaring (`> H`) wastes duty points.

---

## Stage 2: Route Stage
- Identify `S = min(c1, c2, c3)` and `H = max(c1, c2, c3)`.
- Calculate `duty_saved = floor(0.30 * H) - floor(0.15 * H)`.
- Decision rule:
  - If `S < duty_saved` (i.e. `S == 5` and `H >= 34`, where `duty_saved = 6`):
    - Reply `[route: night]`.
  - In all other cases (`S >= duty_saved`):
    - Reply `[route: main]`.