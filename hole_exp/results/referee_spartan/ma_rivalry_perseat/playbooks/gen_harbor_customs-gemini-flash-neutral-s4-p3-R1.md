---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1099
---
### Playbook

- **Stage 1 (Declare):**
  - Always declare the exact value of my heaviest crate in the current hold: `[declare: max_crate]`.
  - Never declare below the heaviest crate; doing so triggers a -40 point penalty and recalculates duty at 30% of total hold value.
  - Never declare above the heaviest crate (e.g., trying to match opponent averages, bluff, or declare the full hold sum); doing so needlessly increases the duty paid without providing any safety benefit against the spot check.

- **Stage 2 (Route):**
  - Choose `[route: main]` whenever the value of my smallest crate is greater than the duty difference between routes: `smallest_crate > floor(0.30 * declared) - floor(0.15 * declared)`. In almost all standard hands, the smallest crate is worth 5 or more while duty savings from `night` are at most 6 points (since declared values are $\le 40$), making `main` strictly higher in net value.
  - Only choose `[route: night]` if the smallest crate's value is strictly less than `floor(0.30 * declared) - floor(0.15 * declared)`. Otherwise, keep all three crates and take `main`.