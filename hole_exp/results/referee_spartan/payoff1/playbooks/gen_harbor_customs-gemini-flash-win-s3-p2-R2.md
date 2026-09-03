---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 785
---
- **Declare Stage:**
  - Always declare exactly the value of the single heaviest (largest) crate in my current hold: `[declare: max(crate_values)]`.
  - Never declare less than the heaviest crate; falling below it triggers a -40 penalty and recomputes full-hold duty at 30%.
  - Never declare more than the heaviest crate (such as the sum of all crates); declaring extra only inflates the duty owed without providing any benefit.

- **Route Stage:**
  - Calculate the duty difference: `saving = floor(0.30 * declared) - floor(0.15 * declared)`.
  - Compare the saving to the smallest crate's value:
    - If `saving > min(crate_values)`, choose `[route: night]`.
    - Otherwise (which is almost always the case since `saving <= 6` while crates are worth 5–40), choose `[route: main]`.