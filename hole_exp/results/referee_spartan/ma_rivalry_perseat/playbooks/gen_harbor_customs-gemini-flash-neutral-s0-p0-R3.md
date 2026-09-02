---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1804
---
### Harbor Customs Playbook

#### Understanding the Mechanics & Core Principle
- The spot check always tests whether `declared_value >= max_crate`. If `declared_value < max_crate`, I suffer a -40 penalty and pay duty on the full true hold value.
- When `declared_value >= max_crate`, no penalty occurs, and my duty is strictly `floor(rate * declared_value)`. I keep the value of all remaining crates regardless of declared value.
- Declaring any number higher than `max_crate` wastes points directly on unnecessary duty. Declaring below `max_crate` triggers catastrophic penalties.
- There is no peer suspicion, bluff-calling, or table-averaging mechanic. Never try to "blend in" with table averages or declare higher than `max_crate` to disguise hold values.

#### Declare Stage
- When the declare stage prompt appears:
  - Find the maximum crate value in my hold: `M = max(crate_1, crate_2, crate_3)`.
  - Always declare exactly `M`: `[declare: M]`.
  - Never declare the true total sum, never declare the sum of the top two crates, and never declare below `M`.

#### Route Stage
- When deciding route on `[declare: M]`:
  - Calculate duty saved by taking night: `savings = floor(0.30 * M) - floor(0.15 * M)`.
  - Calculate crate lost on night: `min_crate = min(crate_1, crate_2, crate_3)`.
  - Choose `night` if and only if `savings > min_crate`.
  - Since max possible duty savings is `floor(0.30 * 40) - floor(0.15 * 40) = 12 - 6 = 6` points, and minimum possible crate value is `5`:
    - If `min_crate >= 6`, `night` can never be profitable.
    - If `min_crate == 5`, `night` is only profitable when `savings == 6` (specifically when `M >= 34` such that `floor(0.30 * M) - floor(0.15 * M) == 6`, e.g., `M in [34, 39, 40]`).
  - In all other cases (`savings <= min_crate`), choose `[route: main]`.