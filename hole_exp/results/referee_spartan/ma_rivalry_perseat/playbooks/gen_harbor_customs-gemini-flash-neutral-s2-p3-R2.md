---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1924
---
# Harbor Customs Playbook

## Rules of Thumb & Core Mechanics
- The spot check always tests whether `declared_value >= heaviest_crate`.
- Falling below the heaviest crate triggers a -40 penalty and forces duty to `floor(0.30 * true_hold_total)`.
- Declaring above the heaviest crate pays unnecessary duty on both routes without providing any extra protection. Never declare more than the heaviest crate.
- Route comparison when declaring `D = heaviest_crate`:
  - `main` payout: `Total_Hold - floor(0.30 * D)`
  - `night` payout: `Total_Hold - smallest_crate - floor(0.15 * D)`
  - Difference (`main - night`): `smallest_crate - (floor(0.30 * D) - floor(0.15 * D)) ≈ smallest_crate - 0.15 * D`.
  - Since crate values range from 5 to 40, duty savings `floor(0.30 * D) - floor(0.15 * D)` is at most 6 points (achieved only when `D >= 34`).
  - `main` strictly dominates `night` in nearly all hands, as losing the smallest crate costs 5 to 40 points, almost always exceeding the small duty savings.

---

## Stage 1: Declare Stage
- Identify the three crate values in my hold and find the maximum value `H = max(c1, c2, c3)`.
- Always set my declaration exactly equal to `H`:
  - Reply `[declare: H]`.
- What did not work:
  - Declaring below `H`: triggers a severe -40 penalty plus full duty recalculation. Never under-declare relative to `H`.
  - Declaring the full sum of all three crates or inflating the declaration: pays unnecessary extra duty for zero benefit.

---

## Stage 2: Route Stage
- Given my hold crates `(smallest, middle, heaviest)`:
  - Calculate duty saved by night: `duty_saved = floor(0.30 * heaviest) - floor(0.15 * heaviest)`.
  - If `smallest < duty_saved` (only possible if `smallest == 5` and `heaviest >= 34`, where duty saved is 6 and crate loss is 5):
    - Reply `[route: night]`.
  - Otherwise (if `smallest >= duty_saved`, which is true for virtually every hand):
    - Reply `[route: main]`.