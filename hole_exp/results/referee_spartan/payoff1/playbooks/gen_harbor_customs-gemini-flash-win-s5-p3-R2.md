---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1403
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
  - Note: Since duty savings from `night` are at most `floor(0.15 * declared_value) <= floor(0.15 * 40) = 6` points, and the minimum possible crate value is 5, `night` is only viable when `min(crates) == 5` and `floor(0.30 * declared) - floor(0.15 * declared) > 5` (e.g., declared >= 34). In almost all hands, `main` is strictly optimal.

### Response Formatting
- Declare stages: include a single brief reasoning sentence followed by `[declare: X]`.
- Route stages: include a single brief reasoning sentence followed by `[route: main]` or `[route: night]`.