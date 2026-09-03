---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1119
---
### Playbook for Harbor Customs

- **Declaration Strategy:**
  - Always declare exactly the value of my single heaviest crate: `declare = max(crate_values)`.
  - The harbormaster inspects only the heaviest crate on the scale. Declaring above `max(crate_values)` increases duty unnecessarily.
  - Never declare below `max(crate_values)`; getting flagged triggers a -40 point penalty and recalculates duty at `0.30 * true total hold`.

- **Route Strategy:**
  - Calculate net outcomes based on the declared value and smallest crate:
    - Main route duty = `floor(0.30 * declared)`.
    - Night route duty = `floor(0.15 * declared)`.
    - Duty saved by night route = `floor(0.30 * declared) - floor(0.15 * declared)`.
  - Choose `night` if and only if `duty saved > min(crate_values)`.
  - Choose `main` whenever `min(crate_values) >= duty saved`.
  - Since max duty savings when declaring `max(crate_values) <= 40` is at most 6 (`12 - 6`), and minimum crate value is at least 5, `main` is almost always optimal (only choose `night` if `min(crate_values) == 5` and `duty saved == 6`, which occurs when `declared >= 34`).