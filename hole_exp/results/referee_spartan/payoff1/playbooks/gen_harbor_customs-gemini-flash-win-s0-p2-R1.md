---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1274
---
### Playbook for Harbor Customs

- **Declaration Strategy:**
  - Always declare exactly the value of my single heaviest (maximum value) crate: `declare = max(crate_values)`.
  - Do not declare the true total sum or sum combinations of crates. The harbormaster only compares my declaration against my single heaviest crate. Declaring higher than the heaviest crate strictly increases my duty without providing any extra protection against inspection.
  - Never declare below the heaviest crate value, as getting caught triggers a -40 penalty plus full duty on the true hold value.

- **Route Strategy:**
  - When deciding route, compare the duty savings against the lost crate:
    - Main route net score = `Total Hold - floor(0.30 * declared)`.
    - Night route net score = `Total Hold - Smallest Crate - floor(0.15 * declared)`.
    - Duty difference saved by Night = `floor(0.30 * declared) - floor(0.15 * declared)` (approximately `0.15 * declared`).
  - Choose `night` only when the duty saved is greater than the smallest crate's value: `floor(0.30 * declared) - floor(0.15 * declared) > min(crate_values)`.
  - Choose `main` whenever `min(crate_values) >= floor(0.30 * declared) - floor(0.15 * declared)` (which is almost always true given the legal range of crates).