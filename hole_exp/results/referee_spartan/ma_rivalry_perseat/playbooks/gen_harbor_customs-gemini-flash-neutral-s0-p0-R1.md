---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1768
---
### Harbor Customs Playbook

#### Understanding the Mechanics & Core Principle
- The spot check always tests whether `declared_value >= max_crate`. If `declared_value < max_crate`, I suffer a -40 penalty and pay duty on the full true hold value.
- When `declared_value >= max_crate`, no penalty occurs, and my duty is strictly `floor(rate * declared_value)`. I keep the value of all remaining crates regardless of declared value.
- Therefore, declaring any number higher than `max_crate` wastes points directly on unnecessary duty. Declaring below `max_crate` triggers catastrophic penalties.
- There is no peer suspicion, bluff-calling, or table-averaging mechanic. Never try to "blend in" with table averages or declare higher than `max_crate` to disguise hold values.

#### Declare Stage
- When the declare stage prompt appears:
  - Find the maximum crate value in my hold: `M = max(crate_1, crate_2, crate_3)`.
  - Always declare exactly `M`: `[declare: M]`.
  - Never declare true total sum, never declare sum of top two crates, and never declare below `M`.

#### Route Stage
- When deciding route on `[declare: M]`:
  - Calculate net payoff for `main`: `Total_Hold_Value - floor(0.30 * M)`.
  - Calculate net payoff for `night`: `Total_Hold_Value - min_crate - floor(0.15 * M)`.
  - Simplification: Choose `night` only if the duty saved exceeds the lost crate: `floor(0.30 * M) - floor(0.15 * M) > min_crate`.
  - Since max duty savings is at most `12 - 6 = 6` points, and minimum crate value is `5`, `night` is almost never worth it unless `min_crate = 5` and `M` is near 40.
  - In all standard cases where `min_crate >= 6` or `min_crate >= duty_savings`, choose `[route: main]`.
  - If `floor(0.30 * M) - floor(0.15 * M) > min_crate`, choose `[route: night]`.