---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 1465
---
### Manifest Declaration Strategy
- Identify the single heaviest crate in my current private hold: `max_crate = max(crates)`.
- Always declare exactly the value of that heaviest crate (`[declare: max_crate]`).
  - Never declare below `max_crate`: doing so fails the harbormaster's spot check, incurring a -40 point penalty and 30% duty on the entire hold value.
  - Never declare above `max_crate`: declaring higher than the heaviest crate only unnecessarily inflates the duty paid.

### Route Selection Strategy
- Compute the exact point loss for both route options:
  - `main` loss = `floor(0.30 * declared_value)`
  - `night` loss = `min(crates) + floor(0.15 * declared_value)`
- Decision rule:
  - If `min(crates) + floor(0.15 * declared_value) < floor(0.30 * declared_value)`, choose `[route: night]`.
  - Otherwise, choose `[route: main]`.
  - Note: Duty savings from `night` are `floor(0.30 * declared) - floor(0.15 * declared)`, which is at most 6 points (since max declared is 40). Because crate values are at least 5, `night` is only strictly better in the edge case where `min(crates) == 5` and `floor(0.30 * declared) - floor(0.15 * declared) == 6` (which occurs when `declared >= 34`). In all other cases, `main` is optimal or tied.

### Response Formatting
- Declare stages: include a single brief reasoning sentence followed by `[declare: X]`.
- Route stages: include a single brief reasoning sentence followed by `[route: main]` or `[route: night]`.