---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1237
---
### Playbook for Harbor Customs

- **Declaration Strategy:**
  - Always declare exactly the value of my single heaviest (maximum value) crate: `declare = max(crate_values)`.
  - Do not declare the true total sum or sum combinations of crates. The harbormaster only checks the heaviest crate on the scale. Declaring higher than the heaviest crate strictly increases duty without providing extra protection.
  - Never declare below the heaviest crate value; getting flagged imposes a -40 penalty plus full duty (0.30 x true total hold value).

- **Route Strategy:**
  - Compare the duty savings of the night route against the value of the confiscated smallest crate:
    - Main route net score = `Total Hold - floor(0.30 * declared)`.
    - Night route net score = `Total Hold - min(crate_values) - floor(0.15 * declared)`.
    - Duty saved by Night = `floor(0.30 * declared) - floor(0.15 * declared)`.
  - Choose `night` if and only if `duty saved > min(crate_values)`.
  - Choose `main` whenever `min(crate_values) >= duty saved`. (With crate values between 5 and 40, duty saved by declaring `max(crate)` is at most `floor(0.30*40) - floor(0.15*40) = 12 - 6 = 6`, meaning `main` is optimal virtually every round unless `min(crate) < 6`).