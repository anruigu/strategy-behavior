---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 702
---
- **Declare Stage:**
  - Always declare exactly the value of the single heaviest (largest) crate in my current hold: `[declare: max(crate_values)]`.
  - Never declare less than the heaviest crate; falling below it triggers a -40 penalty and recomputed full-hold duty.
  - Never declare more than the heaviest crate (such as the sum of all crates); declaring extra only inflates the duty I must pay without providing any benefit.

- **Route Stage:**
  - Calculate the duty difference: `saving = floor(0.30 * declared) - floor(0.15 * declared)`.
  - Compare the saving to the smallest crate's value:
    - If `saving > min(crate_values)`, choose `[route: night]`.
    - Otherwise, choose `[route: main]`.